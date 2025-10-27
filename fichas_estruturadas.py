# fichas_estruturadas.py
import re
import json
import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button
from utils import chamar_groq, get_system_prompt, key_from_name
from config import fichas_personagens, sistemas_rpg, sessoes_ativas
from sistemas_rpg import SISTEMAS_DISPONIVEIS, resolver_alias
import os

DATA_DIR = os.path.join(os.getcwd(), "bot_data")
FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")

# ========== ESTRUTURA DE FICHA POR SISTEMA ==========

ESTRUTURA_FICHAS = {
    "dnd5e": {
        "secoes": ["basico", "atributos", "recursos", "combate", "equipamento", "magia", "historia"],
        "campos": {
            "basico": ["Nome", "Raça", "Classe", "Nível", "Antecedente", "Alinhamento"],
            "atributos": ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"],
            "recursos": ["HP Máximo", "HP Atual", "Dados de Vida", "Proficiência"],
            "combate": ["CA", "Iniciativa", "Velocidade", "Ataques"],
            "equipamento": ["Armas", "Armadura", "Itens", "Dinheiro"],
            "magia": ["Nível de Conjurador", "CD de Magia", "Bônus de Ataque", "Espaços de Magia", "Magias Conhecidas"],
            "historia": ["Personalidade", "Ideais", "Vínculos", "Defeitos", "História"]
        }
    },
    "pathfinder": {
        "secoes": ["basico", "atributos", "recursos", "combate", "equipamento", "magia", "historia"],
        "campos": {
            "basico": ["Nome", "Ancestralidade", "Classe", "Nível", "Background", "Divindade"],
            "atributos": ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"],
            "recursos": ["HP Máximo", "HP Atual", "Pontos Heroicos", "Proficiências"],
            "combate": ["CA", "Fortitude", "Reflexos", "Vontade", "Velocidade", "Ataques"],
            "equipamento": ["Armas", "Armadura", "Itens Mágicos", "Investidos", "Ouro"],
            "magia": ["Tradição", "CD", "Ataque", "Pontos de Foco", "Magias Preparadas"],
            "historia": ["Personalidade", "Crenças", "História"]
        }
    },
    "cthulhu": {
        "secoes": ["basico", "atributos", "recursos", "combate", "pericia", "historia"],
        "campos": {
            "basico": ["Nome", "Ocupação", "Idade", "Sexo", "Residência", "Local de Nascimento"],
            "atributos": ["FOR", "CON", "TAM", "DES", "APA", "INT", "POD", "EDU", "SOR"],
            "recursos": ["HP Máximo", "HP Atual", "Sanidade Máxima", "Sanidade Atual", "Magia", "Movimento"],
            "combate": ["Dano Bônus", "Constituição", "Esquiva", "Armas"],
            "pericia": ["Perícias de Investigação", "Perícias Interpessoais", "Perícias de Combate", "Outras"],
            "historia": ["Descrição Pessoal", "Ideologia", "Pessoas Importantes", "Locais Significativos", "Posses Valiosas", "Traços", "Feridas e Cicatrizes"]
        }
    },
    "shadowrun": {
        "secoes": ["basico", "atributos", "recursos", "combate", "equipamento", "magia", "historia"],
        "campos": {
            "basico": ["Nome", "Metatipo", "Arquétipo", "Idade", "Sexo", "Estilo de Vida"],
            "atributos": ["Corpo", "Agilidade", "Reação", "Força", "Força de Vontade", "Lógica", "Intuição", "Carisma"],
            "recursos": ["Essência", "Magia", "Ressonância", "Borda", "Iniciativa", "Karma"],
            "combate": ["Monitores de Dano", "Defesas", "Limiar de Dor", "Armas"],
            "equipamento": ["Cyberware", "Bioware", "Equipamento", "Veículos", "Nuyen"],
            "magia": ["Tradição", "Feitiços", "Formas de Conjuração", "Espíritos Vinculados"],
            "historia": ["Conceito", "Contatos", "Inimigos", "História"]
        }
    },
    "vampire": {
        "secoes": ["basico", "atributos", "recursos", "disciplinas", "equipamento", "historia"],
        "campos": {
            "basico": ["Nome", "Clã", "Geração", "Seita", "Idade Aparente", "Refúgio"],
            "atributos": ["Força", "Destreza", "Vigor", "Carisma", "Manipulação", "Compostura", "Inteligência", "Raciocínio", "Perseverança"],
            "recursos": ["Saúde", "Força de Vontade", "Humanidade", "Fome", "Pontos de Sangue"],
            "disciplinas": ["Disciplinas de Clã", "Disciplinas Adquiridas", "Poderes", "Rituais"],
            "equipamento": ["Recursos", "Refúgios", "Lacaios", "Contatos", "Posses"],
            "historia": ["Abraço", "Sire", "Ambição", "Desejo", "Máscara", "Juramentos", "Inimigos"]
        }
    }
}

# Template genérico para sistemas não mapeados
ESTRUTURA_GENERICA = {
    "secoes": ["basico", "atributos", "recursos", "combate", "equipamento", "historia"],
    "campos": {
        "basico": ["Nome", "Raça/Ancestralidade", "Classe/Arquétipo", "Nível", "Conceito"],
        "atributos": ["Atributos Principais"],
        "recursos": ["Pontos de Vida", "Recursos Especiais"],
        "combate": ["Defesa", "Ataques", "Iniciativa"],
        "equipamento": ["Armas", "Armadura", "Itens", "Dinheiro"],
        "historia": ["Personalidade", "História", "Motivações"]
    }
}

