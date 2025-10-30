# commands/geracao_mundo.py
"""Comandos de geração de mundo, cenas e nomes."""

import discord
from discord.ext import commands


def register_mundo_commands(bot: commands.Bot, sistemas_rpg, SISTEMAS_DISPONIVEIS, chamar_groq, get_system_prompt):
    """Registra comandos de geração de mundo e narrativa."""

    def get_sistema_usuario(user_id):
        """Retorna o sistema configurado para o USUÁRIO."""
        return sistemas_rpg.get(user_id, "dnd5e")

    # Remove comandos duplicados
    for cmd in ["cena", "nome"]:
        try:
            bot.remove_command(cmd)
        except Exception:
            pass

    @bot.command(name="cena")
    async def cena(ctx, *, descricao: str = None):
        """Descreve uma cena dramaticamente. Uso: !cena <descrição básica>"""
        sistema = get_sistema_usuario(ctx.author.id)
        system_prompt = get_system_prompt(sistema)
        
        if not descricao:
            await ctx.send("❌ Use: `!cena <descrição básica>` - Ex: `!cena taverna movimentada`")
            return
        
        prompt = f"Descreva a seguinte cena de forma dramática e imersiva: '{descricao}'. Use linguagem evocativa, apele aos 5 sentidos, crie atmosfera e termine com um gancho claro para ação. Seja cinematográfico e envolvente."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send("🎬 Criando cena...")
        resposta = await chamar_groq(mensagens, max_tokens=1000)
        
        embed = discord.Embed(
            title="🎬 Cena",
            description=resposta[:4000],
            color=discord.Color.teal()
        )
        await ctx.send(embed=embed)

    @bot.command(name="nome")
    async def nome(ctx, *, tipo: str = "fantasia"):
        """Gera lista de nomes. Uso: !nome <tipo> - Ex: élfico, anão, orc, humano, etc"""
        sistema = get_sistema_usuario(ctx.author.id)
        system_prompt = get_system_prompt(sistema)
        
        prompt = f"Gere uma lista de 10 nomes criativos do tipo '{tipo}' apropriados para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Varie entre nomes masculinos e femininos. Apenas liste os nomes, sem explicações."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"📝 Gerando nomes de {tipo}...")
        resposta = await chamar_groq(mensagens, max_tokens=500)
        
        embed = discord.Embed(
            title=f"📝 Nomes - {tipo.capitalize()}",
            description=resposta[:4000],
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
