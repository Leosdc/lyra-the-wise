# geracao_conteudo.py — Geração de NPCs, monstros, itens, puzzles, etc.
import discord
from discord.ext import commands
from utils import chamar_groq, get_system_prompt
from config import sistemas_rpg
from sistemas_rpg import SISTEMAS_DISPONIVEIS
from monstros_database import buscar_monstro, listar_monstros_por_sistema, formatar_monstro
import random

def register(bot: commands.Bot):
    """Registra comandos de geração de conteúdo."""

    def get_sistema_canal(channel_id):
        """Retorna o sistema configurado para o canal."""
        return sistemas_rpg.get(channel_id, "dnd5e")

    # ========== MONSTRO ==========
    @bot.command(name="monstro")
    async def monstro(ctx, *, nome: str = None):
        """Busca ou gera um monstro. Uso: !monstro <nome> ou !monstro para gerar novo"""
        sistema = get_sistema_canal(ctx.channel.id)
        
        if nome:
            # Primeiro tenta buscar no banco de dados
            monstro_db = buscar_monstro(nome, sistema)
            
            if monstro_db:
                # Encontrou no banco de dados
                texto = formatar_monstro(monstro_db)
                embed = discord.Embed(
                    title=f"👹 {monstro_db['nome']}",
                    description=texto[:4000],
                    color=discord.Color.dark_red()
                )
                embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']} | Do banco de dados")
                await ctx.send(embed=embed)
                return
            
            # Não encontrou, gera com IA
            system_prompt = get_system_prompt(sistema)
            prompt = f"Crie as estatísticas completas de combate para o monstro **{nome}** no sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: atributos, ataques, habilidades especiais, pontos de vida e nível de desafio. Seja detalhado e balanceado."
        else:
            # Gera monstro aleatório
            system_prompt = get_system_prompt(sistema)
            prompt = f"Crie um monstro original e interessante para o sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']}, com estatísticas completas de combate, habilidades únicas e uma breve descrição atmosférica. Seja criativo!"
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"👹 {'Gerando' if nome else 'Criando'} monstro{' ' + nome if nome else ' aleatório'}...")
        resposta = await chamar_groq(mensagens, max_tokens=1000)
        
        embed = discord.Embed(
            title=f"👹 {nome if nome else 'Monstro Gerado'}",
            description=resposta[:4000],
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']} | Gerado por IA")
        await ctx.send(embed=embed)

    # ========== LISTAR MONSTROS ==========
    @bot.command(name="monstros")
    async def listar_monstros(ctx):
        """Lista todos os monstros disponíveis no banco de dados para o sistema atual."""
        sistema = get_sistema_canal(ctx.channel.id)
        monstros = listar_monstros_por_sistema(sistema)
        
        if not monstros:
            await ctx.send(f"❌ Nenhum monstro catalogado para {SISTEMAS_DISPONIVEIS[sistema]['nome']} ainda.")
            return
        
        lista = "\n".join([f"• {m}" for m in monstros])
        embed = discord.Embed(
            title=f"👹 Monstros - {SISTEMAS_DISPONIVEIS[sistema]['nome']}",
            description=f"Use `!monstro <nome>` para ver detalhes\n\n{lista}",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=f"{len(monstros)} monstros disponíveis")
        await ctx.send(embed=embed)

    # ========== NPC ==========
    @bot.command(name="npc")
    async def npc(ctx, *, descricao: str = None):
        """Gera um NPC completo."""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        if descricao:
            prompt = f"Crie um NPC detalhado baseado em: {descricao}. Inclua: nome, personalidade marcante, aparência distintiva, motivações claras, um segredo interessante e estatísticas básicas para {SISTEMAS_DISPONIVEIS[sistema]['nome']}."
        else:
            prompt = f"Crie um NPC interessante e memorável com: nome único, personalidade marcante, aparência distintiva, motivações claras, um segredo intrigante e estatísticas básicas para {SISTEMAS_DISPONIVEIS[sistema]['nome']}."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send("🎭 Gerando NPC...")
        resposta = await chamar_groq(mensagens, max_tokens=800)
        
        embed = discord.Embed(
            title="🎭 NPC Gerado",
            description=resposta[:4000],
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    # ========== ENCONTRO ==========
    @bot.command(name="encontro")
    async def encontro(ctx, nivel: int = None, dificuldade: str = "medio"):
        """Gera um encontro balanceado. Uso: !encontro <nível> <facil/medio/dificil>"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        if not nivel:
            nivel = 5  # Padrão
        
        dif_map = {
            "facil": "fácil",
            "fácil": "fácil",
            "medio": "médio",
            "médio": "médio",
            "dificil": "difícil",
            "difícil": "difícil"
        }
        dificuldade = dif_map.get(dificuldade.lower(), "médio")
        
        prompt = f"Crie um encontro de combate balanceado para um grupo de nível {nivel} no sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Dificuldade: {dificuldade}. Inclua: inimigos com estatísticas completas, táticas de combate, descrição do ambiente e possíveis recompensas."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"⚔️ Gerando encontro nível {nivel} ({dificuldade})...")
        resposta = await chamar_groq(mensagens, max_tokens=1200)
        
        embed = discord.Embed(
            title=f"⚔️ Encontro - Nível {nivel} ({dificuldade.capitalize()})",
            description=resposta[:4000],
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    # ========== ARMADILHA ==========
    @bot.command(name="armadilha")
    async def armadilha(ctx, dificuldade: str = "medio"):
        """Gera uma armadilha. Uso: !armadilha <facil/medio/dificil>"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        dif_map = {
            "facil": "fácil",
            "fácil": "fácil",
            "medio": "médio",
            "médio": "médio",
            "dificil": "difícil",
            "difícil": "difícil"
        }
        dificuldade = dif_map.get(dificuldade.lower(), "médio")
        
        prompt = f"Crie uma armadilha criativa para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Dificuldade: {dificuldade}. Inclua: mecanismo de ativação, efeito, CD para detectar, CD para desarmar, dano/efeito e possível forma de evitar ou mitigar."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"🪤 Gerando armadilha ({dificuldade})...")
        resposta = await chamar_groq(mensagens, max_tokens=600)
        
        embed = discord.Embed(
            title=f"🪤 Armadilha ({dificuldade.capitalize()})",
            description=resposta[:4000],
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    # ========== ITEM ==========
    @bot.command(name="item")
    async def item(ctx, *, tipo: str = None):
        """Gera um item mágico/especial. Uso: !item <tipo opcional>"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        if tipo:
            prompt = f"Crie um item mágico/especial do tipo '{tipo}' para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: nome evocativo, descrição visual, propriedades mecânicas, história ou origem e raridade."
        else:
            prompt = f"Crie um item mágico/especial criativo para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: nome evocativo, descrição visual detalhada, propriedades mecânicas interessantes, uma breve história ou origem e raridade apropriada."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send("✨ Gerando item mágico...")
        resposta = await chamar_groq(mensagens, max_tokens=700)
        
        embed = discord.Embed(
            title="✨ Item Mágico",
            description=resposta[:4000],
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    # ========== TESOURO ==========
    @bot.command(name="tesouro")
    async def tesouro(ctx, nivel: int = None):
        """Gera tesouro balanceado. Uso: !tesouro <nível>"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        if not nivel:
            nivel = 5
        
        prompt = f"Crie um tesouro balanceado para grupo de nível {nivel} em {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: moedas/dinheiro, itens mundanos valiosos, 1-2 itens mágicos apropriados e descrição visual do tesouro."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"💰 Gerando tesouro para nível {nivel}...")
        resposta = await chamar_groq(mensagens, max_tokens=700)
        
        embed = discord.Embed(
            title=f"💰 Tesouro - Nível {nivel}",
            description=resposta[:4000],
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    # ========== PUZZLE ==========
    @bot.command(name="puzzle")
    async def puzzle(ctx, *, tema: str = None):
        """Gera um enigma/quebra-cabeça. Uso: !puzzle <tema opcional>"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        if tema:
            prompt = f"Crie um enigma/puzzle interessante com o tema '{tema}'. Inclua: descrição do puzzle, pistas disponíveis, solução e consequências de falha/sucesso. Seja criativo e desafiador."
        else:
            prompt = f"Crie um enigma/puzzle criativo e desafiador. Inclua: descrição visual e narrativa do puzzle, pistas sutis mas justas, solução clara e consequências interessantes de falha/sucesso."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send("🧩 Gerando puzzle...")
        resposta = await chamar_groq(mensagens, max_tokens=800)
        
        embed = discord.Embed(
            title="🧩 Enigma",
            description=resposta[:4000],
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    # ========== VILÃO ==========
    @bot.command(name="vilao")
    async def vilao(ctx, *, tipo: str = None):
        """Gera um vilão completo. Uso: !vilao <tipo opcional>"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        if tipo:
            prompt = f"Crie um vilão memorável do tipo '{tipo}' para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: nome, aparência marcante, personalidade complexa, motivações profundas, plano maligno, estatísticas completas e uma fraqueza ou vulnerabilidade interessante."
        else:
            prompt = f"Crie um vilão memorável e complexo para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: nome impactante, aparência distintiva, personalidade tridimensional, motivações que façam sentido (mesmo que distorcidas), plano detalhado, estatísticas completas de combate e uma fraqueza ou vulnerabilidade interessante."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send("😈 Gerando vilão...")
        resposta = await chamar_groq(mensagens, max_tokens=1200)
        
        embed = discord.Embed(
            title="😈 Vilão",
            description=resposta[:4000],
            color=discord.Color.dark_purple()
        )
        await ctx.send(embed=embed)

    # ========== CENA ==========
    @bot.command(name="cena")
    async def cena(ctx, *, descricao: str = None):
        """Descreve uma cena dramaticamente. Uso: !cena <descrição básica>"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        if not descricao:
            await ctx.send("❌ Use: `!cena <descrição básica>` - Ex: `!cena taverna movimentada`")
            return
        
        prompt = f"Descreva a seguinte cena de forma dramática e imersiva: '{descricao}'. Use linguagem evocativa, apele aos 5 sentidos, crie atmosfera e termine com um gancho para ação. Seja cinematográfico e envolvente."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send("🎬 Criando cena...")
        resposta = await chamar_groq(mensagens, max_tokens=600)
        
        embed = discord.Embed(
            title="🎬 Cena",
            description=resposta[:4000],
            color=discord.Color.teal()
        )
        await ctx.send(embed=embed)

    # ========== NOME ==========
    @bot.command(name="nome")
    async def nome(ctx, *, tipo: str = "fantasia"):
        """Gera lista de nomes. Uso: !nome <tipo> - Ex: élfico, anão, orc, humano, etc"""
        sistema = get_sistema_canal(ctx.channel.id)
        system_prompt = get_system_prompt(sistema)
        
        prompt = f"Gere uma lista de 10 nomes criativos do tipo '{tipo}' apropriados para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Varie entre nomes masculinos e femininos. Apenas liste os nomes, sem explicações."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"📝 Gerando nomes de {tipo}...")
        resposta = await chamar_groq(mensagens, max_tokens=400)
        
        embed = discord.Embed(
            title=f"📝 Nomes - {tipo.capitalize()}",
            description=resposta[:4000],
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    # ========== MOTIVAÇÃO ==========
    @bot.command(name="motivacao")
    async def motivacao(ctx):
        """Sorteia uma motivação aleatória para NPC."""
        motivacoes = [
            "💰 Ganância - Busca riqueza acima de tudo",
            "⚔️ Vingança - Quer punir aqueles que o prejudicaram",
            "👑 Poder - Deseja controle e influência",
            "❤️ Amor - Movido por paixão romântica ou familiar",
            "🛡️ Proteção - Quer defender alguém ou algo",
            "🎓 Conhecimento - Busca verdades ocultas",
            "🙏 Fé - Guiado por crenças religiosas",
            "⚖️ Justiça - Busca fazer o que é certo",
            "🎭 Redenção - Tenta corrigir erros do passado",
            "🌟 Glória - Quer fama e reconhecimento",
            "🔮 Destino - Acredita ter uma missão profética",
            "😱 Medo - Age para evitar algo terrível",
            "🎨 Criação - Quer deixar um legado artístico",
            "🏃 Liberdade - Busca escapar de algemas (literais ou metafóricas)",
            "🤝 Lealdade - Devotado a pessoa, grupo ou ideal",
            "💀 Morte - Obsessão com mortalidade (própria ou alheia)",
            "🌱 Sobrevivência - Fará qualquer coisa para viver",
            "😈 Caos - Deseja destruir ordem estabelecida",
            "🧩 Curiosidade - Movido por fascínio pelo desconhecido",
            "💔 Perda - Ainda lida com trauma de perdas passadas"
        ]
        
        motivacao = random.choice(motivacoes)
        embed = discord.Embed(
            title="🎲 Motivação Aleatória",
            description=motivacao,
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)

    print("✅ geracao_conteudo carregado com sucesso!")