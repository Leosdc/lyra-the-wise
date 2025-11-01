# commands/xp_commands.py
"""
Sistema de XP e progressão de personagens.
"""

import discord
from discord.ext import commands
from typing import Dict, Any


# Tabela de XP por nível (D&D 5e como base)
XP_TABLE = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000
}


def get_xp_for_next_level(current_level: int) -> int:
    """Retorna XP necessário para próximo nível."""
    if current_level >= 20:
        return XP_TABLE[20]
    return XP_TABLE.get(current_level + 1, XP_TABLE[20])


def calculate_level_from_xp(xp: int) -> int:
    """Calcula nível baseado no XP total."""
    for nivel, xp_min in sorted(XP_TABLE.items(), reverse=True):
        if xp >= xp_min:
            return nivel
    return 1


def register_xp_commands(bot: commands.Bot, fichas_personagens: Dict[str, Any], salvar_dados):
    """Registra comandos de XP e progressão."""
    
    @bot.command(name="darxp")
    @commands.guild_only()
    async def dar_xp(ctx: commands.Context, jogador: discord.Member, quantidade: int):
        """[MESTRE] Dá XP para um jogador."""
        from config import sessoes_ativas
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Use dentro de uma sessão!")
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o **mestre** pode dar XP!")
        
        if quantidade <= 0:
            return await ctx.send("❌ Quantidade de XP deve ser positiva!")
        
        # Busca ficha do jogador
        fichas_sel = sessao.get("fichas", {})
        chave = fichas_sel.get(str(jogador.id)) or fichas_sel.get(jogador.id)
        
        if not chave or chave not in fichas_personagens:
            return await ctx.send(f"❌ {jogador.mention} não tem ficha selecionada!")
        
        ficha = fichas_personagens[chave]
        nome_personagem = ficha.get("nome", jogador.display_name)
        
        secoes = ficha.get("secoes", {})
        
        if "progressao" not in secoes:
            secoes["progressao"] = {}
        
        progressao = secoes["progressao"]
        
        # XP atual
        xp_atual = progressao.get("XP Atual", 0)
        xp_total = progressao.get("XP Total", 0)
        
        # Adiciona XP
        novo_xp_atual = xp_atual + quantidade
        novo_xp_total = xp_total + quantidade
        
        progressao["XP Atual"] = novo_xp_atual
        progressao["XP Total"] = novo_xp_total
        
        # Verifica level up
        basico = secoes.get("basico", {})
        nivel_atual = basico.get("Nível", 1)
        
        if isinstance(nivel_atual, str):
            try:
                nivel_atual = int(nivel_atual)
            except:
                nivel_atual = 1
        
        xp_proximo_nivel = get_xp_for_next_level(nivel_atual)
        
        leveled_up = False
        if novo_xp_atual >= xp_proximo_nivel and nivel_atual < 20:
            # LEVEL UP!
            novo_nivel = nivel_atual + 1
            basico["Nível"] = novo_nivel
            
            # Reseta XP atual para o próximo nível
            progressao["XP Atual"] = novo_xp_atual - xp_proximo_nivel
            
            leveled_up = True
            novo_xp_proximo = get_xp_for_next_level(novo_nivel)
            
            from core.ficha_helpers import salvar_fichas_agora
            salvar_fichas_agora()
            
            # Embed de level up
            embed = discord.Embed(
                title="🎉 LEVEL UP!",
                description=(
                    f"**{nome_personagem}** subiu para o **Nível {novo_nivel}**!\n\n"
                    f"💫 +{quantidade} XP recebidos\n"
                    f"📊 XP Total: {novo_xp_total}\n"
                    f"📈 Próximo nível: {novo_xp_proximo} XP"
                ),
                color=discord.Color.gold()
            )
            embed.set_footer(text=f"Jogador: {jogador.display_name}")
            
            await ctx.send(f"🎊 {jogador.mention}", embed=embed)
        else:
            from core.ficha_helpers import salvar_fichas_agora
            salvar_fichas_agora()
            
            # XP normal
            xp_faltando = xp_proximo_nivel - novo_xp_atual
            porcentagem = int((novo_xp_atual / xp_proximo_nivel) * 100)
            
            embed = discord.Embed(
                title=f"✨ XP Recebido!",
                description=(
                    f"**{nome_personagem}** ganhou **+{quantidade} XP**!\n\n"
                    f"📊 **XP Atual:** {novo_xp_atual} / {xp_proximo_nivel}\n"
                    f"📈 **Faltam:** {xp_faltando} XP para nível {nivel_atual + 1}\n"
                    f"📉 **Progresso:** {porcentagem}%\n"
                    f"🎯 **XP Total:** {novo_xp_total}"
                ),
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Jogador: {jogador.display_name}")
            
            await ctx.send(embed=embed)
    
    @bot.command(name="xp")
    async def ver_xp(ctx: commands.Context, *, nome_personagem: str = None):
        """Ver XP e progressão de um personagem."""
        from core.ficha_helpers import encontrar_ficha
        from config import sessoes_ativas
        
        # Se estiver em sessão, usa ficha ativa
        sessao = sessoes_ativas.get(ctx.channel.id)
        if sessao and not nome_personagem:
            fichas_sel = sessao.get("fichas", {})
            chave = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
            ficha = fichas_personagens.get(chave) if chave else None
        else:
            chave, ficha = encontrar_ficha(ctx.author.id, nome_personagem or "")
        
        if not ficha:
            return await ctx.send("❌ Ficha não encontrada!")
        
        nome = ficha.get("nome", "Personagem")
        secoes = ficha.get("secoes", {})
        
        # Dados básicos
        basico = secoes.get("basico", {})
        nivel = basico.get("Nível", 1)
        
        if isinstance(nivel, str):
            try:
                nivel = int(nivel)
            except:
                nivel = 1
        
        # Progressão
        progressao = secoes.get("progressao", {})
        xp_atual = progressao.get("XP Atual", 0)
        xp_total = progressao.get("XP Total", 0)
        
        xp_proximo = get_xp_for_next_level(nivel)
        xp_faltando = max(0, xp_proximo - xp_atual)
        
        if xp_proximo > 0:
            porcentagem = int((xp_atual / xp_proximo) * 100)
        else:
            porcentagem = 100
        
        # Barra de progresso visual
        barra_cheia = int(porcentagem / 10)
        barra_vazia = 10 - barra_cheia
        barra = "🟩" * barra_cheia + "⬜" * barra_vazia
        
        embed = discord.Embed(
            title=f"📊 Progressão de {nome}",
            description=(
                f"**Nível Atual:** {nivel}\n"
                f"**XP Atual:** {xp_atual} / {xp_proximo}\n"
                f"**XP Total Acumulado:** {xp_total}\n\n"
                f"**Progresso para Nível {nivel + 1}:**\n"
                f"{barra} {porcentagem}%\n\n"
                f"**Faltam:** {xp_faltando} XP"
            ),
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name="darxpgrupo")
    @commands.guild_only()
    async def dar_xp_grupo(ctx: commands.Context, quantidade: int):
        """[MESTRE] Dá XP para TODOS os jogadores da sessão."""
        from config import sessoes_ativas
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Use dentro de uma sessão!")
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o **mestre** pode dar XP!")
        
        if quantidade <= 0:
            return await ctx.send("❌ Quantidade de XP deve ser positiva!")
        
        fichas_sel = sessao.get("fichas", {})
        jogadores_atualizados = []
        leveled_up = []
        
        for uid in sessao.get("jogadores", []):
            chave = fichas_sel.get(str(uid)) or fichas_sel.get(uid)
            
            if not chave or chave not in fichas_personagens:
                continue
            
            ficha = fichas_personagens[chave]
            nome_personagem = ficha.get("nome", f"Jogador {uid}")
            
            secoes = ficha.get("secoes", {})
            
            if "progressao" not in secoes:
                secoes["progressao"] = {}
            
            progressao = secoes["progressao"]
            
            xp_atual = progressao.get("XP Atual", 0)
            xp_total = progressao.get("XP Total", 0)
            
            novo_xp_atual = xp_atual + quantidade
            novo_xp_total = xp_total + quantidade
            
            progressao["XP Atual"] = novo_xp_atual
            progressao["XP Total"] = novo_xp_total
            
            # Verifica level up
            basico = secoes.get("basico", {})
            nivel_atual = basico.get("Nível", 1)
            
            if isinstance(nivel_atual, str):
                try:
                    nivel_atual = int(nivel_atual)
                except:
                    nivel_atual = 1
            
            xp_proximo_nivel = get_xp_for_next_level(nivel_atual)
            
            if novo_xp_atual >= xp_proximo_nivel and nivel_atual < 20:
                novo_nivel = nivel_atual + 1
                basico["Nível"] = novo_nivel
                progressao["XP Atual"] = novo_xp_atual - xp_proximo_nivel
                
                member = ctx.guild.get_member(uid)
                leveled_up.append((member, nome_personagem, novo_nivel))
            
            jogadores_atualizados.append(nome_personagem)
        
        from core.ficha_helpers import salvar_fichas_agora
        salvar_fichas_agora()
        
        # Mensagem de resultado
        descricao = f"✨ **Todos receberam +{quantidade} XP!**\n\n"
        descricao += f"**Jogadores:** {', '.join(jogadores_atualizados)}\n\n"
        
        if leveled_up:
            descricao += "🎉 **LEVEL UP:**\n"
            for member, nome, nivel in leveled_up:
                descricao += f"• **{nome}** → Nível {nivel}!\n"
        
        embed = discord.Embed(
            title="📊 XP Distribuído para o Grupo",
            description=descricao,
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)