def get_estrutura_ficha(sistema):
    """Retorna a estrutura de ficha apropriada para o sistema."""
    return ESTRUTURA_FICHAS.get(sistema, ESTRUTURA_GENERICA)

# ========== FUNÇÕES DE PERSISTÊNCIA ==========

def salvar_fichas_agora():
    """SALVA FICHAS IMEDIATAMENTE no arquivo JSON com encoding correto."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Força encoding UTF-8 explicitamente
        with open(FICHAS_PATH, "w", encoding="utf-8") as f:
            json.dump(fichas_personagens, f, ensure_ascii=False, indent=2)
        
        print(f"💾 FICHAS SALVAS! Total: {len(fichas_personagens)}")
        return True
    except Exception as e:
        print(f"❌ ERRO ao salvar fichas: {e}")
        import traceback
        traceback.print_exc()
        return False

def encontrar_ficha(user_id, nome):
    """Busca ficha do usuário. Prioriza match exato, depois busca parcial."""
    nome_lower = nome.lower().strip()
    
    # 1ª tentativa: Match EXATO (ignora case)
    for k, v in fichas_personagens.items():
        if v.get("autor") == user_id:
            if v.get("nome", "").lower().strip() == nome_lower:
                return k, v
    
    # 2ª tentativa: Match parcial
    nome_proc = re.sub(r'[^a-z0-9_]+', '', nome_lower)
    for k, v in fichas_personagens.items():
        if v.get("autor") == user_id:
            nome_limpo = re.sub(r'[^a-z0-9_]+', '', v.get("nome", "").lower())
            if nome_proc in nome_limpo or nome_limpo in nome_proc:
                return k, v
    
    return None, None

# ========== VIEW DE NAVEGAÇÃO DE FICHAS ==========

class FichaNavigationView(View):
    """View para navegar entre páginas da ficha."""
    
    def __init__(self, ficha_data, sistema, timeout=180):
        super().__init__(timeout=timeout)
        self.ficha_data = ficha_data
        self.sistema = sistema
        self.estrutura = get_estrutura_ficha(sistema)
        self.current_page = 0
        self.max_pages = len(self.estrutura["secoes"])
        
    def get_embed(self):
        """Gera embed para a página atual."""
        secao_nome = self.estrutura["secoes"][self.current_page]
        campos = self.estrutura["campos"][secao_nome]
        
        # Títulos bonitos para as seções
        titulos_secoes = {
            "basico": "📋 Dados Básicos",
            "atributos": "💪 Atributos",
            "recursos": "❤️ Recursos e Pontos",
            "combate": "⚔️ Combate",
            "equipamento": "🎒 Equipamento",
            "magia": "✨ Magia e Conjuração",
            "disciplinas": "🩸 Disciplinas Vampíricas",
            "pericia": "🔍 Perícias",
            "historia": "📖 História e Personalidade"
        }
        
        titulo = titulos_secoes.get(secao_nome, secao_nome.title())
        
        # Pega dados estruturados ou conteúdo antigo
        if "secoes" in self.ficha_data and self.ficha_data["secoes"]:
            conteudo_secao = self.ficha_data["secoes"].get(secao_nome, {})
            descricao = ""
            
            # NORMALIZA nomes de campos (remove acentos quebrados)
            for campo in campos:
                # Tenta encontrar o campo com encoding correto OU incorreto
                valor = None
                
                # 1. Tenta nome correto
                if campo in conteudo_secao:
                    valor = conteudo_secao[campo]
                else:
                    # 2. Tenta variações com encoding quebrado
                    campo_lower = campo.lower()
                    for k, v in conteudo_secao.items():
                        if k.lower().replace('ã§', 'ç').replace('ã£', 'ã').replace('ãª', 'ê') == campo_lower:
                            valor = v
                            break
                
                if valor is None:
                    valor = "—"
                
                # Formata o valor
                if isinstance(valor, list):
                    valor = ", ".join(str(item) for item in valor)
                elif isinstance(valor, dict):
                    valor = json.dumps(valor, ensure_ascii=False)
                
                descricao += f"**{campo}:** {valor}\n"
        else:
            # Formato antigo - exibe conteúdo bruto
            descricao = self.ficha_data.get("conteudo", "Ficha no formato antigo. Use !editarficha para atualizar.")[:4000]
        
        embed = discord.Embed(
            title=f"📜 {self.ficha_data.get('nome', 'Ficha')}",
            description=descricao,
            color=discord.Color.gold()
        )
        
        embed.set_footer(text=f"Página {self.current_page + 1}/{self.max_pages} • {titulo} • Sistema: {SISTEMAS_DISPONIVEIS[self.sistema]['nome']}")
        
        return embed
    
    @discord.ui.button(label="◀️ Anterior", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        """Vai para a página anterior."""
        self.current_page = (self.current_page - 1) % self.max_pages
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    @discord.ui.button(label="▶️ Próxima", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        """Vai para a próxima página."""
        self.current_page = (self.current_page + 1) % self.max_pages
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: discord.Interaction, button: Button):
        """Fecha a visualização."""
        await interaction.message.delete()

# ========== REGISTRO DE COMANDOS ==========

def register(bot: commands.Bot):
    # Remove comandos duplicados
    for cmd in ["ficha", "criarficha", "verficha", "editarficha", "deletarficha",
                "minhasfichas", "converterficha", "exportarficha"]:
        try:
            bot.remove_command(cmd)
        except Exception:
            pass

    # ========== CRIAR FICHA ESTRUTURADA ==========
    @bot.command(name="criarficha")
    async def criar_ficha_estruturada(ctx):
        """Cria uma ficha estruturada através de perguntas interativas."""
        sistema = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema)
        estrutura = get_estrutura_ficha(sistema)
        
        # Deleta comando do usuário
        try:
            await ctx.message.delete()
        except:
            pass
        
        # Envia tudo por DM
        try:
            # Mensagem inicial com preview das perguntas
            await ctx.author.send(
                f"📝 **Criação de Ficha Estruturada**\n"
                f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}\n\n"
                f"**Farei estas 8 perguntas para você:**\n"
                f"1️⃣ Nome do personagem\n"
                f"2️⃣ Raça/Ancestralidade\n"
                f"3️⃣ Classe/Profissão\n"
                f"4️⃣ Nível ou Idade\n"
                f"5️⃣ Personalidade (3-5 traços)\n"
                f"6️⃣ Aparência física\n"
                f"7️⃣ Background/Origem\n"
                f"8️⃣ Objetivos/Motivações\n\n"
                f"💡 **Dica importante:** Para evitar timeout durante a criação, "
                f"prepare suas respostas mais longas (história, aparência, objetivos) "
                f"em outro lugar e cole quando chegar a pergunta!\n\n"
                f"Digite `cancelar` a qualquer momento para parar.\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"**1/8** - Qual o **nome** do seu personagem?"
            )
            
            await ctx.send(
                f"✅ {ctx.author.mention}, processo de criação iniciado no privado! "
                f"Confira sua DM.",
                delete_after=10
            )
        
        except discord.Forbidden:
            await ctx.send(
                f"❌ {ctx.author.mention}, não consigo te enviar DM! "
                f"Habilite mensagens diretas nas configurações.",
                delete_after=15
            )
            return
        
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
        
        try:
            # Nome
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            nome = msg.content
            
            # Raça/Ancestralidade
            await ctx.author.send(f"**2/8** - Qual a **raça/ancestralidade** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            raca = msg.content
            
            # Classe/Arquétipo
            await ctx.author.send(f"**3/8** - Qual a **classe/profissão** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            classe = msg.content
            
            # Nível/Idade
            await ctx.author.send(f"**4/8** - Qual o **nível ou idade** de {nome}? (Ex: Nível 5, ou 28 anos)")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            nivel = msg.content
            
            # Conceito/Personalidade
            await ctx.author.send(f"**5/8** - Descreva a **personalidade** de {nome} (3-5 traços):")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            conceito = msg.content
            
            # Aparência
            await ctx.author.send(f"**6/8** - Descreva a **aparência física** de {nome}:")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            aparencia = msg.content
            
            # Background/História
            await ctx.author.send(f"**7/8** - Qual o **background ou origem** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            historia = msg.content
            
            # Objetivos/Motivações
            await ctx.author.send(f"**8/8** - Quais os **objetivos ou motivações** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            objetivos = msg.content
            
            # Gera ficha estruturada com IA
            await ctx.author.send(f"✨ Gerando ficha estruturada de **{nome}** com IA...")
            
            # Monta prompt específico para formato estruturado
            prompt = f"""Crie uma ficha de personagem COMPLETA, DETALHADA e BALANCEADA para {SISTEMAS_DISPONIVEIS[sistema]['nome']}.

