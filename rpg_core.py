# rpg_core.py - Corrigido
import random
import re
import discord
from discord.ext import commands
from config import conversation_history
from utils import chamar_groq, get_system_prompt

# === Funções auxiliares ===

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


# === Registro principal ===

def register(bot):
    """Registra os comandos principais do bot RPG."""

    # --- Limpar histórico ---
    @bot.command(name="limpar")
    async def limpar(ctx):
        """Limpa o histórico de conversa do canal atual."""
        if str(ctx.channel.id) in conversation_history:
            conversation_history[str(ctx.channel.id)] = []
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
        resultados = {
            membro.display_name: random.randint(1, 20) + random.randint(1, 4)
            for membro in participantes
        }

        ranking = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        texto = "⚔️ **Iniciativa do Grupo:**\n"
        for i, (nome, valor) in enumerate(ranking, start=1):
            texto += f"{i}. **{nome}** → {valor}\n"
        await ctx.send(texto)

    # --- Mestre (IA) ---
    @bot.command(name="mestre")
    async def mestre(ctx, *, pergunta: str):
        """Interaja com o Mestre de RPG (IA)."""
        system_prompt = get_system_prompt("dnd5e")
        historico = conversation_history.setdefault(str(ctx.channel.id), [])
        
        # Adiciona mensagem do usuário
        historico.append({"role": "user", "content": pergunta})
        
        # CORREÇÃO: Cria lista completa de mensagens
        mensagens_completas = [
            {"role": "system", "content": system_prompt}
        ] + historico

        resposta = await chamar_groq(mensagens_completas, max_tokens=800)
        
        if resposta and "Erro" not in resposta:
            historico.append({"role": "assistant", "content": resposta})
            await ctx.send(f"🎭 {resposta[:1900]}")
        else:
            await ctx.send(f"⚠️ {resposta}")

    # --- Plot ---
    @bot.command(name="plot")
    async def plot(ctx, *, tema: str):
        """Gera uma ideia de missão ou aventura."""
        prompt = f"Crie uma ideia de missão ou aventura para o tema: {tema}"
        system_prompt = get_system_prompt("dnd5e")
        
        # CORREÇÃO: Passa lista de mensagens
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=800)
        await ctx.send(f"📜 Ideia de aventura:\n{resposta[:1900]}")

    # --- Regra ---
    @bot.command(name="regra")
    async def regra(ctx, *, duvida: str):
        """Consulta uma regra específica do sistema atual."""
        prompt = f"Explique a seguinte dúvida de RPG de mesa de forma clara e breve: {duvida}"
        system_prompt = get_system_prompt("dnd5e")
        
        # CORREÇÃO: Passa lista de mensagens
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=600)
        await ctx.send(f"⚖️ {resposta[:1900]}")

    print("✅ Módulo 'rpg_core' carregado com sucesso!")