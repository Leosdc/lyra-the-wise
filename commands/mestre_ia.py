# commands/mestre_ia.py
"""Comandos de assistência com IA (mestre, plot, regra, sessão)."""

import discord
from discord.ext import commands
from config import conversation_history, sistemas_rpg
from utils import chamar_groq, get_system_prompt


def register_mestre_ia_commands(bot: commands.Bot):
    """Registra comandos de IA para assistência ao mestre."""

    @bot.command(name="limpar")
    async def limpar(ctx):
        """Limpa o histórico de conversa do canal atual."""
        if str(ctx.channel.id) in conversation_history:
            conversation_history[str(ctx.channel.id)] = []
            await ctx.send("🧹 Histórico do canal limpo com sucesso!")
        else:
            await ctx.send("🧹 Nenhum histórico encontrado para este canal.")

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
            resposta += "\n\n⚠️ *Resposta pode ter sido cortada. Use `!sessao` novamente ou peça detalhes específicos com `!mestre`*"
        
        # Envia em partes se necessário
        if len(resposta) <= 1900:
            await ctx.send(f"📋 **Planejamento de Sessão: {tema}**\n\n{resposta}")
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
            
            await ctx.send(f"📋 **Planejamento de Sessão: {tema}** (parte 1/{len(partes)})\n\n{partes[0]}")
            for i, parte in enumerate(partes[1:], start=2):
                await ctx.send(f"📋 *(continuação {i}/{len(partes)})*\n\n{parte}")