**INFORMAÇÕES FORNECIDAS PELO JOGADOR:**
- Nome: {nome}
- Raça/Ancestralidade: {raca}
- Classe/Profissão: {classe}
- Nível/Idade: {nivel}
- Personalidade: {conceito}
- Aparência Física: {aparencia}
- Background/Origem: {historia}
- Objetivos/Motivações: {objetivos}

**INSTRUÇÕES OBRIGATÓRIAS:**
1. EXPANDA todas as informações - transforme respostas curtas em descrições ricas
2. CALCULE todos os valores numéricos apropriados ao nível
3. PREENCHA 100% dos campos - NENHUM campo pode ficar vazio, com "—" ou "A definir"
4. CRIE equipamento inicial completo e apropriado
5. ADICIONE habilidades de classe do nível apropriado
6. DESENVOLVA história em 3-4 parágrafos envolventes

**FORMATO JSON OBRIGATÓRIO - PREENCHA TODOS OS CAMPOS:**

{{
  "basico": {{
    "Nome": "{nome}",
    "Raça": "[EXPANDIR {raca} com detalhes de sub-raça]",
    "Classe": "[EXPANDIR {classe} com arquétipo/caminho]",
    "Nível": "[EXTRAIR número de: {nivel}]",
    "Antecedente": "[CRIAR baseado em: {historia}]",
    "Alinhamento": "[DEFINIR baseado na personalidade]"
  }},
  "atributos": {{
    "Força": [VALOR 8-18],
    "Destreza": [VALOR 8-18],
    "Constituição": [VALOR 8-18],
    "Inteligência": [VALOR 8-18],
    "Sabedoria": [VALOR 8-18],
    "Carisma": [VALOR 8-18]
  }},
  "recursos": {{
    "HP Máximo": [CALCULAR: dado_classe × nível + CON×nível],
    "HP Atual": [IGUAL ao HP Máximo],
    "Dados de Vida": "[Ex: 5d8 para Paladino nível 5]",
    "Proficiência": "[+2 até nível 4, +3 para nível 5-8, +4 para 9-12, +5 para 13-16, +6 para 17-20]"
  }},
  "combate": {{
    "CA": [CALCULAR: 10 + mod_DES + armadura],
    "Iniciativa": [modificador de Destreza com sinal: +2, -1, etc],
    "Velocidade": "9m",
    "Ataques": ["[ARMA 1]: +[bônus] para acertar, [dano]+[mod]", "[ARMA 2]: +[bônus] para acertar, [dano]+[mod]"]
  }},
  "equipamento": {{
    "Armas": ["[LISTAR 2-3 armas apropriadas com bônus mágico se nível alto]"],
    "Armadura": "[TIPO de armadura apropriada (ex: Cota de Malha, Armadura de Placas +1)]",
    "Itens": ["[LISTAR 6-10 itens: poções, ferramentas, itens mundanos]"],
    "Dinheiro": "[QUANTIDADE apropriada] PO"
  }},
  "magia": {{
    "Nível de Conjurador": "[NÚMERO ou 'Não possui']",
    "CD de Magia": "[CALCULAR: 8 + proficiência + modificador_atributo ou 'N/A']",
    "Bônus de Ataque": "[proficiência + modificador ou 'N/A']",
    "Espaços de Magia": "[Ex: 4/3/2 ou por nível conforme classe ou 'N/A']",
    "Magias Conhecidas": ["[LISTAR 8-12 magias apropriadas ao nível e classe, ou 'Não possui magias']"]
  }},
  "historia": {{
    "Personalidade": "[EXPANDIR {conceito} em 2-3 frases detalhadas]",
    "Ideais": "[CRIAR 1-2 ideais baseados na personalidade e background]",
    "Vínculos": "[CRIAR 1-2 vínculos baseados em {historia} e {objetivos}]",
    "Defeitos": "[CRIAR 1-2 defeitos interessantes e balanceados]",
    "História": "[ESCREVER 3-4 parágrafos completos integrando: {aparencia}, {historia}, {objetivos} de forma coesa e envolvente]"
  }}
}}

