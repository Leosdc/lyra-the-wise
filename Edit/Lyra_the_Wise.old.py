import discord
from discord.ext import commands
from discord.ui import View, button
import os
from groq import Groq
from dotenv import load_dotenv
import random
import re
import asyncio
import json
from pathlib import Path
from sessoes_rpg import setup_sessoes

# Importa banco de dados de sistemas
from sistemas_rpg import SISTEMAS_DISPONIVEIS, resolver_alias, listar_por_categoria, buscar_sistema

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Cliente da API Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Diretório para salvar dados
DATA_DIR = Path("bot_data")
DATA_DIR.mkdir(exist_ok=True)

# Arquivos de dados
FICHAS_FILE = DATA_DIR / "fichas_personagens.json"
SISTEMAS_FILE = DATA_DIR / "sistemas_rpg.json"
SESSOES_FILE = DATA_DIR / "sessoes_ativas.json"

# Histórico de conversas por canal (não salvo - muito grande)
conversation_history = {}

# Sistema de RPG atual do canal
sistemas_rpg = {}

# Fichas de personagens salvas
fichas_personagens = {}

# Sessões ativas
sessoes_ativas = {}

# Função para carregar dados
def carregar_dados():
    """Carrega dados salvos dos arquivos JSON"""
    global fichas_personagens, sistemas_rpg, sessoes_ativas
    
    # Carrega fichas
    if FICHAS_FILE.exists():
        try:
            with open(FICHAS_FILE, 'r', encoding='utf-8') as f:
                fichas_personagens = json.load(f)
            print(f"✅ {len(fichas_personagens)} fichas carregadas!")
        except Exception as e:
            print(f"⚠️ Erro ao carregar fichas: {e}")
            fichas_personagens = {}
    
    # Carrega sistemas
    if SISTEMAS_FILE.exists():
        try:
            with open(SISTEMAS_FILE, 'r', encoding='utf-8') as f:
                # Converte chaves de volta para int
                sistemas_data = json.load(f)
                sistemas_rpg = {int(k): v for k, v in sistemas_data.items()}
            print(f"✅ Sistemas de {len(sistemas_rpg)} canais carregados!")
        except Exception as e:
            print(f"⚠️ Erro ao carregar sistemas: {e}")
            sistemas_rpg = {}
    
    # Carrega sessões
    if SESSOES_FILE.exists():
        try:
            with open(SESSOES_FILE, 'r', encoding='utf-8') as f:
                sessoes_data = json.load(f)
                sessoes_ativas = {int(k): v for k, v in sessoes_data.items()}
            print(f"✅ {len(sessoes_ativas)} sessões ativas carregadas!")
        except Exception as e:
            print(f"⚠️ Erro ao carregar sessões: {e}")
            sessoes_ativas = {}

