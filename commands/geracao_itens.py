# commands/geracao_itens.py
"""Comandos de geração de itens, tesouros e puzzles."""

import discord
from discord.ext import commands


def register_itens_commands(bot: commands.Bot, sistemas_rpg, SISTEMAS_DISPONIVEIS, chamar_groq, get_system_prompt):
    """Registra comandos de geração de itens e tesouros."""

    def get_sistema_usuario(user_id):
        """Retorna o sistema configurado para o USUÁRIO."""
        return sistemas_rpg.get(user_id, "dnd5e")

    # Remove comandos duplicados
    for cmd in ["item", "tesouro", "puzzle"]:
        try:
            bot.remove_command(cmd)
        except Exception:
            pass

    @bot.command(name="item")
    async def item(ctx, *, tipo: str = None):
        """Gera um item mágico/especial. Uso: !item <tipo opcional>"""
        sistema = get_sistema_usuario(ctx.author.id)
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
        resposta = await chamar_groq(mensagens, max_tokens=1000)
        
        embed = discord.Embed(
            title="✨ Item Mágico",
            description=resposta[:4000],
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @bot.command(name="tesouro")
    async def tesouro(ctx, nivel: int = None):
        """Gera tesouro balanceado. Uso: !tesouro <nível>"""
        sistema = get_sistema_usuario(ctx.author.id)
        system_prompt = get_system_prompt(sistema)
        
        if not nivel:
            nivel = 5
        
        prompt = f"Crie um tesouro balanceado para grupo de nível {nivel} em {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: moedas/dinheiro, itens mundanos valiosos, 1-2 itens mágicos apropriados e descrição visual do tesouro."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"💰 Gerando tesouro para nível {nivel}...")
        resposta = await chamar_groq(mensagens, max_tokens=1000)
        
        embed = discord.Embed(
            title=f"💰 Tesouro - Nível {nivel}",
            description=resposta[:4000],
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @bot.command(name="puzzle")
    async def puzzle(ctx, *, tema: str = None):
        """Gera um enigma/quebra-cabeça. Uso: !puzzle <tema opcional>"""
        sistema = get_sistema_usuario(ctx.author.id)
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
        resposta = await chamar_groq(mensagens, max_tokens=1200)
        
        embed = discord.Embed(
            title="🧩 Enigma",
            description=resposta[:4000],
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