**VALIDAÇÃO FINAL OBRIGATÓRIA:**
✓ TODOS os campos têm valores reais (não "—", "A definir", ou vazios)
✓ Atributos somam entre 70-78 (método padrão 4d6 descartando menor)
✓ HP calculado corretamente conforme dado de vida da classe
✓ CA inclui armadura apropriada
✓ Ataques têm bônus de ataque e dano calculados
✓ Equipamento faz sentido para o nível e classe
✓ Magias apropriadas para nível de conjurador
✓ História é rica, coerente e bem desenvolvida

**RETORNE APENAS O JSON PURO - SEM TEXTO ANTES OU DEPOIS, SEM MARKDOWN, SEM EXPLICAÇÕES.**"""

            historico = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            conteudo_bruto = await chamar_groq(historico, max_tokens=2500)
            
            # Tenta parsear JSON estruturado
            secoes_estruturadas = None
            try:
                conteudo_limpo = conteudo_bruto.strip()
                
                # Remove markdown
                if "```" in conteudo_limpo:
                    import re
                    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', conteudo_limpo, re.DOTALL)
                    if json_match:
                        conteudo_limpo = json_match.group(1)
                
                # Extrai JSON
                inicio = conteudo_limpo.find('{')
                fim = conteudo_limpo.rfind('}') + 1
                if inicio >= 0 and fim > inicio:
                    conteudo_limpo = conteudo_limpo[inicio:fim]
                
                # Parseia
                secoes_estruturadas = json.loads(conteudo_limpo)
                
                # Valida
                if not isinstance(secoes_estruturadas, dict) or not secoes_estruturadas:
                    raise ValueError("JSON inválido")
                
                print(f"✅ JSON OK! {len(secoes_estruturadas)} seções")
                
            except Exception as e:
                print(f"⚠️ Erro JSON: {e}")
                # Fallback básico
                secoes_estruturadas = {
                    "basico": {"Nome": nome, "Raça": raca, "Classe": classe, "Nível": nivel},
                    "atributos": {"Força": 10, "Destreza": 10, "Constituição": 10, "Inteligência": 10, "Sabedoria": 10, "Carisma": 10},
                    "recursos": {},
                    "combate": {},
                    "equipamento": {},
                    "magia": {},
                    "historia": {"Personalidade": conceito, "Aparência": aparencia, "História": historia, "Objetivos": objetivos}
                }
                await ctx.author.send("⚠️ IA teve dificuldades. Criada ficha básica. Use `!editarficha` para completar!")
            
            # Salva ficha
            chave = key_from_name(f"{ctx.author.id}_{nome}")
            fichas_personagens[chave] = {
                "nome": nome,
                "sistema": sistema,
                "autor": ctx.author.id,
                "criada_em": "estruturada",
                "secoes": secoes_estruturadas,
                "conteudo": conteudo_bruto
            }
            
            if salvar_fichas_agora():
                print(f"✅ Ficha estruturada '{nome}' salva para user {ctx.author.id}")
            
            # Mostra ficha com navegação
            if secoes_estruturadas and any(secoes_estruturadas.values()):
                view = FichaNavigationView(fichas_personagens[chave], sistema)
                await ctx.author.send(
                    content="✅ **Ficha Criada com Sucesso!**",
                    embed=view.get_embed(),
                    view=view
                )
            else:
                await ctx.author.send(
                    embed=discord.Embed(
                        title=f"⚠️ Ficha Criada (Formato Simplificado)",
                        description=(
                            f"**{nome}** foi criado, mas em formato simplificado.\n\n"
                            f"**Dados Básicos:**\n"
                            f"• Raça: {raca}\n"
                            f"• Classe: {classe}\n"
                            f"• Conceito: {conceito}\n\n"
                            f"**História:** {historia[:200]}...\n\n"
                            f"💡 **Dica:** Use `!editarficha {nome}` para adicionar atributos e equipamento."
                        ),
                        color=discord.Color.orange()
                    ).set_footer(text="Sistema: " + SISTEMAS_DISPONIVEIS[sistema]['nome'])
                )
            
        except asyncio.TimeoutError:
            await ctx.author.send(
                "⏰ Tempo esgotado!\n\n"
                "💡 **Dica:** Prepare suas respostas longas (história, aparência) "
                "em um editor de texto antes e cole quando chegar a pergunta.\n\n"
                "Use `!criarficha` novamente quando estiver pronto!"
            )

    # ========== VER FICHA COM NAVEGAÇÃO ==========
    @bot.command(name="verficha")
    async def ver_ficha(ctx, *, nome: str = None):
        """Visualiza uma ficha com navegação por páginas."""
        if not nome:
            await ctx.send("❌ Use `!verficha <nome>`.")
            return
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        
        if sessao:
            # Em sessão - permite ver fichas dos participantes
            participantes = [sessao["mestre_id"]] + sessao["jogadores"]
            ficha_encontrada = None
            sistema_encontrado = None
            
            for user_id in participantes:
                chave, ficha = encontrar_ficha(user_id, nome)
                if ficha:
                    ficha_encontrada = ficha
                    sistema_encontrado = ficha.get("sistema", "dnd5e")
                    break
            
            if not ficha_encontrada:
                await ctx.send(f"❌ Ficha '{nome}' não encontrada entre os participantes!")
                return
            
            view = FichaNavigationView(ficha_encontrada, sistema_encontrado)
            await ctx.send(embed=view.get_embed(), view=view)
            
        else:
            # Fora de sessão - apenas próprias fichas
            chave, ficha = encontrar_ficha(ctx.author.id, nome)
            if not ficha:
                await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
                return
            
            sistema = ficha.get("sistema", "dnd5e")
            view = FichaNavigationView(ficha, sistema)
            await ctx.send(embed=view.get_embed(), view=view)

    # ========== OUTROS COMANDOS (mantidos da versão anterior) ==========
    
    @bot.command(name="ficha")
    async def ficha_cmd(ctx, *, nome: str = None):
        """Cria ficha rápida ESTRUTURADA com IA."""
        if not nome:
            await ctx.send("❌ Use `!ficha <nome>` para criação rápida ou `!criarficha` para modo interativo estruturado.")
            return

        sistema = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema)
        estrutura = get_estrutura_ficha(sistema)
        sistema_nome = SISTEMAS_DISPONIVEIS[sistema]['nome']

        await ctx.send(f"📝 Criando ficha estruturada de **{nome}** em {sistema_nome}...")

        # Gera exemplo JSON dinâmico baseado na estrutura
        exemplo_secoes = []
        for secao in estrutura["secoes"]:
            campos = estrutura["campos"][secao]
            campos_exemplo = {campo: f"[preencher {campo}]" for campo in campos}
            exemplo_secoes.append(f'  "{secao}": {json.dumps(campos_exemplo, ensure_ascii=False, indent=4)}')
        
        exemplo_json = "{\n" + ",\n".join(exemplo_secoes) + "\n}"

        prompt = f"""Crie uma ficha de personagem COMPLETA e BALANCEADA para {sistema_nome}.

