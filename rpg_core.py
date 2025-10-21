# rpg_core.py — versão final com integração dinâmica de sistemas
import random
import re
import discord
from discord.ext import commands
from config import conversation_history, sistemas_rpg
from utils import chamar_groq, get_system_prompt


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


def register(bot):
    """Registra os comandos principais do bot RPG."""

    # --- Limpar histórico ---
    @bot.command(name="limpar")
    async def limpar(ctx):
        """Limpa o histórico de conversa do canal atual."""
        canal_id = str(ctx.channel.id)
        if canal_id in conversation_history:
            conversation_history[canal_id] = []
            await ctx.send("🧹 Histórico do canal limpo com sucesso!")
        else:
            await ctx.send("🧹 Nenhum histórico encontrado para este canal.")

    # --- Rolar dados ---
    @bot.command(name="rolar", aliases=["r"])
    async def rolar(ctx, *, expressao: str):
        """Rola dados no formato 2d6+3, 4d6k3, etc."""
        texto, _ = rolar_dados(expressao)
        await ctx.send(texto)

    # --- Iniciativa ---
    @bot.command(name="iniciativa")
    async def iniciativa(ctx):
        """Rola iniciativa para todos os usuários no canal de voz."""
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ Você precisa estar em um canal de voz para usar este comando.")
            return

        canal = ctx.author.voice.channel
        participantes = canal.members
        resultados = {m.display_name: random.randint(1, 20) + random.randint(1, 4) for m in participantes}
        ranking = sorted(resultados.items(), key=lambda x: x[1], reverse=True)

        texto = "⚔️ **Iniciativa do Grupo:**\n"
        for i, (nome, valor) in enumerate(ranking, start=1):
            texto += f"{i}. **{nome}** → {valor}\n"
        await ctx.send(texto)

    # --- Mestre (IA) ---
    @bot.command(name="mestre")
    async def mestre(ctx, *, pergunta: str):
        """Interaja com o Mestre de RPG (IA)."""
        canal_id = str(ctx.channel.id)
        sistema_atual = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        system_prompt = get_system_prompt(sistema_atual)

        historico = conversation_history.setdefault(canal_id, [])
        historico.append({"role": "user", "content": pergunta})

        mensagens = [{"role": "system", "content": system_prompt}] + historico
        resposta = await chamar_groq(mensagens, max_tokens=800)

        if resposta and "Erro" not in resposta:
            historico.append({"role": "assistant", "content": resposta})
            await ctx.send(f"🎭 {resposta[:1900]}")
        else:
            await ctx.send(f"⚠️ {resposta or 'Erro desconhecido ao chamar a IA.'}")

    # --- Plot ---
    @bot.command(name="plot")
    async def plot(ctx, *, tema: str):
        """Gera uma ideia de missão ou aventura."""
        sistema_atual = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        system_prompt = get_system_prompt(sistema_atual)

        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Crie uma missão ou aventura no estilo de {sistema_atual}, com o tema: {tema}"}
        ]

        resposta = await chamar_groq(mensagens, max_tokens=700)
        await ctx.send(f"📜 Ideia de aventura ({sistema_atual.upper()}):\n{resposta[:1900]}")

    # --- Regra ---
    @bot.command(name="regra")
    async def regra(ctx, *, duvida: str):
        """Consulta uma regra específica do sistema atual."""
        sistema_atual = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        system_prompt = get_system_prompt(sistema_atual)

        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Explique brevemente a seguinte dúvida do sistema {sistema_atual}: {duvida}"}
        ]

        resposta = await chamar_groq(mensagens, max_tokens=600)
        await ctx.send(f"⚖️ {resposta[:1900]}")

    print("✅ Módulo 'rpg_core' carregado com suporte a múltiplos sistemas!")
