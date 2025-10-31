# commands/sessoes_commands.py
"""Comandos do sistema de sessões de RPG."""

import discord
from discord.ext import commands
import datetime
import asyncio

from core.sessao_helpers import (
    user_mention, coletar_fichas_usuario, formatar_lista_fichas,
    garantir_categoria, criar_canal_de_sessao
)
from views.sessao_control_views import SessionControlView


def register_sessoes_commands(
    bot: commands.Bot,
    SISTEMAS_DISPONIVEIS,
    fichas_personagens,
    sistemas_rpg,
    sessoes_ativas,
    chamar_groq,
    get_system_prompt,
    salvar_dados,
):
    """Registra todos os comandos de sessão."""

    @bot.command(name="iniciarsessao")
    @commands.guild_only()
    async def iniciarsessao(ctx: commands.Context, *membros: discord.Member):
        if not membros:
            return await ctx.send("❌ Use: `!iniciarsessao @Jogador1 @Jogador2 ...`")

        guild = ctx.guild
        mestre = ctx.author
        jogadores = list(membros)
        bot_member = guild.get_member(bot.user.id)

        categoria = await garantir_categoria(guild)
        canal_texto, canal_voz = await criar_canal_de_sessao(guild, categoria, mestre, jogadores, bot_member, f"sessao-{mestre.name.lower()}")

        # Move jogadores para voz
        movidos, nao_movidos = [], []
        for jogador in [mestre] + jogadores:
            if jogador.voice and jogador.voice.channel:
                try:
                    await jogador.move_to(canal_voz)
                    await jogador.edit(mute=False, deafen=False)
                    movidos.append(jogador.mention)
                except Exception:
                    nao_movidos.append(jogador.mention)
            else:
                nao_movidos.append(jogador.mention)

        sistema = sistemas_rpg.get(mestre.id, "dnd5e")
        sessoes_ativas[canal_texto.id] = {
            "guild_id": guild.id,
            "channel_id": canal_texto.id,
            "voice_channel_id": canal_voz.id,
            "categoria_id": categoria.id,
            "mestre_id": mestre.id,
            "jogadores": [j.id for j in jogadores],
            "fichas": {},
            "status": "preparando",
            "sistema": sistema,
            "criada_em": datetime.datetime.utcnow().isoformat(),
            "historia": [],
        }
        salvar_dados()

        view = SessionControlView(bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt, timeout=None)
        sistema_nome = SISTEMAS_DISPONIVEIS.get(sistema, {}).get('nome', sistema)
        
        embed = discord.Embed(
            title="🎲 Sessão de RPG Criada!",
            description=f"Mestre: {mestre.mention}\nSistema: **{sistema_nome}**\n\n**Jogadores:**\n" + "\n".join([f"• {j.mention}" for j in jogadores]),
            color=discord.Color.blurple()
        )
        embed.add_field(name="🗂️ Selecionar Ficha", value="Use `!selecionarficha <Nome>`", inline=False)
        embed.add_field(name="🎙️ Canal de Voz", value=f"{canal_voz.mention} criado!", inline=False)

        await canal_texto.send(embed=embed, view=view)
        
        if movidos:
            await canal_texto.send(f"✅ Movidos: {', '.join(movidos)}")
        if nao_movidos:
            await canal_texto.send(f"⚠️ Entrem manualmente: {', '.join(nao_movidos)}")

        # Lista fichas de cada jogador
        for j in jogadores:
            fichas = coletar_fichas_usuario(fichas_personagens, j.id)
            if fichas:
                await canal_texto.send(embed=discord.Embed(
                    title=f"📚 Fichas de {j.display_name}",
                    description=formatar_lista_fichas(fichas, SISTEMAS_DISPONIVEIS),
                    color=discord.Color.dark_teal()
                ))

        await ctx.send(f"✅ Sessão criada! {canal_texto.mention}")

    @bot.command(name="selecionarficha")
    @commands.guild_only()
    async def selecionarficha(ctx: commands.Context, *, nome_personagem: str = None):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use dentro do canal da sessão.")
        if not nome_personagem:
            return await ctx.send("❌ Use: `!selecionarficha <Nome>`")

        sessao = sessoes_ativas[ctx.channel.id]
        chave_encontrada = None
        
        for chave, ficha in fichas_personagens.items():
            if ficha.get("autor") == ctx.author.id and ficha.get("nome", "").lower() == nome_personagem.lower():
                chave_encontrada = chave
                break

        if not chave_encontrada:
            return await ctx.send("❌ Ficha não encontrada.")

        sessao["fichas"][str(ctx.author.id)] = chave_encontrada
        salvar_dados()
        await ctx.send(f"✅ Ficha **{nome_personagem}** selecionada!")

        # Notifica quantos jogadores já selecionaram
        jogadores_total = len(sessao.get("jogadores", []))
        fichas_selecionadas = len(sessao.get("fichas", {}))

        if fichas_selecionadas >= jogadores_total:
            await ctx.send("🎉 **Todos os jogadores selecionaram suas fichas!** O mestre pode iniciar a aventura.")
        else:
            faltam = jogadores_total - fichas_selecionadas
            await ctx.send(f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} selecionar ficha...")

    @bot.command(name="sessoes")
    @commands.guild_only()
    async def sessoes_cmd(ctx: commands.Context):
        guild = ctx.guild
        ativos = [s for s in sessoes_ativas.values() if s.get("guild_id") == guild.id]
        if not ativos:
            return await ctx.send("— Não há sessões ativas.")

        linhas = []
        for s in ativos[:20]:
            canal = guild.get_channel(s["channel_id"])
            mestre = user_mention(guild, s["mestre_id"])
            linhas.append(f"• {canal.mention if canal else '#apagado'} — Mestre: {mestre} — Sistema: `{s.get('sistema')}`")

        await ctx.send(embed=discord.Embed(title="📋 Sessões Ativas", description="\n".join(linhas), color=discord.Color.blurple()))

    @bot.command(name="pausarsessao")
    @commands.guild_only()
    async def pausarsessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use no canal da sessão.")
        
        sessao = sessoes_ativas[ctx.channel.id]
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o mestre pode pausar.")

        if sessao["status"] == "pausada":
            sessao["status"] = "em_andamento"
            salvar_dados()
            return await ctx.send(embed=discord.Embed(title="▶️ Sessão retomada", color=discord.Color.green()))
        else:
            sessao["status"] = "pausada"
            salvar_dados()
            return await ctx.send(embed=discord.Embed(title="⏸️ Sessão pausada", color=discord.Color.orange()))

    @bot.command(name="resumosessao")
    @commands.guild_only()
    async def resumosessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use no canal da sessão.")

        logs = []
        async for m in ctx.channel.history(limit=50, oldest_first=False):
            if not m.author.bot and m.content:
                logs.append(f"{m.author.display_name}: {m.content}")
        
        logs = list(reversed(logs))[:40]
        resumo_input = "\n".join(logs)

        sessao = sessoes_ativas[ctx.channel.id]
        sistema = sessao.get("sistema", "dnd5e")
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
            {"role": "user", "content": f"Faça um resumo narrativo (3-5 parágrafos):\n\n{resumo_input}"}
        ]

        await ctx.send("🧠 Gerando resumo...")
        texto = await chamar_groq(mensagens, max_tokens=800)
        await ctx.send(embed=discord.Embed(title="📝 Resumo da Sessão", description=texto[:4000], color=discord.Color.purple()))