**PERSONAGEM:** {nome}

**INSTRUÇÕES OBRIGATÓRIAS:**
1. PREENCHA 100% dos campos - NUNCA deixe vazio, com "—" ou "A definir"
2. Crie valores apropriados para o sistema {sistema_nome}
3. Seja criativo mas coerente com as regras do sistema
4. História deve ter 3-4 parágrafos completos
5. Todos os valores numéricos devem ser calculados corretamente

**USE ESTA ESTRUTURA JSON EXATA:**

{exemplo_json}

**REGRAS:**
- Nome do personagem: {nome}
- TODOS os campos devem ter valores reais e completos
- Use terminologia correta do sistema
- Seja detalhado em descrições e história
- Calcule valores numéricos apropriados

**RETORNE APENAS O JSON - SEM MARKDOWN, SEM TEXTO EXTRA.**"""

        historico = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        conteudo_bruto = await chamar_groq(historico, max_tokens=2500)
        
        # Parser JSON robusto
        secoes_estruturadas = None
        try:
            conteudo_limpo = conteudo_bruto.strip()
            
            # Remove markdown
            if "```" in conteudo_limpo:
                import re
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', conteudo_limpo, re.DOTALL)
                if json_match:
                    conteudo_limpo = json_match.group(1)
            
            # Extrai JSON
            inicio = conteudo_limpo.find('{')
            fim = conteudo_limpo.rfind('}') + 1
            if inicio >= 0 and fim > inicio:
                conteudo_limpo = conteudo_limpo[inicio:fim]
            
            # Parseia
            secoes_estruturadas = json.loads(conteudo_limpo)
            
            # Valida que não está vazio
            if not isinstance(secoes_estruturadas, dict) or not secoes_estruturadas:
                raise ValueError("JSON vazio")
            
            # Valida que tem pelo menos a seção "basico"
            if "basico" not in secoes_estruturadas:
                raise ValueError("Falta seção 'basico'")
            
            print(f"✅ Ficha estruturada criada: {len(secoes_estruturadas)} seções")
            
        except Exception as e:
            print(f"⚠️ Erro ao parsear JSON: {e}")
            print(f"Conteúdo recebido: {conteudo_bruto[:500]}...")
            
            # Fallback genérico baseado na estrutura
            secoes_estruturadas = {}
            for secao in estrutura["secoes"]:
                secoes_estruturadas[secao] = {}
                for campo in estrutura["campos"][secao]:
                    if "Nome" in campo:
                        secoes_estruturadas[secao][campo] = nome
                    elif any(x in campo for x in ["HP", "Vida", "PV", "Pontos"]):
                        secoes_estruturadas[secao][campo] = 30
                    elif any(x in campo for x in ["Força", "FOR", "Destreza", "DES"]):
                        secoes_estruturadas[secao][campo] = 10
                    else:
                        secoes_estruturadas[secao][campo] = "—"
            
            await ctx.send("⚠️ IA teve dificuldades. Ficha básica criada. Use `!editarficha` para completar!")
        
        # Salva ficha
        chave = key_from_name(f"{ctx.author.id}_{nome}")
        fichas_personagens[chave] = {
            "nome": nome,
            "sistema": sistema,
            "autor": ctx.author.id,
            "criada_em": "estruturada_rapida",
            "secoes": secoes_estruturadas,
            "conteudo": conteudo_bruto
        }
        
        salvar_fichas_agora()
        print(f"✅ Ficha '{nome}' salva para sistema {sistema}")
        
        # Mostra ficha com navegação
        view = FichaNavigationView(fichas_personagens[chave], sistema)
        await ctx.send(
            content=f"✅ **Ficha Criada: {nome}**\n💡 Use `!criarficha` para modo interativo detalhado.",
            embed=view.get_embed(),
            view=view
        )

    @bot.command(name="minhasfichas")
    async def minhas_fichas(ctx, sistema_filtro: str = None):
        """Lista suas fichas."""
        user_id = ctx.author.id
        fichas_user = {k: v for k, v in fichas_personagens.items() if v.get("autor") == user_id}
        
        if not fichas_user:
            await ctx.send(f"❌ Você não tem fichas salvas ainda.\n💡 Use `!ficha <nome>` ou `!criarficha` para criar uma!")
            return

        if sistema_filtro:
            sistema_filtro = resolver_alias(sistema_filtro.lower())
            fichas_user = {k: v for k, v in fichas_user.items() if v.get("sistema") == sistema_filtro}

        total = len(fichas_user)
        sistemas_dict = {}
        for f in fichas_user.values():
            sistemas_dict.setdefault(f["sistema"], []).append(f)

        descricao = f"Total: {total} ficha(s)\n\n"
        for s, lista in sistemas_dict.items():
            descricao += f"🎲 {SISTEMAS_DISPONIVEIS[s]['nome']} ({len(lista)})\n"
            for f in lista:
                nome = f['nome']
                tipo = " 📋" if "secoes" in f and f["secoes"] else " 📄"
                descricao += f"• {nome}{tipo}\n"
            descricao += "\n"

        await ctx.send(
            embed=discord.Embed(
                title="📚 Suas Fichas de Personagem",
                description=descricao[:4000],
                color=discord.Color.blurple(),
            ).set_footer(text="📋 = Estruturada (com páginas) | 📄 = Formato antigo | Use !verficha <nome>")
        )

    @bot.command(name="deletarficha")
    async def deletar_ficha(ctx, *, nome: str = None):
        """Deleta uma ficha."""
        if not nome:
            await ctx.send("❌ Use `!deletarficha <nome>`.")
            return
        
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
            return

        del fichas_personagens[chave]
        salvar_fichas_agora()
        
        await ctx.send(f"🗑️ Ficha **{ficha['nome']}** deletada com sucesso.")

    @bot.command(name="converterficha")
    async def converter_ficha(ctx, novo_sistema: str, *, nome_personagem: str = None):
        """Converte ficha entre sistemas mantendo conceito."""
        if not nome_personagem:
            await ctx.send("❌ Use: `!converterficha <sistema> <nome>`\n💡 Exemplo: `!converterficha cthulhu Thorin`")
            return

        novo_sistema_original = novo_sistema
        novo_sistema = resolver_alias(novo_sistema.lower())
        
        if novo_sistema not in SISTEMAS_DISPONIVEIS:
            await ctx.send(f"❌ Sistema `{novo_sistema_original}` inválido.\n💡 Use `!sistemas` para ver todos disponíveis.")
            return

        chave, ficha = encontrar_ficha(ctx.author.id, nome_personagem)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada!")
            return

        atual = ficha.get("sistema", "dnd5e")
        if atual == novo_sistema:
            await ctx.send("⚠️ A ficha já é desse sistema.")
            return

        await ctx.send(f"🔄 Convertendo **{ficha['nome']}** de {SISTEMAS_DISPONIVEIS[atual]['nome']} para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}...")

        # Extrai dados da ficha original
        if "secoes" in ficha and ficha["secoes"]:
            # Ficha estruturada - extrai dados-chave
            secoes_orig = ficha["secoes"]
            dados_basicos = secoes_orig.get("basico", {})
            atributos = secoes_orig.get("atributos", {})
            historia_secao = secoes_orig.get("historia", {})
            
            descricao_personagem = f"""
