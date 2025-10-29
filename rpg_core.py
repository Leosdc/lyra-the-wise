# rpg_core.py
import random
import re
import discord
from discord.ext import commands
from config import conversation_history, sistemas_rpg
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
        sistema_atual = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema_atual)
        
        historico = conversation_history.setdefault(str(ctx.channel.id), [])
        
        historico.append({"role": "user", "content": pergunta})
        
        mensagens_completas = [
            {"role": "system", "content": system_prompt}
        ] + historico

        resposta = await chamar_groq(mensagens_completas, max_tokens=2000)
        
        if resposta and "Erro" not in resposta:
            historico.append({"role": "assistant", "content": resposta})
            
            # Divide em mensagens se necessário
            if len(resposta) <= 1900:
                await ctx.send(f"🎭 {resposta}")
            else:
                partes = []
                texto_restante = resposta
                while texto_restante:
                    if len(texto_restante) <= 1900:
                        partes.append(texto_restante)
                        break
                    ponto_corte = texto_restante.rfind('\n', 0, 1900)
                    if ponto_corte == -1:
                        ponto_corte = 1900
                    partes.append(texto_restante[:ponto_corte])
                    texto_restante = texto_restante[ponto_corte:].lstrip()
                
                for i, parte in enumerate(partes, start=1):
                    if i == 1:
                        await ctx.send(f"🎭 {parte}")
                    else:
                        await ctx.send(f"🎭 *(cont. {i}/{len(partes)})* {parte}")
        else:
            await ctx.send(f"⚠️ {resposta}")

    # --- Plot ---
    @bot.command(name="plot")
    async def plot(ctx, *, tema: str):
        """Gera uma ideia de missão ou aventura."""
        sistema_atual = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema_atual)
        
        prompt = f"Crie uma ideia de missão ou aventura para o tema: {tema}"
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=1500)
        
        if len(resposta) <= 1900:
            await ctx.send(f"📜 **Ideia de aventura:**\n{resposta}")
        else:
            partes = []
            texto_restante = resposta
            while texto_restante:
                if len(texto_restante) <= 1900:
                    partes.append(texto_restante)
                    break
                ponto_corte = texto_restante.rfind('\n', 0, 1900)
                if ponto_corte == -1:
                    ponto_corte = 1900
                partes.append(texto_restante[:ponto_corte])
                texto_restante = texto_restante[ponto_corte:].lstrip()
            
            await ctx.send(f"📜 **Ideia de aventura:** (parte 1/{len(partes)})\n{partes[0]}")
            for i, parte in enumerate(partes[1:], start=2):
                await ctx.send(f"📜 *(continuação {i}/{len(partes)})*\n{parte}")

    # --- Regra --- CORRIGIDO AQUI
    @bot.command(name="regra")
    async def regra(ctx, *, duvida: str):
        """Consulta uma regra específica do sistema atual."""
        sistema_atual = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema_atual)
        
        prompt = f"Explique a seguinte dúvida de RPG de mesa de forma clara e breve: {duvida}"
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=1000)
        
        # Divide se necessário
        if len(resposta) <= 1900:
            await ctx.send(f"⚖️ {resposta}")
        else:
            partes = []
            texto_restante = resposta
            while texto_restante:
                if len(texto_restante) <= 1900:
                    partes.append(texto_restante)
                    break
                ponto_corte = texto_restante.rfind('\n', 0, 1900)
                if ponto_corte == -1:
                    ponto_corte = 1900
                partes.append(texto_restante[:ponto_corte])
                texto_restante = texto_restante[ponto_corte:].lstrip()
            
            await ctx.send(f"⚖️ {partes[0]}")
            for parte in partes[1:]:
                await ctx.send(f"⚖️ *(cont.)* {parte}")

    # --- Sessão --- NOVO
    @bot.command(name="sessao")
    async def sessao(ctx, *, tema: str):
        """Planeja uma sessão completa de RPG com o tema fornecido."""
        sistema_atual = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema_atual)
        
        await ctx.send(f"📋 Planejando sessão completa sobre: **{tema}**...")
        
        prompt = f"""Crie um planejamento COMPLETO de sessão de RPG para o tema: {tema}

Inclua de forma OBJETIVA e CONCISA:

1. **SINOPSE** - Resumo em 2-3 frases

2. **GANCHO INICIAL** - Como começar (1 parágrafo)

3. **CENAS PRINCIPAIS** (3 cenas):
   - Cena 1: Local, NPC, objetivo
   - Cena 2: Local, NPC, objetivo  
   - Cena 3: Local, NPC, objetivo

4. **ENCONTRO/COMBATE** - 1 encontro com stats resumidas

5. **RECOMPENSAS** - XP, itens, info

6. **GANCHO FUTURO** - 1-2 frases

7. **DICAS** - 2-3 dicas práticas

Sistema: {sistema_atual.upper()}. SEJA DIRETO E COMPLETE TODAS AS SEÇÕES."""

        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=3000)
        
        # Verifica se resposta foi cortada no meio
        if resposta and not any(palavra in resposta[-100:].lower() for palavra in ["dica", "nota", "final", "conclusão", "fim"]):
            # Resposta provavelmente foi cortada, avisa o usuário
            resposta += "\n\n⚠️ *Resposta pode ter sido cortada. Use `!sessao` novamente ou peça detalhes específicos com `!mestre`*"
        
        # Envia em partes se necessário
        if len(resposta) <= 1900:
            await ctx.send(f"📋 **Planejamento de Sessão: {tema}**\n\n{resposta}")
        else:
            # Divide em partes de 1900 caracteres
            partes = []
            texto_restante = resposta
            while texto_restante:
                if len(texto_restante) <= 1900:
                    partes.append(texto_restante)
                    break
                # Tenta cortar em uma quebra de linha próxima ao limite
                ponto_corte = texto_restante.rfind('\n', 0, 1900)
                if ponto_corte == -1:
                    ponto_corte = 1900
                partes.append(texto_restante[:ponto_corte])
                texto_restante = texto_restante[ponto_corte:].lstrip()
            
            await ctx.send(f"📋 **Planejamento de Sessão: {tema}** (parte 1/{len(partes)})\n\n{partes[0]}")
            for i, parte in enumerate(partes[1:], start=2):
                await ctx.send(f"📋 *(continuação {i}/{len(partes)})*\n\n{parte}")