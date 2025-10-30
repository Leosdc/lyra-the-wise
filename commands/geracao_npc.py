# commands/geracao_npc.py
"""Comandos de geração de NPCs, vilões e motivações."""

import discord
from discord.ext import commands
import random


def register_npc_commands(bot: commands.Bot, sistemas_rpg, SISTEMAS_DISPONIVEIS, chamar_groq, get_system_prompt):
    """Registra comandos de geração de NPCs."""

    def get_sistema_usuario(user_id):
        """Retorna o sistema configurado para o USUÁRIO."""
        return sistemas_rpg.get(user_id, "dnd5e")

    # Remove comandos duplicados
    for cmd in ["npc", "vilao", "motivacao"]:
        try:
            bot.remove_command(cmd)
        except Exception:
            pass

    @bot.command(name="npc")
    async def npc(ctx, *, descricao: str = None):
        """Gera um NPC completo."""
        sistema = get_sistema_usuario(ctx.author.id)
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
        resposta = await chamar_groq(mensagens, max_tokens=1200)
        
        embed = discord.Embed(
            title="🎭 NPC Gerado",
            description=resposta[:4000],
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @bot.command(name="vilao")
    async def vilao(ctx, *, tipo: str = None):
        """Gera um vilão completo. Uso: !vilao <tipo opcional>"""
        sistema = get_sistema_usuario(ctx.author.id)
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
        resposta = await chamar_groq(mensagens, max_tokens=1800)
        
        embed = discord.Embed(
            title="😈 Vilão",
            description=resposta[:4000],
            color=discord.Color.dark_purple()
        )
        await ctx.send(embed=embed)

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
            "🃏 Liberdade - Busca escapar de algemas (literais ou metafóricas)",
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