Personagem: {ficha['nome']}
Conceito: {dados_basicos.get('Classe', dados_basicos.get('Arquétipo', 'Aventureiro'))}
Raça/Tipo: {dados_basicos.get('Raça', dados_basicos.get('Metatipo', dados_basicos.get('Clã', 'Humano')))}
Atributos principais: {', '.join([f'{k}:{v}' for k, v in list(atributos.items())[:3]])}
Personalidade: {historia_secao.get('Personalidade', 'A definir')}
História: {historia_secao.get('História', historia_secao.get('Background', 'A definir'))}
"""
        else:
            # Ficha em formato texto - usa conteúdo direto
            descricao_personagem = f"Ficha original:\n{ficha.get('conteudo', '')[:500]}"

        # Monta prompt de conversão
        prompt = f"""Converta o seguinte personagem de {SISTEMAS_DISPONIVEIS[atual]['nome']} para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}.

IMPORTANTE: Mantenha o CONCEITO, PERSONALIDADE e PODER RELATIVO do personagem, mas adapte completamente as mecânicas para o novo sistema.

{descricao_personagem}

Retorne a ficha COMPLETA no formato JSON estruturado:

{{
  "basico": {{}},
  "atributos": {{}},
  "recursos": {{}},
  "combate": {{}},
  "equipamento": {{}},
  "magia": {{}},
  "historia": {{}}
}}

