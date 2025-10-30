# commands/dados.py
"""Comandos de rolagem de dados e iniciativa."""

import random
import re
import discord
from discord.ext import commands


def rolar_dados(expressao: str):
    """Interpreta expressões como 2d6+3 ou 4d6k3 e retorna (resultado, total)."""
    padrao = r"(\d*)d(\d+)(k\d+)?([+-]\d+)?"
    match = re.match(padrao, expressao.replace(" ", ""))
    if not match:
        return f"Expressão inválida: `{expressao}`", None

    qtd = int(match.group(1)) if match.group(1) else 1
    faces = int(match.group(2))
    keep = match.group(3)
    mod = int(match.group(4)) if match.group(4) else 0

    resultados = [random.randint(1, faces) for _ in range(qtd)]
    texto = f"🎲 Rolando {qtd}d{faces}"
    if keep:
        k = int(keep[1:])
        resultados.sort(reverse=True)
        mantidos = resultados[:k]
        texto += f" mantendo {k} maiores → {mantidos}"
        total = sum(mantidos) + mod
    else:
        total = sum(resultados) + mod

    if mod:
        texto += f" {'+' if mod > 0 else '-'} {abs(mod)}"
    texto += f"\n🧮 Resultado: {resultados} → **{total}**"
    return texto, total


def register_dados_commands(bot: commands.Bot):
    """Registra comandos de dados e iniciativa."""

    @bot.command(name="rolar", aliases=["r"])
    async def rolar(ctx, *, expressao: str):
        """Rola dados no formato 2d6+3, 4d6k3, etc."""
        texto, _ = rolar_dados(expressao)
        await ctx.send(texto)