# Função para salvar dados
def salvar_dados():
    """Salva dados nos arquivos JSON"""
    try:
        # Salva fichas
        with open(FICHAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(fichas_personagens, f, ensure_ascii=False, indent=2)
        
        # Salva sistemas (converte chaves int para str para JSON)
        sistemas_data = {str(k): v for k, v in sistemas_rpg.items()}
        with open(SISTEMAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sistemas_data, f, ensure_ascii=False, indent=2)
        
        # Salva sessões
        sessoes_data = {str(k): v for k, v in sessoes_ativas.items()}
        with open(SESSOES_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessoes_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        return False

# Auto-save a cada 5 minutos
async def auto_save():
    """Salva dados automaticamente a cada 5 minutos"""
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(300)  # 5 minutos
        if salvar_dados():
            print("💾 Auto-save realizado!")

def get_system_prompt(sistema="dnd5e"):
    sistema_info = SISTEMAS_DISPONIVEIS.get(sistema, SISTEMAS_DISPONIVEIS["dnd5e"])
    return f"""Você é um Mestre de RPG especialista em {sistema_info['nome']}. Suas responsabilidades incluem:

1. **Narração Imersiva**: Crie descrições vívidas e envolventes de cenários, NPCs e situações
2. **Conhecimento de Regras**: Domine as regras de {sistema_info['nome']} e ajude os jogadores
3. **Criação de Conteúdo**: Gere NPCs, monstros, itens e missões balanceadas
4. **Assistência ao Mestre**: Auxilie na preparação e condução de sessões

**Atributos do sistema**: {', '.join(sistema_info['atributos'])}
**Classes disponíveis**: {', '.join(sistema_info['classes'][:10])}

Seja criativo, justo e sempre focado em proporcionar uma experiência divertida. Use linguagem clara e direta.
Quando criar fichas ou NPCs, forneça informações completas e balanceadas para o nível apropriado."""

def inicializar_historico(channel_id):
    sistema = sistemas_rpg.get(channel_id, "dnd5e")
    if channel_id not in conversation_history:
        conversation_history[channel_id] = [
            {"role": "system", "content": get_system_prompt(sistema)}
        ]

async def chamar_groq(mensagens, max_tokens=1000):
    """Função auxiliar para chamar a API Groq"""
    try:
        chat_completion = client.chat.completions.create(
            messages=mensagens,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=max_tokens,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Erro ao chamar API: {str(e)}"

@bot.event
async def on_ready():
    print(f'🎲 {bot.user} está online!')
    print(f'Conectado a {len(bot.guilds)} servidor(es)')
    
    # Carrega dados salvos
    carregar_dados()
    
    # Inicia auto-save em background
    bot.loop.create_task(auto_save())
    print("💾 Sistema de auto-save ativado!")

# ---------------- Comandos ---------------- #

@bot.command(name='sistema')
async def definir_sistema(ctx, sistema: str = None):
    """Define o sistema de RPG do canal"""
    if sistema is None:
        sistema_atual = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        
        # Conta fichas do usuário por sistema
        fichas_usuario = {k: f for k, f in fichas_personagens.items() if f["autor"] == ctx.author.id}
        sistemas_fichas = {}
        for ficha in fichas_usuario.values():
            s = ficha.get('sistema', 'dnd5e')
            sistemas_fichas[s] = sistemas_fichas.get(s, 0) + 1
        
        info_fichas = ""
        if sistemas_fichas:
            info_fichas = "\n\n**🗂️ Suas fichas por sistema:**\n" + "\n".join([
                f"• {SISTEMAS_DISPONIVEIS[s]['nome']}: {c} ficha(s)" 
                for s, c in sistemas_fichas.items()
            ])
        
        embed = discord.Embed(
            title="🎲 Sistema de RPG Atual",
            description=f"**Sistema atual deste canal**: {SISTEMAS_DISPONIVEIS[sistema_atual]['nome']}\n\n"
                       f"**Uso**: `!sistema <código>`\n"
                       f"**Ver todos**: `!sistemas`\n"
                       f"**Buscar**: `!buscarsistema <nome>`\n"
                       f"**Detalhes**: `!infosistema <código>`{info_fichas}",
            color=discord.Color.purple()
        )
        embed.set_footer(text="💡 Mudar sistema não afeta fichas já criadas")
        await ctx.send(embed=embed)
        return

    sistema = resolver_alias(sistema.lower())
    if sistema not in SISTEMAS_DISPONIVEIS:
        await ctx.send(f"❌ Sistema '{sistema}' não encontrado! Use `!sistemas` para ver os disponíveis.")
        return

    sistema_anterior = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    sistemas_rpg[ctx.channel.id] = sistema
    conversation_history[ctx.channel.id] = [
        {"role": "system", "content": get_system_prompt(sistema)}
    ]
    
    # Salva alteração
    salvar_dados()
    
    sistema_info = SISTEMAS_DISPONIVEIS[sistema]
    embed = discord.Embed(
        title=f"✅ Sistema alterado: {sistema_info['nome']}",
        description=f"O bot agora está configurado para **{sistema_info['nome']}**!",
        color=discord.Color.green()
    )
    embed.add_field(name="📖 Categoria", value=sistema_info['categoria'], inline=True)
    embed.add_field(name="🎲 Dados", value=", ".join(sistema_info['dados']), inline=True)
    embed.add_field(name="📈 Nível Max", value=str(sistema_info['nivel_max']), inline=True)
    
    classes_texto = ", ".join(sistema_info['classes'][:5])
    if len(sistema_info['classes']) > 5:
        classes_texto += f" (+{len(sistema_info['classes']) - 5} mais)"
    embed.add_field(name="⚔️ Classes", value=classes_texto, inline=False)
    
    # Aviso sobre o que muda e o que não muda
    embed.add_field(
        name="📋 O que isso afeta:",
        value=(
            f"✅ Comandos: `!monstro`, `!regra`, `!mestre`, `!npc`, etc\n"
            f"✅ Novas fichas criadas com `!ficha` e `!criarficha`\n"
            f"✅ Contexto da IA para este canal\n"
            f"❌ **Não afeta** fichas já criadas (elas mantêm o sistema original)"
        ),
        inline=False
    )
    
    if sistema_anterior != sistema:
        embed.add_field(
            name="💡 Dica",
            value=f"Use `!converterficha {sistema} <nome>` para converter fichas existentes!",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='sistemas', aliases=['rpgs', 'listarsistemas'])
async def listar_sistemas(ctx):
    """Lista todos os sistemas de RPG disponíveis, agrupados por categoria."""
    try:
        sistemas_por_categoria = listar_por_categoria()

        embeds = []
        embed = discord.Embed(
            title="📚 Sistemas de RPG Disponíveis (50+)",
            description=(
                "Use `!sistema <código>` para mudar o sistema.\n"
                "Use `!infosistema <código>` para ver detalhes.\n"
                "Use `!buscarsistema <nome>` para buscar.\n\n"
                "🔹 Dica: Muitos sistemas disponíveis! A lista será dividida automaticamente."
            ),
            color=discord.Color.dark_teal()
        )

        for categoria, sistemas in sistemas_por_categoria.items():
            # Monta o texto da categoria
            sistemas_friendly = "\n".join([f"• **{nome}** (`{codigo}`)" for codigo, nome in sistemas])
            
            # Divide o conteúdo se for muito grande
            if len(sistemas_friendly) > 1024:
                chunks = [sistemas[i:i + 10] for i in range(0, len(sistemas), 10)]
                for i, chunk in enumerate(chunks):
                    chunk_text = "\n".join([f"• **{nome}** (`{codigo}`)" for codigo, nome in chunk])
                    embed.add_field(
                        name=f"--- {categoria} (Parte {i + 1}) ---",
                        value=chunk_text,
                        inline=False
                    )
                    # Se atingir o limite de campos, armazena e reinicia
                    if len(embed.fields) >= 25:
                        embeds.append(embed)
                        embed = discord.Embed(color=discord.Color.dark_teal())
            else:
                embed.add_field(
                    name=f"--- {categoria} ({len(sistemas)}) ---",
                    value=sistemas_friendly,
                    inline=False
                )
                if len(embed.fields) >= 25:
                    embeds.append(embed)
                    embed = discord.Embed(color=discord.Color.dark_teal())

        # Adiciona o último embed se houver campos restantes
        if len(embed.fields) > 0:
            embed.set_footer(text="Total: 50+ sistemas de RPG! 🎲")
            embeds.append(embed)

        # Envia todos os embeds
        for e in embeds:
            await ctx.send(embed=e)

    except Exception as e:
        await ctx.send(f"❌ Erro ao listar sistemas: {type(e).__name__}: {str(e)}")
        print(f"Erro no comando !sistemas: {e}")

@bot.command(name='buscarsistema')
async def buscar_sistema_cmd(ctx, *, busca: str = None):
    """Busca sistemas de RPG por nome"""
    if not busca:
        await ctx.send("❌ Forneça um termo de busca! Exemplo: `!buscarsistema vampire`")
        return
    
    busca_lower = busca.lower()
    resultados = []
    
    for codigo, info in SISTEMAS_DISPONIVEIS.items():
        if busca_lower in info['nome'].lower() or busca_lower in codigo.lower():
            resultados.append(f"• **{info['nome']}** (`{codigo}`) - {info['categoria']}")
    
    if not resultados:
        await ctx.send(f"❌ Nenhum sistema encontrado com '{busca}'")
        return
    
    embed = discord.Embed(
        title=f"🔍 Busca: '{busca}'",
        description="\n".join(resultados[:20]),  # Limite 20 resultados
        color=discord.Color.blue()
    )
    embed.set_footer(text="Use !infosistema <código> para ver detalhes completos")
    await ctx.send(embed=embed)

@bot.command(name='infosistema')
async def info_sistema(ctx, sistema_codigo: str = None):
    """Mostra informações detalhadas de um sistema"""
    if not sistema_codigo:
        # Mostra info do sistema atual do canal
        sistema_codigo = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    sistema_codigo = resolver_alias(sistema_codigo.lower())
    
    if sistema_codigo not in SISTEMAS_DISPONIVEIS:
        await ctx.send(f"❌ Sistema '{sistema_codigo}' não encontrado! Use `!sistemas` para ver todos.")
        return
    
    info = SISTEMAS_DISPONIVEIS[sistema_codigo]
    
    embed = discord.Embed(
        title=f"📖 {info['nome']}",
        description=f"**Categoria:** {info['categoria']}",
        color=discord.Color.purple()
    )
    
    embed.add_field(name="🎲 Dados", value=", ".join(info['dados']), inline=False)
    embed.add_field(name="📊 Atributos", value=", ".join(info['atributos']), inline=False)
    
    if info['classes']:
        classes_texto = ", ".join(info['classes'][:10])
        if len(info['classes']) > 10:
            classes_texto += f" (+{len(info['classes']) - 10} mais)"
        embed.add_field(name="⚔️ Classes/Tipos", value=classes_texto, inline=False)
    
    embed.add_field(name="🔧 Mecânicas", value=info['mecanicas'], inline=False)
    embed.add_field(name="📈 Nível Máximo", value=str(info['nivel_max']), inline=True)
    embed.add_field(name="🔑 Código", value=f"`{sistema_codigo}`", inline=True)
    
    embed.set_footer(text=f"Use !sistema {sistema_codigo} para mudar para este sistema")
    await ctx.send(embed=embed)

@bot.command(name='rolar', aliases=['r', 'roll'])
async def rolar_dados(ctx, *, dados: str = None):
    """Rola dados de RPG com suporte a modificadores"""
    if not dados:
        await ctx.send("❌ Formato inválido! Exemplos: `!rolar 1d20`, `!rolar 2d6+3`, `!rolar 4d6k3 Ataque`")
        return

    # Separa descrição do comando
    partes = dados.split(maxsplit=1)
    formula = partes[0].lower()
    descricao = partes[1] if len(partes) > 1 else ""

    try:
        # Parse da fórmula: NdX+MOD ou NdXkY (keep highest)
        padrao_keep = r'(\d+)d(\d+)k(\d+)([+-]\d+)?'
        padrao_normal = r'(\d+)d(\d+)([+-]\d+)?'
        
        resultado_keep = re.match(padrao_keep, formula)
        resultado_normal = re.match(padrao_normal, formula)
        
        if resultado_keep:
            num_dados = int(resultado_keep.group(1))
            lados = int(resultado_keep.group(2))
            keep = int(resultado_keep.group(3))
            modificador = int(resultado_keep.group(4)) if resultado_keep.group(4) else 0
            
            if num_dados > 100 or lados > 1000:
                await ctx.send("❌ Limite: 100 dados de até 1000 lados!")
                return
            
            rolagens = sorted([random.randint(1, lados) for _ in range(num_dados)], reverse=True)
            mantidos = rolagens[:keep]
            descartados = rolagens[keep:]
            total = sum(mantidos) + modificador
            
            resultado_texto = f"**{ctx.author.display_name}** rolou `{formula}`"
            if descricao:
                resultado_texto += f" para **{descricao}**"
            
            embed = discord.Embed(title="🎲 Rolagem de Dados", description=resultado_texto, color=discord.Color.blue())
            embed.add_field(name="Mantidos", value=f"{mantidos} = {sum(mantidos)}", inline=False)
            if descartados:
                embed.add_field(name="Descartados", value=f"{descartados}", inline=False)
            if modificador:
                embed.add_field(name="Modificador", value=f"{modificador:+d}", inline=False)
            embed.add_field(name="🎯 Total", value=f"**{total}**", inline=False)
            
        elif resultado_normal:
            num_dados = int(resultado_normal.group(1))
            lados = int(resultado_normal.group(2))
            modificador = int(resultado_normal.group(3)) if resultado_normal.group(3) else 0
            
            if num_dados > 100 or lados > 1000:
                await ctx.send("❌ Limite: 100 dados de até 1000 lados!")
                return
            
            rolagens = [random.randint(1, lados) for _ in range(num_dados)]
            soma = sum(rolagens)
            total = soma + modificador
            
            resultado_texto = f"**{ctx.author.display_name}** rolou `{formula}`"
            if descricao:
                resultado_texto += f" para **{descricao}**"
            
            embed = discord.Embed(title="🎲 Rolagem de Dados", description=resultado_texto, color=discord.Color.blue())
            
            if num_dados <= 20:
                embed.add_field(name="Resultados", value=f"{rolagens}", inline=False)
            embed.add_field(name="Soma dos dados", value=f"{soma}", inline=True)
            if modificador:
                embed.add_field(name="Modificador", value=f"{modificador:+d}", inline=True)
            embed.add_field(name="🎯 Total", value=f"**{total}**", inline=False)
            
            # Críticos em d20
            if lados == 20 and num_dados == 1:
                if rolagens[0] == 20:
                    embed.set_footer(text="🌟 CRÍTICO! 🌟")
                elif rolagens[0] == 1:
                    embed.set_footer(text="💀 FALHA CRÍTICA! 💀")
        else:
            await ctx.send("❌ Formato inválido! Use: `NdX`, `NdX+Y`, ou `NdXkY` (ex: `1d20`, `2d6+3`, `4d6k3`)")
            return
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao processar rolagem: {str(e)}")

@bot.command(name='ficha')
async def criar_ficha(ctx, *, nome_personagem: str = None):
    """Cria uma ficha de personagem completa"""
    if not nome_personagem:
        await ctx.send("❌ Forneça um nome para o personagem! Exemplo: `!ficha Thorin Escudo-de-Ferro`")
        return
    
    await ctx.send(f"🎭 Criando ficha para **{nome_personagem}**... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    sistema_info = SISTEMAS_DISPONIVEIS[sistema]
    
    prompt = f"""Crie uma ficha de personagem COMPLETA para {sistema_info['nome']} com o nome "{nome_personagem}".

Inclua obrigatoriamente:
- Nome, Raça, Classe e Nível (3-5)
- Todos os atributos: {', '.join(sistema_info['atributos'])}
- Pontos de Vida, CA (Classe de Armadura)
- Proficiências e perícias principais
- 2-3 equipamentos importantes
- Uma característica de personalidade
- Background breve (2-3 linhas)

Seja criativo mas balanceado! Formato organizado e fácil de ler."""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1500)
    
    # Salva ficha
    chave_ficha = f"{ctx.author.id}_{nome_personagem.lower().replace(' ', '_')}"
    fichas_personagens[chave_ficha] = {
        "nome": nome_personagem,
        "sistema": sistema,
        "conteudo": resposta,
        "autor": ctx.author.id
    }
    
    # Salva no arquivo
    salvar_dados()
    
    embed = discord.Embed(
        title=f"📜 Ficha: {nome_personagem}",
        description=resposta[:4000],  # Limite do Discord
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Sistema: {sistema_info['nome']} | Criada por {ctx.author.display_name}")
    
    await ctx.send(embed=embed)

@bot.command(name='verficha')
async def ver_ficha(ctx, *, nome_personagem: str = None):
    """Mostra uma ficha salva"""
    if not nome_personagem:
        # Lista todas as fichas do usuário
        fichas_usuario = [f for k, f in fichas_personagens.items() if f["autor"] == ctx.author.id]
        if not fichas_usuario:
            await ctx.send("❌ Você não tem fichas salvas! Use `!ficha <nome>` para criar.")
            return
        
        lista = "\n".join([f"• **{f['nome']}** ({SISTEMAS_DISPONIVEIS[f['sistema']]['nome']})" for f in fichas_usuario])
        embed = discord.Embed(title="📚 Suas Fichas", description=lista, color=discord.Color.blue())
        embed.set_footer(text="Use !verficha <nome> para ver detalhes")
        await ctx.send(embed=embed)
        return
    
    chave_ficha = f"{ctx.author.id}_{nome_personagem.lower().replace(' ', '_')}"
    
    if chave_ficha not in fichas_personagens:
        await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada!")
        return
    
    ficha = fichas_personagens[chave_ficha]
    embed = discord.Embed(
        title=f"📜 Ficha: {ficha['nome']}",
        description=ficha['conteudo'][:4000],
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[ficha['sistema']]['nome']}")
    await ctx.send(embed=embed)

@bot.command(name='criarficha')
async def criar_ficha_interativa(ctx):
    """Cria uma ficha através de perguntas interativas"""
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    sistema_info = SISTEMAS_DISPONIVEIS[sistema]
    
    embed_intro = discord.Embed(
        title="📝 Criação de Ficha Interativa",
        description=f"Vou fazer algumas perguntas para criar sua ficha de **{sistema_info['nome']}**.\n\nVocê tem **60 segundos** para responder cada pergunta.\nDigite `cancelar` a qualquer momento para abortar.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_intro)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    respostas = {}
    
    # Lista de perguntas baseadas no sistema
    if sistema == "dnd5e" or sistema == "dnd35" or sistema == "pathfinder1e" or sistema == "pathfinder" or sistema == "13thage":
        perguntas = [
            ("nome", "📛 Qual o **nome** do seu personagem?"),
            ("raca", "🧬 Qual a **raça**? (Ex: Humano, Elfo, Anão, etc)"),
            ("classe", f"⚔️ Qual a **classe**?\nDisponíveis: {', '.join(sistema_info['classes'][:8])}..."),
            ("nivel", "📊 Qual o **nível**? (1-20)"),
            ("antecedente", "📖 Qual o **antecedente/background**? (Ex: Soldado, Eremita, Nobre)"),
            ("forca", "💪 **Força** (atributo):"),
            ("destreza", "🎯 **Destreza** (atributo):"),
            ("constituicao", "❤️ **Constituição** (atributo):"),
            ("inteligencia", "🧠 **Inteligência** (atributo):"),
            ("sabedoria", "🦉 **Sabedoria** (atributo):"),
            ("carisma", "✨ **Carisma** (atributo):"),
            ("personalidade", "🎭 Descreva a **personalidade** em 1-2 linhas:")
        ]
    elif sistema == "cthulhu":
        perguntas = [
            ("nome", "📛 Qual o **nome** do investigador?"),
            ("ocupacao", "💼 Qual a **ocupação**? (Ex: Detetive, Jornalista, Professor)"),
            ("idade", "📅 Qual a **idade**?"),
            ("for", "💪 **FOR** (Força):"),
            ("con", "❤️ **CON** (Constituição):"),
            ("tam", "📏 **TAM** (Tamanho):"),
            ("des", "🎯 **DES** (Destreza):"),
            ("int", "🧠 **INT** (Inteligência):"),
            ("pod", "🔮 **POD** (Poder):"),
            ("edu", "📚 **EDU** (Educação):"),
            ("personalidade", "🎭 Descreva a **personalidade** em 1-2 linhas:")
        ]
    else:
        perguntas = [
            ("nome", "📛 Qual o **nome** do seu personagem?"),
            ("tipo", f"🧬 Qual o **tipo/classe**?\nDisponíveis: {', '.join(sistema_info['classes'][:8])}..."),
            ("conceito", "💡 Qual o **conceito** do personagem? (1 linha)"),
            ("personalidade", "🎭 Descreva a **personalidade** em 1-2 linhas:")
        ]
    
    try:
        for chave, pergunta in perguntas:
            embed_pergunta = discord.Embed(
                title="❓ Pergunta",
                description=pergunta,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed_pergunta)
            
            try:
                resposta = await bot.wait_for('message', timeout=60.0, check=check)
                
                if resposta.content.lower() == 'cancelar':
                    await ctx.send("❌ Criação de ficha cancelada!")
                    return
                
                respostas[chave] = resposta.content
                
            except asyncio.TimeoutError:
                await ctx.send("⏰ Tempo esgotado! Criação cancelada.")
                return
        
        # Processa as respostas e cria a ficha
        await ctx.send("⏳ Processando sua ficha...")
        
        # Monta o prompt para a IA finalizar a ficha
        respostas_texto = "\n".join([f"- {k.title()}: {v}" for k, v in respostas.items()])
        
        prompt = f"""Com base nas informações fornecidas, crie uma ficha COMPLETA e detalhada para {sistema_info['nome']}:

{respostas_texto}

Complete a ficha com:
- Calcule modificadores de atributos
- Adicione Pontos de Vida e CA apropriados
- Liste proficiências relevantes para a classe/ocupação
- Adicione 3-4 equipamentos iniciais apropriados
- Expanda o background (3-4 linhas)
- Adicione traços de personalidade adicionais

Formate de forma clara e organizada!"""

        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
            {"role": "user", "content": prompt}
        ]
        
        ficha_completa = await chamar_groq(mensagens, max_tokens=2000)
        
        # Salva a ficha
        nome_personagem = respostas.get('nome', 'Personagem')
        chave_ficha = f"{ctx.author.id}_{nome_personagem.lower().replace(' ', '_')}"
        fichas_personagens[chave_ficha] = {
            "nome": nome_personagem,
            "sistema": sistema,
            "conteudo": ficha_completa,
            "autor": ctx.author.id,
            "respostas_originais": respostas
        }
        
        # Salva no arquivo
        salvar_dados()
        
        embed_resultado = discord.Embed(
            title=f"📜 Ficha Criada: {nome_personagem}",
            description=ficha_completa[:4000],
            color=discord.Color.gold()
        )
        embed_resultado.set_footer(text=f"Sistema: {sistema_info['nome']} | Use !editarficha {nome_personagem} para editar")
        await ctx.send(embed=embed_resultado)
        
    except Exception as e:
        await ctx.send(f"❌ Erro durante a criação: {str(e)}")

@bot.command(name='editarficha')
async def editar_ficha(ctx, *, nome_personagem: str = None):
    """Edita uma ficha existente"""
    if not nome_personagem:
        await ctx.send("❌ Forneça o nome da ficha! Exemplo: `!editarficha Thorin`")
        return
    
    chave_ficha = f"{ctx.author.id}_{nome_personagem.lower().replace(' ', '_')}"
    
    if chave_ficha not in fichas_personagens:
        await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada! Use `!verficha` para ver suas fichas.")
        return
    
    ficha = fichas_personagens[chave_ficha]
    
    embed_menu = discord.Embed(
        title=f"✏️ Editar Ficha: {ficha['nome']}",
        description="O que você deseja fazer?\n\n"
                    "**1️⃣** - Editar atributos\n"
                    "**2️⃣** - Editar nível/classe\n"
                    "**3️⃣** - Editar equipamentos\n"
                    "**4️⃣** - Editar personalidade/background\n"
                    "**5️⃣** - Adicionar anotações livres\n"
                    "**6️⃣** - Reescrever ficha completa\n"
                    "**❌** - Cancelar\n\n"
                    "Digite o número da opção:",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed_menu)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        opcao_msg = await bot.wait_for('message', timeout=60.0, check=check)
        opcao = opcao_msg.content.strip()
        
        if opcao == '❌' or opcao.lower() == 'cancelar':
            await ctx.send("❌ Edição cancelada!")
            return
        
        sistema = ficha['sistema']
        
        if opcao == '1':
            await ctx.send("📊 Digite os novos valores dos atributos no formato:\n`Força: 16, Destreza: 14, Constituição: 15` (etc)")
            
        elif opcao == '2':
            await ctx.send("⚔️ Digite o novo nível e/ou classe:\nEx: `Nível 5` ou `Guerreiro Nível 7`")
            
        elif opcao == '3':
            await ctx.send("🎒 Digite os equipamentos que deseja adicionar/modificar:\nEx: `Espada Longa +1, Armadura de Couro, Poção de Cura`")
            
        elif opcao == '4':
            await ctx.send("🎭 Digite a nova personalidade ou informações de background:")
            
        elif opcao == '5':
            await ctx.send("📝 Digite suas anotações livres (XP ganho, itens adquiridos, relacionamentos, etc):")
            
        elif opcao == '6':
            await ctx.send("🔄 Digite como você quer que a ficha seja reescrita ou 'completo' para uma revisão geral:")
            
        else:
            await ctx.send("❌ Opção inválida!")
            return
        
        # Aguarda a resposta
        try:
            resposta = await bot.wait_for('message', timeout=120.0, check=check)
            edicao = resposta.content
            
            await ctx.send("⏳ Processando edição...")
            
            # Monta prompt para IA processar a edição
            prompt = f"""Atualize a seguinte ficha de personagem de {SISTEMAS_DISPONIVEIS[sistema]['nome']}:

FICHA ATUAL:
{ficha['conteudo']}

ALTERAÇÃO SOLICITADA (tipo {opcao}):
{edicao}

Reescreva a ficha COMPLETA incorporando as mudanças solicitadas. Mantenha o que não foi alterado e ajuste o que for necessário para manter consistência."""

            mensagens = [
                {"role": "system", "content": get_system_prompt(sistema)},
                {"role": "user", "content": prompt}
            ]
            
            ficha_atualizada = await chamar_groq(mensagens, max_tokens=2000)
            
            # Atualiza a ficha
            fichas_personagens[chave_ficha]['conteudo'] = ficha_atualizada
            
            # Salva alteração
            salvar_dados()
            
            embed_resultado = discord.Embed(
                title=f"✅ Ficha Atualizada: {ficha['nome']}",
                description=ficha_atualizada[:4000],
                color=discord.Color.green()
            )
            embed_resultado.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}")
            await ctx.send(embed=embed_resultado)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado! Edição cancelada.")
            
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo esgotado! Edição cancelada.")
    except Exception as e:
        await ctx.send(f"❌ Erro durante a edição: {str(e)}")

@bot.command(name='deletarficha')
async def deletar_ficha(ctx, *, nome_personagem: str = None):
    """Deleta uma ficha salva"""
    if not nome_personagem:
        await ctx.send("❌ Forneça o nome da ficha! Exemplo: `!deletarficha Thorin`")
        return
    
    chave_ficha = f"{ctx.author.id}_{nome_personagem.lower().replace(' ', '_')}"
    
    if chave_ficha not in fichas_personagens:
        await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada!")
        return
    
    # Confirmação
    embed_confirma = discord.Embed(
        title="⚠️ Confirmar Exclusão",
        description=f"Tem certeza que deseja deletar a ficha **{nome_personagem}**?\n\nDigite `sim` para confirmar ou `não` para cancelar.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed_confirma)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['sim', 'não', 'nao']
    
    try:
        confirmacao = await bot.wait_for('message', timeout=30.0, check=check)
        
        if confirmacao.content.lower() == 'sim':
            del fichas_personagens[chave_ficha]
            salvar_dados()
            await ctx.send(f"✅ Ficha **{nome_personagem}** deletada com sucesso!")
        else:
            await ctx.send("❌ Exclusão cancelada!")
            
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo esgotado! Exclusão cancelada.")

@bot.command(name='minhasfichas')
async def minhas_fichas(ctx, filtro_sistema: str = None):
    """Lista suas fichas com mais detalhes, opcionalmente filtradas por sistema"""
    fichas_usuario = {k: f for k, f in fichas_personagens.items() if f["autor"] == ctx.author.id}
    
    if not fichas_usuario:
        await ctx.send("❌ Você não tem fichas criadas! Use `!ficha <nome>` ou `!criarficha` para criar.")
        return
    
    # Filtra por sistema se especificado
    if filtro_sistema:
        filtro_sistema = resolver_alias(filtro_sistema.lower())
        if filtro_sistema not in SISTEMAS_DISPONIVEIS:
            await ctx.send(f"❌ Sistema '{filtro_sistema}' não encontrado!")
            return
        fichas_usuario = {k: f for k, f in fichas_usuario.items() if f.get('sistema', 'dnd5e') == filtro_sistema}
    
    if not fichas_usuario:
        sistema_nome = SISTEMAS_DISPONIVEIS[filtro_sistema]['nome']
        await ctx.send(f"❌ Você não tem fichas de {sistema_nome}!")
        return
    
    # Organiza por sistema
    fichas_por_sistema = {}
    for ficha in fichas_usuario.values():
        sistema = ficha.get('sistema', 'dnd5e')
        if sistema not in fichas_por_sistema:
            fichas_por_sistema[sistema] = []
        fichas_por_sistema[sistema].append(ficha)
    
    embed = discord.Embed(
        title=f"📚 Suas Fichas de Personagem",
        description=f"Total: **{len(fichas_usuario)}** ficha(s)",
        color=discord.Color.blue()
    )
    
    for sistema, fichas in fichas_por_sistema.items():
        sistema_info = SISTEMAS_DISPONIVEIS[sistema]
        lista = "\n".join([
            f"• **{f['nome']}**{' *(convertida)*' if 'convertida_de' in f else ''}"
            for f in fichas
        ])
        
        embed.add_field(
            name=f"🎲 {sistema_info['nome']} ({len(fichas)})",
            value=lista,
            inline=False
        )
    
    embed.set_footer(text="Use !verficha <nome> para ver detalhes • !converterficha <sistema> <nome> para converter")
    await ctx.send(embed=embed)

@bot.command(name='converterficha')
async def converter_ficha(ctx, novo_sistema: str, *, nome_personagem: str = None):
    """Converte uma ficha para outro sistema de RPG"""
    if not nome_personagem:
        await ctx.send("❌ Forneça o sistema e nome da ficha! Exemplo: `!converterficha pathfinder Thorin`")
        return
    
    novo_sistema = resolver_alias(novo_sistema.lower())
    if novo_sistema not in SISTEMAS_DISPONIVEIS:
        await ctx.send(f"❌ Sistema '{novo_sistema}' não encontrado! Use `!sistemas` para ver disponíveis.")
        return
    
    import re
    chave_ficha = f"{ctx.author.id}_" + re.sub(r'[^a-z0-9_]+', '_', nome_personagem.lower())

    if chave_ficha not in fichas_personagens:
        await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada!")
        return
    
    ficha = fichas_personagens[chave_ficha]
    sistema_atual = ficha.get('sistema', 'dnd5e')
    
    if sistema_atual == novo_sistema:
        await ctx.send(f"⚠️ A ficha já está em {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}!")
        return
    
    await ctx.send(f"🔄 Convertendo **{ficha['nome']}** de {SISTEMAS_DISPONIVEIS[sistema_atual]['nome']} para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}... ⏳")
    
    prompt = f"""Converta a seguinte ficha de personagem de {SISTEMAS_DISPONIVEIS[sistema_atual]['nome']} para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}.

FICHA ORIGINAL ({SISTEMAS_DISPONIVEIS[sistema_atual]['nome']}):
{ficha['conteudo']}

Crie uma ficha COMPLETA e EQUIVALENTE em {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}:
- Mantenha o mesmo conceito, personalidade e história
- Converta atributos para o novo sistema
- Ajuste classes/habilidades de forma equivalente
- Mantenha o mesmo nível de poder
- Use as regras corretas de {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}

Formato organizado e fácil de ler!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(novo_sistema)},
        {"role": "user", "content": prompt}
    ]
    
    try:
        ficha_convertida = await chamar_groq(mensagens, max_tokens=2000)
        
        # Cria nova ficha com sufixo do sistema
        novo_nome = f"{ficha['nome']} ({SISTEMAS_DISPONIVEIS[novo_sistema]['nome'][:10]})"
        chave_nova = f"{ctx.author.id}_{novo_nome.lower().replace(' ', '_').replace('(', '').replace(')', '')}"
        
        fichas_personagens[chave_nova] = {
            "nome": novo_nome,
            "sistema": novo_sistema,
            "conteudo": ficha_convertida,
            "autor": ctx.author.id,
            "convertida_de": sistema_atual
        }
        
        salvar_dados()
        
        embed = discord.Embed(
            title=f"✅ Ficha Convertida!",
            description=f"**{ficha['nome']}** foi convertida para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}!\n\n"
                       f"Nova ficha salva como: **{novo_nome}**\n\n"
                       f"{ficha_convertida[:3000]}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Ficha original mantida • Use !verficha para ver")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao converter ficha: {str(e)}")

@bot.command(name='exportarficha')
async def exportar_ficha(ctx, *, nome_personagem: str = None):
    """Exporta uma ficha como arquivo JSON"""
    if not nome_personagem:
        await ctx.send("❌ Forneça o nome da ficha! Exemplo: `!exportarficha Thorin`")
        return
    
    chave_ficha = f"{ctx.author.id}_{nome_personagem.lower().replace(' ', '_')}"
    
    if chave_ficha not in fichas_personagens:
        await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada!")
        return
    
    ficha = fichas_personagens[chave_ficha]
    
    # Cria arquivo temporário
    arquivo_nome = f"{nome_personagem.replace(' ', '_')}.json"
    arquivo_path = DATA_DIR / arquivo_nome
    
    try:
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            json.dump(ficha, f, ensure_ascii=False, indent=2)
        
        await ctx.send(
            f"📤 Exportando ficha **{nome_personagem}**...",
            file=discord.File(arquivo_path)
        )
        
        # Remove arquivo temporário
        arquivo_path.unlink()
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao exportar: {str(e)}")

@bot.command(name='npc')
async def gerar_npc(ctx, *, descricao: str = None):
    """Gera um NPC rápido"""
    if not descricao:
        descricao = "um NPC genérico"
    
    await ctx.send(f"🎭 Gerando NPC: {descricao}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie um NPC rápido: {descricao}

Inclua:
- Nome e aparência (2-3 linhas)
- Personalidade marcante (1 linha)
- Uma motivação ou segredo
- 1-2 stats importantes para combate/interação (se relevante)

Seja conciso mas memorável!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=800)
    
    embed = discord.Embed(
        title=f"🎭 NPC Gerado",
        description=resposta,
        color=discord.Color.purple()
    )
    embed.set_footer(text=f"Solicitado por {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name='monstro')
async def buscar_monstro(ctx, *, nome: str = None):
    """Busca ou gera stats de monstros"""
    if not nome:
        await ctx.send("❌ Forneça o nome do monstro. Exemplo: `!monstro Dragão Vermelho`")
        return
    
    await ctx.send(f"🐉 Buscando informações sobre: {nome}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Forneça o bloco de estatísticas do monstro "{nome}" para {SISTEMAS_DISPONIVEIS[sistema]['nome']}.

Inclua:
- Tipo, tamanho, alinhamento
- CA, PV, Deslocamento
- Atributos
- Ataques e habilidades especiais
- Desafio (CR/ND) apropriado
- Breve descrição tática

Se o monstro não existir oficialmente, crie uma versão balanceada e interessante!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1200)
    
    embed = discord.Embed(
        title=f"🐉 {nome}",
        description=resposta[:4000],
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}")
    await ctx.send(embed=embed)

@bot.command(name='cena')
async def descrever_cena(ctx, *, descricao: str = None):
    """Descreve uma cena de forma dramática"""
    if not descricao:
        await ctx.send("❌ Forneça uma descrição da cena. Exemplo: `!cena taverna em ruínas`")
        return
    
    await ctx.send(f"🎬 Narrando cena... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Descreva de forma DRAMÁTICA e IMERSIVA a seguinte cena: {descricao}

Use:
- Linguagem sensorial (visão, sons, cheiros)
- Detalhes atmosféricos
- 3-5 parágrafos curtos
- Tom apropriado ao cenário

Seja cinematográfico e envolvente!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1000)
    
    embed = discord.Embed(
        title=f"🎬 {descricao.title()}",
        description=resposta,
        color=discord.Color.dark_blue()
    )
    await ctx.send(embed=embed)

@bot.command(name='plot')
async def gerar_plot(ctx, *, tema: str = None):
    """Gera ideias de missão/aventura"""
    if not tema:
        tema = "aventura genérica"
    
    await ctx.send(f"📖 Gerando plot: {tema}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie uma ideia de missão/aventura com o tema: {tema}

Inclua:
- **Gancho**: Como os jogadores se envolvem (2-3 linhas)
- **Objetivo Principal**: O que precisam fazer
- **Complicação**: Um obstáculo ou reviravolta
- **Recompensa**: O que ganham ao completar
- **3 Encontros/Cenas Sugeridos**: Breve descrição de cada

Seja criativo e engajante!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1200)
    
    embed = discord.Embed(
        title=f"📖 Plot: {tema.title()}",
        description=resposta,
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}")
    await ctx.send(embed=embed)

@bot.command(name='regra')
async def consultar_regra(ctx, *, duvida: str = None):
    """Consulta regras do sistema"""
    if not duvida:
        await ctx.send("❌ Forneça a regra ou dúvida. Exemplo: `!regra como funcionam ataques de oportunidade`")
        return
    
    await ctx.send(f"📚 Consultando regras... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Explique a seguinte regra de {SISTEMAS_DISPONIVEIS[sistema]['nome']}: {duvida}

Forneça:
- Explicação clara e direta
- Exemplo prático de uso
- Exceções ou casos especiais (se houver)
- Referência à página/seção do livro (se souber)

Seja preciso e didático!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1000)
    
    embed = discord.Embed(
        title=f"📚 Regra: {duvida.Title()}",
        description=resposta,
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}")
    await ctx.send(embed=embed)

@bot.command(name='mestre')
async def assistente_mestre(ctx, *, pergunta: str = None):
    """Assistente geral do mestre"""
    if not pergunta:
        await ctx.send("❌ Faça uma pergunta. Exemplo: `!mestre Como criar um encontro equilibrado para nível 5?`")
        return
    
    await ctx.send(f"🎲 Pensando... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    # Adiciona ao histórico
    conversation_history[ctx.channel.id].append({
        "role": "user",
        "content": pergunta
    })
    
    resposta = await chamar_groq(conversation_history[ctx.channel.id], max_tokens=1500)
    
    # Salva resposta no histórico
    conversation_history[ctx.channel.id].append({
        "role": "assistant",
        "content": resposta
    })
    
    # Limita histórico a 20 mensagens
    if len(conversation_history[ctx.channel.id]) > 20:
        conversation_history[ctx.channel.id] = [conversation_history[ctx.channel.id][0]] + conversation_history[ctx.channel.id][-19:]
    
    # Divide em chunks se necessário
    if len(resposta) > 4000:
        chunks = [resposta[i:i+4000] for i in range(0, len(resposta), 4000)]
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"🎲 Assistente do Mestre {f'({i+1}/{len(chunks)})' if len(chunks) > 1 else ''}",
                description=chunk,
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="🎲 Assistente do Mestre",
            description=resposta,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

@bot.command(name='limpar')
async def limpar_historico(ctx):
    """Limpa o histórico de conversas do canal"""
    if ctx.channel.id in conversation_history:
        sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        conversation_history[ctx.channel.id] = [
            {"role": "system", "content": get_system_prompt(sistema)}
        ]
        await ctx.send("✅ Histórico de conversas limpo!")
    else:
        await ctx.send("❌ Não há histórico para limpar.")

@bot.command(name='iniciativa')
async def rolar_iniciativa(ctx):
    """Rola iniciativa para membros no canal de voz"""
    if not ctx.author.voice:
        await ctx.send("❌ Você precisa estar em um canal de voz!")
        return
    
    membros = ctx.author.voice.channel.members
    if len(membros) < 2:
        await ctx.send("❌ Precisa de pelo menos 2 pessoas no canal de voz!")
        return
    
    iniciativas = []
    for membro in membros:
        if not membro.bot:
            rolagem = random.randint(1, 20)
            modificador = random.randint(-1, 5)  # Simulado
            total = rolagem + modificador
            iniciativas.append((membro.display_name, rolagem, modificador, total))
    
    # Ordena por total (decrescente)
    iniciativas.sort(key=lambda x: x[3], reverse=True)
    
    embed = discord.Embed(title="⚔️ Ordem de Iniciativa", color=discord.Color.red())
    
    ordem = ""
    for i, (nome, rolagem, mod, total) in enumerate(iniciativas, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
        ordem += f"{emoji} **{nome}**: {rolagem} {mod:+d} = **{total}**\n"
    
    embed.description = ordem
    embed.set_footer(text="Boa sorte no combate!")
    await ctx.send(embed=embed)

@bot.command(name='tesouro')
async def gerar_tesouro(ctx, *, nivel: str = "1-5"):
    """Gera tesouro aleatório baseado no nível"""
    await ctx.send(f"💰 Gerando tesouro para nível {nivel}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Gere um tesouro apropriado para personagens de nível {nivel} em {SISTEMAS_DISPONIVEIS[sistema]['nome']}.

Inclua:
- Quantidade de ouro/moedas
- 2-4 itens mágicos ou valiosos (com descrição breve)
- 1 item especial/único com história interessante

Seja criativo mas balanceado para o nível!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1000)
    
    embed = discord.Embed(
        title=f"💰 Tesouro (Nível {nivel})",
        description=resposta,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Solicitado por {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name='armadilha')
async def gerar_armadilha(ctx, *, dificuldade: str = "média"):
    """Gera uma armadilha para usar na aventura"""
    await ctx.send(f"⚠️ Gerando armadilha {dificuldade}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie uma armadilha de dificuldade {dificuldade} para {SISTEMAS_DISPONIVEIS[sistema]['nome']}.

Inclua:
- Descrição da armadilha (como funciona)
- CD para detectar
- CD para desarmar
- Efeito se ativada (dano, efeito de status, etc)
- Dica sutil que pode alertar os jogadores

Seja criativo e equilibrado!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=800)
    
    embed = discord.Embed(
        title=f"⚠️ Armadilha: {dificuldade.title()}",
        description=resposta,
        color=discord.Color.dark_red()
    )
    await ctx.send(embed=embed)

@bot.command(name='puzzle')
async def gerar_puzzle(ctx, *, tema: str = "genérico"):
    """Gera um quebra-cabeça ou enigma"""
    await ctx.send(f"🧩 Gerando puzzle... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie um quebra-cabeça/enigma com o tema: {tema}

Inclua:
- Descrição do puzzle (como se apresenta aos jogadores)
- Pistas disponíveis (2-3)
- Solução detalhada
- Recompensa por resolver
- Consequência se falharem (opcional)

Seja desafiador mas justo!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1200)
    
    # Envia a resposta em partes se necessário
    partes = resposta.split("**Solução")
    
    # Primeira parte (descrição e pistas)
    embed1 = discord.Embed(
        title=f"🧩 Puzzle: {tema.title()}",
        description=partes[0],
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed1)
    
    # Segunda parte (solução) - envia por DM para o mestre
    if len(partes) > 1:
        try:
            embed2 = discord.Embed(
                title="🔐 Solução (Spoiler!)",
                description="**Solução" + partes[1],
                color=discord.Color.dark_purple()
            )
            await ctx.author.send(embed=embed2)
            await ctx.send(f"✉️ Solução enviada por DM para {ctx.author.mention}!")
        except discord.Forbidden:
            await ctx.send("⚠️ Não consegui enviar a solução por DM. Ative as mensagens diretas!")

@bot.command(name='encontro')
async def gerar_encontro(ctx, nivel: int = 3, dificuldade: str = "média"):
    """Gera um encontro de combate balanceado"""
    await ctx.send(f"⚔️ Gerando encontro para nível {nivel}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie um encontro de combate balanceado para {SISTEMAS_DISPONIVEIS[sistema]['nome']}:
- Nível do grupo: {nivel}
- Dificuldade: {dificuldade}
- 4 jogadores

Inclua:
- Composição dos inimigos (quantos e quais)
- CR/ND total do encontro
- Ambiente/cenário do combate
- 2-3 elementos táticos (cobertura, terreno, hazards)
- Possível tesouro

Seja balanceado e interessante taticamente!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1200)
    
    embed = discord.Embed(
        title=f"⚔️ Encontro - Nível {nivel} ({dificuldade.title()})",
        description=resposta,
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}")
    await ctx.send(embed=embed)

@bot.command(name='item')
async def gerar_item(ctx, *, tipo: str = "mágico comum"):
    """Gera um item mágico ou especial"""
    await ctx.send(f"✨ Gerando item: {tipo}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie um item para {SISTEMAS_DISPONIVEIS[sistema]['nome']}: {tipo}

Inclua:
- Nome criativo
- Tipo e raridade
- Aparência/descrição
- Propriedades mecânicas (bônus, efeitos)
- História ou lore interessante (2-3 linhas)
- Possível malefício ou desvantagem (se apropriado)

Seja criativo e balanceado!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1000)
    
    embed = discord.Embed(
        title=f"✨ Item Gerado",
        description=resposta,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name='sessao')
async def planejar_sessao(ctx, *, tema: str = None):
    """Ajuda a planejar uma sessão completa"""
    if not tema:
        await ctx.send("❌ Forneça um tema ou objetivo. Exemplo: `!sessao explorar masmorra antiga`")
        return
    
    await ctx.send(f"📋 Planejando sessão: {tema}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie um plano de sessão completo para {SISTEMAS_DISPONIVEIS[sistema]['nome']} com o tema: {tema}

Inclua:
- **Resumo da Sessão** (2-3 linhas)
- **Cena de Abertura** (gancho inicial)
- **3-4 Encontros/Cenas Principais** (combate, exploração, roleplay)
- **Clímax** (momento épico da sessão)
- **Encerramento** (gancho para próxima sessão)
- **NPCs Importantes** (1-2 nomes e motivações)
- **Recompensas Sugeridas**

Formato: sessão de 3-4 horas. Seja detalhado mas conciso!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=2000)
    
    # Divide em chunks se necessário
    if len(resposta) > 4000:
        chunks = [resposta[i:i+3900] for i in range(0, len(resposta), 3900)]
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"📋 Plano de Sessão ({i+1}/{len(chunks)}): {tema.title()}",
                description=chunk,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=f"📋 Plano de Sessão: {tema.title()}",
            description=resposta,
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

@bot.command(name='nome')
async def gerar_nomes(ctx, *, tipo: str = "fantasia"):
    """Gera nomes para personagens, lugares, etc"""
    await ctx.send(f"📝 Gerando nomes de {tipo}... ⏳")
    
    prompt = f"""Gere 10 nomes criativos e memoráveis do tipo: {tipo}

Forneça:
- Lista numerada de 10 nomes
- Cada nome com uma palavra descritiva entre parênteses

Exemplos de tipos: fantasia, élfico, anão, taverna, cidade, reino, arma, feitiço, etc."""

    mensagens = [
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=600)
    
    embed = discord.Embed(
        title=f"📝 Nomes: {tipo.title()}",
        description=resposta,
        color=discord.Color.teal()
    )
    await ctx.send(embed=embed)

@bot.command(name='motivacao')
async def gerar_motivacao(ctx):
    """Gera motivações para NPCs ou vilões"""
    motivacoes = [
        "💰 **Ganância** - Busca riquezas e poder material",
        "👑 **Ambição** - Deseja controle e autoridade",
        "❤️ **Amor** - Age por alguém que ama",
        "⚖️ **Vingança** - Busca reparação por injustiça",
        "🛡️ **Proteção** - Defende algo/alguém importante",
        "🔬 **Conhecimento** - Busca segredos e sabedoria",
        "😱 **Medo** - Age por terror ou insegurança",
        "🎭 **Loucura** - Motivações irracionais",
        "⚔️ **Honra** - Segue código pessoal ou juramento",
        "🌟 **Destino** - Cumpre profecia ou chamado",
        "💀 **Sobrevivência** - Fará qualquer coisa para viver",
        "🎪 **Caos** - Quer ver o mundo queimar"
    ]
    
    escolhida = random.choice(motivacoes)
    
    embed = discord.Embed(
        title="🎭 Motivação Gerada",
        description=f"{escolhida}\n\nUse isso para dar profundidade aos seus NPCs!",
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed)

@bot.command(name='vilao')
async def gerar_vilao(ctx, *, tipo: str = "genérico"):
    """Gera um vilão completo"""
    await ctx.send(f"😈 Gerando vilão: {tipo}... ⏳")
    
    inicializar_historico(ctx.channel.id)
    sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
    
    prompt = f"""Crie um vilão memorável para {SISTEMAS_DISPONIVEIS[sistema]['nome']}: {tipo}

Inclua:
- **Nome e Título**
- **Aparência** (2-3 linhas marcantes)
- **Motivação Principal** (por que é vilão?)
- **Plano Maligno** (o que está tentando fazer?)
- **Ponto Fraco** (como pode ser derrotado?)
- **Quote Memorável** (algo que o vilão diria)
- **Stats Básicas** (se combate for relevante)

Seja criativo e tridimensional - vilões interessantes têm razões para suas ações!"""

    mensagens = [
        {"role": "system", "content": get_system_prompt(sistema)},
        {"role": "user", "content": prompt}
    ]
    
    resposta = await chamar_groq(mensagens, max_tokens=1500)
    
    embed = discord.Embed(
        title=f"😈 Vilão: {tipo.title()}",
        description=resposta,
        color=discord.Color.dark_red()
    )
    embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}")
    await ctx.send(embed=embed)

@bot.command(name='backup')
@commands.has_permissions(administrator=True)
async def fazer_backup(ctx):
    """Cria um backup manual dos dados (apenas admin)"""
    if salvar_dados():
        total_fichas = len(fichas_personagens)
        total_sistemas = len(sistemas_rpg)
        
        embed = discord.Embed(
            title="💾 Backup Realizado!",
            description=f"✅ Dados salvos com sucesso!\n\n"
                       f"📊 **Estatísticas:**\n"
                       f"• Fichas salvas: **{total_fichas}**\n"
                       f"• Canais configurados: **{total_sistemas}**\n"
                       f"• Local: `{DATA_DIR.absolute()}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Erro ao salvar backup!")

@bot.command(name='stats')
async def estatisticas(ctx):
    """Mostra estatísticas do bot"""
    total_fichas = len(fichas_personagens)
    fichas_usuario = len([f for f in fichas_personagens.values() if f["autor"] == ctx.author.id])
    total_canais = len(sistemas_rpg)
    
    # Conta fichas por sistema
    sistemas_count = {}
    for ficha in fichas_personagens.values():
        sistema = ficha.get('sistema', 'dnd5e')
        sistemas_count[sistema] = sistemas_count.get(sistema, 0) + 1
    
    sistemas_texto = "\n".join([f"• {SISTEMAS_DISPONIVEIS[s]['nome']}: {c}" for s, c in list(sistemas_count.items())[:10]])
    if len(sistemas_count) > 10:
        sistemas_texto += f"\n... e mais {len(sistemas_count) - 10} sistemas"
    
    embed = discord.Embed(
        title="📊 Estatísticas do Bot",
        color=discord.Color.blue()
    )
    embed.add_field(name="🎲 Geral", value=f"Servidores: **{len(bot.guilds)}**\nCanais configurados: **{total_canais}**", inline=False)
    embed.add_field(name="📜 Fichas", value=f"Total: **{total_fichas}**\nSuas fichas: **{fichas_usuario}**", inline=False)
    if sistemas_texto:
        embed.add_field(name="🎮 Fichas por Sistema", value=sistemas_texto, inline=False)
    embed.set_footer(text=f"💾 Auto-save ativo | Dados em: {DATA_DIR.name}/")
    
    await ctx.send(embed=embed)

# ---------------- Painel de ajuda ---------------- #
@bot.command(name="rpghelp")
async def rpghelp(ctx):
    """Mostra o guia completo de comandos do bot de RPG com paginação interativa."""
    pages = []

    # Página 1
    embed1 = discord.Embed(
        title="🎲 RPG Master Bot - Comandos (1/4)",
        description="Seu assistente completo de RPG de mesa!",
        color=discord.Color.teal()
    )
    embed1.add_field(
        name="⚙️ Configuração",
        value=(
            "`!sistema` - Ver/mudar sistema atual\n"
            "`!sistema dnd5e` - Mudar para D&D 5e\n"
            "`!sistemas` - Lista todos os 50+ sistemas\n"
            "`!buscarsistema <nome>` - Busca sistemas\n"
            "`!infosistema <código>` - Detalhes do sistema\n"
            "`!limpar` - Limpa histórico de conversa"
        ), inline=False
    )
    embed1.add_field(
        name="🎲 Dados & Iniciativa",
        value=(
            "`!rolar 1d20` ou `!r 1d20` - Rola dados\n"
            "`!rolar 2d6+3` - Rola com modificador\n"
            "`!rolar 4d6k3` - Mantém 3 maiores\n"
            "`!iniciativa` - Rola iniciativa para o grupo"
        ), inline=False
    )
    embed1.add_field(
        name="👤 Fichas & Personagens",
        value=(
            "`!ficha <nome>` - Cria ficha automática\n"
            "`!criarficha` - Formulário interativo 📝\n"
            "`!verficha` / `!verficha <nome>` - Ver fichas\n"
            "`!editarficha <nome>` - Edita ficha ✏️\n"
            "`!deletarficha <nome>` - Deleta ficha\n"
            "`!converterficha <sistema> <nome>` - Converte ficha\n"
            "`!minhasfichas [sistema]` - Lista detalhada"
        ), inline=False
    )
    embed1.set_footer(text="📄 Página 1/4 • Use os botões abaixo para navegar")
    pages.append(embed1)

    # Página 2
    embed2 = discord.Embed(
        title="🎲 RPG Master Bot - Comandos (2/4)",
        description="Ferramentas de combate e geração de conteúdo",
        color=discord.Color.orange()
    )
    embed2.add_field(
        name="⚔️ Combate & Encontros",
        value=(
            "`!monstro <nome>` - Busca stats\n"
            "`!encontro <nível> <dif>` - Gera encontro\n"
            "`!armadilha <dif>` - Cria armadilha\n"
            "`!cena <descrição>` - Cena descritiva"
        ), inline=False
    )
    embed2.add_field(
        name="✨ Geração de Conteúdo",
        value=(
            "`!item <tipo>` - Item mágico\n"
            "`!tesouro <nível>` - Tesouro balanceado\n"
            "`!puzzle <tema>` - Enigma\n"
            "`!vilao <tipo>` - Vilão completo\n"
            "`!nome <tipo>` - 10 nomes criativos\n"
            "`!motivacao` - Gera motivação para NPC"
        ), inline=False
    )
    embed2.add_field(
        name="📖 História & Campanha",
        value=(
            "`!plot <tema>` - Ideias de missão\n"
            "`!sessao <tema>` - Planeja sessão completa 📋\n"
            "`!regra <dúvida>` - Consulta regras"
        ), inline=False
    )
    embed2.set_footer(text="📄 Página 2/4 • Ferramentas do mestre e combate")
    pages.append(embed2)

    # Página 3
    embed3 = discord.Embed(
        title="🎲 RPG Master Bot - Comandos (3/4)",
        description="Assistente e sistemas disponíveis",
        color=discord.Color.blue()
    )
    embed3.add_field(
        name="🎭 Assistente do Mestre",
        value=(
            "`!mestre <pergunta>` - IA de apoio ao mestre\n"
            "`!npc <descrição>` - Cria NPC rápido\n"
            "`!stats` - Estatísticas do bot\n"
            "`!backup` - Backup manual (admin)"
        ), inline=False
    )
    embed3.add_field(
        name="📚 Sistemas Suportados",
        value=(
            "50+ sistemas de RPG!\n"
            "`!sistemas` / `!listarsistemas` - Ver todos\n"
            "`!buscarsistema <nome>` - Buscar\n"
            "`!infosistema <código>` - Detalhes"
        ), inline=False
    )
    embed3.add_field(
        name="💡 Dicas Rápidas",
        value=(
            "• `!criarficha` → formulário guiado\n"
            "• `!puzzle` envia solução por DM\n"
            "• `!sessao` → planeja 3-4h de jogo\n"
            "• `!mestre` mantém contexto ativo"
        ), inline=False
    )
    embed3.set_footer(text="📄 Página 3/4 • Assistente e sistemas")
    pages.append(embed3)

    # Página 4
    embed4 = discord.Embed(
        title="🎮 RPG Master Bot - Sessões de RPG (4/4)",
        description="Gerencie campanhas com canais privados e fichas integradas",
        color=discord.Color.dark_green()
    )
    embed4.add_field(
        name="🎬 Sessões e Jogadores",
        value=(
            "`!iniciarsessao @Jogador1 @Jogador2` - Cria sessão privada\n"
            "`!sessoes` - Lista sessões ativas\n"
            "`!infosessao` - Mostra detalhes da sessão\n"
            "`!convidarsessao @Jogador` - Adiciona jogador\n"
            "`!removerjogador @Jogador` - Remove jogador"
        ), inline=False
    )
    embed4.add_field(
        name="👤 Fichas em Sessão",
        value=(
            "`!selecionarficha <nome>` - Escolhe ficha\n"
            "`!mudarficha <nome>` - Troca personagem\n"
            "`!verficha <nome>` - Mostra ficha\n"
            "`!resumosessao` - Gera resumo com IA"
        ), inline=False
    )
    embed4.add_field(
        name="⚙️ Controle e Botões",
        value=(
            "`!pausarsessao` - Pausa/retoma sessão\n"
            "`!ajudasessao` - Guia completo de sessões\n\n"
            "🎬 **Botões no canal:**\n"
            "• Iniciar Aventura — Introdução épica\n"
            "• Ver Fichas — Mostra status\n"
            "• Encerrar Sessão — Deleta canal"
        ), inline=False
    )
    embed4.set_footer(text="📄 Página 4/4 • Sistema de Sessões com IA e botões")
    pages.append(embed4)

    # --- View interativa ---
    class HelpView(View):
        def __init__(self):
            super().__init__(timeout=180)
            self.page = 0

        async def update(self, interaction):
            embed = pages[self.page]
            await interaction.response.edit_message(embed=embed, view=self)

        @button(label="◀️ Anterior", style=discord.ButtonStyle.secondary)
        async def previous(self, interaction, button):
            self.page = (self.page - 1) % len(pages)
            await self.update(interaction)

        @button(label="▶️ Próximo", style=discord.ButtonStyle.secondary)
        async def next(self, interaction, button):
            self.page = (self.page + 1) % len(pages)
            await self.update(interaction)

    view = HelpView()
    await ctx.send(embed=pages[0], view=view)


# Handler de erros
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Comando não encontrado! Use `!rpghelp` para ver os comandos disponíveis.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argumento faltando! Use `!rpghelp` para ver como usar o comando.")
    else:
        await ctx.send(f"❌ Erro: {str(error)}")
        print(f"Erro: {error}")
        
# -------------------- 🔥 SISTEMA DE SESSÕES RPG 🔥 --------------------
try:
    setup_sessoes(
        bot,
        SISTEMAS_DISPONIVEIS,
        fichas_personagens,
        sistemas_rpg,
        sessoes_ativas,
        chamar_groq,
        get_system_prompt,
        salvar_dados,
    )
    print("✅ Sistema de sessões RPG carregado com sucesso!")
except Exception as e:
    print(f"⚠️ Erro ao inicializar sistema de sessões: {e}")

# ---------------- Inicia o bot ---------------- #
if __name__ == "__main__":
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("ERRO: Token do Discord não encontrado! Defina a variável DISCORD_BOT_TOKEN no .env")
    else:
        print("🎲 Iniciando RPG Master Bot...")
        bot.run(TOKEN)