Preencha TODOS os campos apropriados para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}. Seja balanceado e completo."""

        historico = [
            {"role": "system", "content": get_system_prompt(novo_sistema)},
            {"role": "user", "content": prompt},
        ]

        convertido = await chamar_groq(historico, max_tokens=2000)
        
        if not convertido or "Erro" in convertido:
            await ctx.send(f"⚠️ Erro ao converter ficha via IA: {convertido}")
            return

        # Tenta parsear JSON estruturado
        try:
            conteudo_limpo = convertido.strip()
            if conteudo_limpo.startswith("```"):
                conteudo_limpo = conteudo_limpo.split("```")[1]
                if conteudo_limpo.startswith("json"):
                    conteudo_limpo = conteudo_limpo[4:]
            
            secoes_convertidas = json.loads(conteudo_limpo)
        except json.JSONDecodeError:
            # Se falhar, usa formato texto mas avisa
            secoes_convertidas = {}
            await ctx.send("⚠️ Conversão em formato texto. Recomendo recriar com `!criarficha`.")

        # Cria nova ficha convertida
        nome_sistema = SISTEMAS_DISPONIVEIS[novo_sistema]['nome'].strip()
        novo_nome = f"{ficha['nome']} ({nome_sistema})"
        nova_chave = key_from_name(f"{ctx.author.id}_{novo_nome}")

        fichas_personagens[nova_chave] = {
            "nome": novo_nome,
            "sistema": novo_sistema,
            "autor": ctx.author.id,
            "convertida_de": atual,
            "secoes": secoes_convertidas,
            "conteudo": convertido  # Backup
        }

        if salvar_fichas_agora():
            print(f"✅ Ficha convertida '{novo_nome}' salva para user {ctx.author.id}")
        else:
            await ctx.send("⚠️ Aviso: A conversão foi feita mas pode não ter sido salva corretamente.")

        # Mostra resultado com navegação
        if secoes_convertidas:
            view = FichaNavigationView(fichas_personagens[nova_chave], novo_sistema)
            await ctx.send(
                embed=view.get_embed(),
                view=view
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="✅ Ficha Convertida!",
                    description=f"Nova ficha: **{novo_nome}**\n\n{convertido[:3000]}",
                    color=discord.Color.green(),
                ).set_footer(text="Use !verficha para visualizar com navegação")
            )

    @bot.command(name="exportarficha")
    async def exportar_ficha(ctx, *, nome: str = None):
        """Exporta ficha como JSON."""
        if not nome:
            await ctx.send("❌ Use `!exportarficha <nome>`.")
            return
        
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send("❌ Ficha não encontrada.")
            return

        json_data = json.dumps(ficha, indent=2, ensure_ascii=False)
        arquivo = f"{ficha['nome']}.json"
        
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(json_data)

        await ctx.send("📦 Ficha exportada!", file=discord.File(arquivo))
        os.remove(arquivo)

    @bot.command(name="editarficha")
    async def editar_ficha(ctx, *, nome: str = None):
        """Edita uma ficha existente de forma interativa."""
        if not nome:
            await ctx.send("❌ Use `!editarficha <nome>`.")
            return
        
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
            return
        
        sistema = ficha.get("sistema", "dnd5e")
        
        await ctx.send(
            f"✏️ **Editando ficha: {ficha['nome']}**\n\n"
            f"O que você deseja fazer?\n"
            f"1️⃣ - Editar atributos/estatísticas\n"
            f"2️⃣ - Adicionar equipamento/item\n"
            f"3️⃣ - Modificar história/background\n"
            f"4️⃣ - Edição livre (descreva o que quer mudar)\n"
            f"❌ - Digite `cancelar` para sair\n\n"
            f"Digite o número da opção:"
        )
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            # Escolha da opção
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if msg.content.lower() == 'cancelar':
                return await ctx.send("❌ Edição cancelada.")
            
            opcao = msg.content.strip()
            
            if opcao == "1":
                await ctx.send("📊 Descreva as mudanças nos atributos/estatísticas (ex: 'aumentar Força para 18, adicionar +2 em Constituição'):")
                msg = await bot.wait_for('message', check=check, timeout=120.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = f"Atualize os atributos e estatísticas conforme solicitado: {msg.content}"
                
            elif opcao == "2":
                await ctx.send("⚔️ Descreva o equipamento/item a adicionar:")
                msg = await bot.wait_for('message', check=check, timeout=120.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = f"Adicione o seguinte equipamento ao inventário do personagem: {msg.content}"
                
            elif opcao == "3":
                await ctx.send("📖 Descreva as mudanças na história/background:")
                msg = await bot.wait_for('message', check=check, timeout=180.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = f"Atualize a história e background do personagem: {msg.content}"
                
            elif opcao == "4":
                await ctx.send("✍️ Descreva livremente o que deseja mudar na ficha:")
                msg = await bot.wait_for('message', check=check, timeout=180.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = msg.content
                
            else:
                return await ctx.send("❌ Opção inválida! Use `!editarficha <nome>` novamente.")
            
            # Processa edição com IA
            await ctx.send(f"✨ Processando alterações em **{ficha['nome']}**...")
            
            system_prompt = get_system_prompt(sistema)
            
            # Extrai conteúdo atual (estruturado ou texto)
            if "secoes" in ficha and ficha["secoes"]:
                conteudo_atual = json.dumps(ficha["secoes"], indent=2, ensure_ascii=False)
                formato = "JSON estruturado"
            else:
                conteudo_atual = ficha.get("conteudo", "")
                formato = "texto"
            
            prompt = f"""Você deve editar uma ficha de personagem de {SISTEMAS_DISPONIVEIS[sistema]['nome']}.

**INSTRUÇÃO DO JOGADOR:**
{instrucao}

**FICHA ATUAL (formato {formato}):**
{conteudo_atual}

**REGRAS CRÍTICAS:**
1. MANTENHA toda a estrutura JSON original
2. Apenas ALTERE os campos mencionados na instrução
3. PRESERVE todos os outros valores inalterados
4. Se adicionar itens/equipamento, ADICIONE à lista existente (não substitua tudo)
5. PREENCHA campos vazios se a instrução pedir

**IMPORTANTE:** 
- Se formato é JSON, retorne JSON PURO (sem ```json ou markdown)
- TODOS os campos não mencionados devem permanecer EXATAMENTE iguais
- Valores calculados (HP, CA) só mudam se atributos mudarem

**RETORNE APENAS O JSON COMPLETO ATUALIZADO, SEM TEXTO EXTRA:**"""

            historico = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            conteudo_novo = await chamar_groq(historico, max_tokens=2500)

            historico = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            conteudo_novo = await chamar_groq(historico, max_tokens=2000)
            
            if not conteudo_novo or "Erro" in conteudo_novo:
                await ctx.send(f"⚠️ Erro ao editar ficha: {conteudo_novo}")
                return
            
            # Atualiza ficha
            if "secoes" in ficha and ficha["secoes"]:
                # Tenta parsear JSON estruturado
                try:
                    conteudo_limpo = conteudo_novo.strip()
                    if conteudo_limpo.startswith("```"):
                        conteudo_limpo = conteudo_limpo.split("```")[1]
                        if conteudo_limpo.startswith("json"):
                            conteudo_limpo = conteudo_limpo[4:]
                    
                    fichas_personagens[chave]["secoes"] = json.loads(conteudo_limpo)
                except json.JSONDecodeError:
                    await ctx.send("⚠️ Erro ao processar edição estruturada. Salvando como texto.")
                    fichas_personagens[chave]["conteudo"] = conteudo_novo
            else:
                fichas_personagens[chave]["conteudo"] = conteudo_novo
            
            if salvar_fichas_agora():
                print(f"✅ Ficha '{ficha['nome']}' atualizada para user {ctx.author.id}")
            else:
                await ctx.send("⚠️ Aviso: A edição foi feita mas pode não ter sido salva corretamente.")
            
            # Mostra resultado
            if "secoes" in fichas_personagens[chave] and fichas_personagens[chave]["secoes"]:
                view = FichaNavigationView(fichas_personagens[chave], sistema)
                await ctx.send(
                    content="✅ **Ficha Atualizada com Sucesso!**",
                    embed=view.get_embed(),
                    view=view
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title=f"✅ Ficha Atualizada: {ficha['nome']}",
                        description=conteudo_novo[:4000],
                        color=discord.Color.blue(),
                    ).set_footer(text="Use !verficha para ver a ficha completa")
                )
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado! Use `!editarficha <nome>` novamente.")

    print("✅ fichas_estruturadas carregado com sucesso!")