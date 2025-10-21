# sessoes_rpg.py
# Sistema de sessões privadas de RPG com botões e gerenciamento completo
# Compatível com a estrutura do Lyra_the_Wise_HML.py

from __future__ import annotations

import discord
from discord.ext import commands
from typing import Dict, List, Optional, Any
import asyncio
import datetime

# -----------------------------
# Estrutura de dados esperada
# -----------------------------
# sessoes_ativas[channel_id] = {
#   "guild_id": int,
#   "channel_id": int,
#   "categoria_id": Optional[int],
#   "mestre_id": int,
#   "jogadores": List[int],
#   "fichas": {user_id: chave_ficha},
#   "status": "preparando" | "em_andamento" | "pausada",
#   "sistema": "dnd5e" | "cthulhu" | ...,
#   "criada_em": iso_str
# }

SESSOES_CATEGORY_NAME = "🎲 Sessões RPG"


# -----------------------------
# Helpers
# -----------------------------

def _user_mention(guild: discord.Guild, user_id: int) -> str:
    member = guild.get_member(user_id)
    return member.mention if member else f"<@{user_id}>"


def _coletar_fichas_usuario(fichas_personagens: Dict[str, Any], user_id: int) -> List[Dict[str, Any]]:
    """Retorna a lista de fichas (dict) do usuário."""
    return [f for f in fichas_personagens.values() if f.get("autor") == user_id]


def _sistema_do_canal(sistemas_rpg: Dict[int, str], channel_id: int) -> str:
    return sistemas_rpg.get(channel_id, "dnd5e")


async def _garantir_categoria(guild: discord.Guild) -> discord.CategoryChannel:
    cat = discord.utils.get(guild.categories, name=SESSOES_CATEGORY_NAME)
    if cat:
        return cat
    return await guild.create_category(SESSOES_CATEGORY_NAME, reason="Categoria para sessões privadas de RPG")


async def _criar_canal_de_sessao(
    guild: discord.Guild,
    categoria: discord.CategoryChannel,
    mestre: discord.Member,
    jogadores: List[discord.Member],
    bot_member: discord.Member,
    nome_sugerido: Optional[str] = None,
) -> discord.TextChannel:
    # Overwrites: canal privado visível somente para mestre, jogadores e bot
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        bot_member: discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True, attach_files=True),
        mestre: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, embed_links=True),
    }
    for j in jogadores:
        overwrites[j] = discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True)

    nome = nome_sugerido or f"sessao-{mestre.name.lower()}"
    channel = await guild.create_text_channel(
        name=nome,
        category=categoria,
        overwrites=overwrites,
        reason="Criação de canal privado para sessão de RPG",
    )
    return channel


def _formatar_lista_fichas(fichas: List[Dict[str, Any]]) -> str:
    if not fichas:
        return "— Nenhuma ficha encontrada."
    linhas = []
    for f in fichas[:25]:  # limitar visual
        sistema = f.get("sistema", "dnd5e")
        nome = f.get("nome", "Sem nome")
        linhas.append(f"• **{nome}** *(sistema: {sistema})*")
    if len(fichas) > 25:
        linhas.append(f"… e mais {len(fichas) - 25}")
    return "\n".join(linhas)


def _embed_status_sessao(guild: discord.Guild, sessao: Dict[str, Any]) -> discord.Embed:
    jogadores = sessao.get("jogadores", [])
    fichas_sel = sessao.get("fichas", {})
    sistema = sessao.get("sistema", "dnd5e")
    status = sessao.get("status", "preparando")
    mestre_id = sessao.get("mestre_id")
    mestre_txt = _user_mention(guild, mestre_id)

    jogadores_txt = "\n".join(
        [f"• {_user_mention(guild, uid)} — {'✅' if str(uid) in fichas_sel or uid in fichas_sel else '⏳ sem ficha'}"
         for uid in jogadores]
    ) or "—"

    embed = discord.Embed(
        title="🎮 Sessão de RPG",
        description=f"**Sistema**: `{sistema}`\n**Status**: **{status.upper()}**\n**Mestre**: {mestre_txt}",
        color=discord.Color.purple()
    )
    embed.add_field(name="👥 Jogadores", value=jogadores_txt, inline=False)
    if fichas_sel:
        picks = []
        for k, chave in fichas_sel.items():
            uid = int(k) if isinstance(k, str) else k
            picks.append(f"• {_user_mention(guild, uid)} → **{chave.split('_', 1)[-1].replace('_',' ').title()}**")
        embed.add_field(name="🧾 Fichas Selecionadas", value="\n".join(picks)[:1024], inline=False)
    return embed


# -----------------------------
# Views (Botões)
# -----------------------------

class SessionControlView(discord.ui.View):
    def __init__(self, bot: commands.Bot, sessao_store: Dict[int, Dict[str, Any]], salvar_dados_cb, chamar_groq_cb, get_system_prompt_cb, timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.sessoes_ativas = sessao_store
        self.salvar_dados = salvar_dados_cb
        self.chamar_groq = chamar_groq_cb
        self.get_system_prompt = get_system_prompt_cb

    def _get_sessao(self, channel_id: int) -> Optional[Dict[str, Any]]:
        return self.sessoes_ativas.get(channel_id)

    def _is_mestre(self, user_id: int, sessao: Dict[str, Any]) -> bool:
        return sessao and sessao.get("mestre_id") == user_id

    @discord.ui.button(label="🎬 Iniciar Aventura", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        sessao = self._get_sessao(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada neste canal.", ephemeral=True)

        if not self._is_mestre(interaction.user.id, sessao):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode iniciar a aventura.", ephemeral=True)

        # Verifica se todos possuem fichas selecionadas
        jogadores = sessao.get("jogadores", [])
        fichas = sessao.get("fichas", {})
        faltando = [uid for uid in jogadores if str(uid) not in fichas and uid not in fichas]
        if faltando:
            faltantes_txt = ", ".join([_user_mention(interaction.guild, uid) for uid in faltando])
            return await interaction.response.send_message(f"⏳ Ainda faltam fichas: {faltantes_txt}", ephemeral=True)

        # Monta resumo das fichas selecionadas para a IA
        sistema = sessao.get("sistema", "dnd5e")
        prompt_intro = "Gere uma **introdução épica** para a sessão de RPG, apresentando o cenário, tom e conexões entre os personagens. 3-5 parágrafos curtos. Termine com um gancho claro para a primeira cena.\n\nPersonagens:\n"
        for uid, chave in fichas.items():
            # chave é "autorid_nome_slug"
            # Aqui não temos a ficha inteira, então pediremos ao canal buscar via referencia (util na integração pelo módulo pai)
            prompt_intro += f"- Jogador {uid}: personagem chave '{chave}'\n"

        # Chama IA
        mensagens = [
            {"role": "system", "content": self.get_system_prompt(sistema)},
            {"role": "user", "content": prompt_intro}
        ]
        await interaction.response.defer(thinking=True)
        intro = await self.chamar_groq(mensagens, max_tokens=900)
        sessao["status"] = "em_andamento"
        self.salvar_dados()

        embed = discord.Embed(
            title="🎬 Aventura Iniciada!",
            description=intro[:4000],
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="📊 Ver Fichas", style=discord.ButtonStyle.primary)
    async def fichas_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        sessao = self._get_sessao(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada neste canal.", ephemeral=True)

        embed = _embed_status_sessao(interaction.guild, sessao)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🚪 Encerrar Sessão", style=discord.ButtonStyle.danger)
    async def end_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        sessao = self._get_sessao(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)

        if not self._is_mestre(interaction.user.id, sessao):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode encerrar.", ephemeral=True)

        await interaction.response.send_message("⚠️ Encerrando sessão e **apagando este canal** em 5 segundos…", ephemeral=False)
        await asyncio.sleep(5)
        try:
            self.sessoes_ativas.pop(interaction.channel.id, None)
            self.salvar_dados()
            await interaction.channel.delete(reason="Sessão encerrada pelo mestre (botão).")
        except Exception:
            pass


# -----------------------------
# Setup de Comandos
# -----------------------------

def setup_sessoes(
    bot: commands.Bot,
    SISTEMAS_DISPONIVEIS: Dict[str, Any],
    fichas_personagens: Dict[str, Any],
    sistemas_rpg: Dict[int, str],
    sessoes_ativas: Dict[int, Dict[str, Any]],
    chamar_groq,
    get_system_prompt,
    salvar_dados,
):
    """Registra comandos de sessão no bot."""

    # ------------- Comando: iniciarsessao -------------
    @bot.command(name="iniciarsessao")
    @commands.guild_only()
    async def iniciarsessao(ctx: commands.Context, *membros: discord.Member):
        if not membros:
            return await ctx.send("❌ Use: `!iniciarsessao @Jogador1 @Jogador2 ...`")

        guild = ctx.guild
        mestre: discord.Member = ctx.author
        jogadores: List[discord.Member] = list(membros)
        bot_member = guild.get_member(bot.user.id)  # type: ignore

        # Categoria + canal
        categoria = await _garantir_categoria(guild)
        canal = await _criar_canal_de_sessao(
            guild=guild,
            categoria=categoria,
            mestre=mestre,
            jogadores=jogadores,
            bot_member=bot_member,
            nome_sugerido=f"sessao-{mestre.name.lower()}",
        )

        # Inicializa sessão
        sistema = _sistema_do_canal(sistemas_rpg, ctx.channel.id)
        sessoes_ativas[canal.id] = {
            "guild_id": guild.id,
            "channel_id": canal.id,
            "categoria_id": categoria.id if categoria else None,
            "mestre_id": mestre.id,
            "jogadores": [j.id for j in jogadores],
            "fichas": {},
            "status": "preparando",
            "sistema": sistema,
            "criada_em": datetime.datetime.utcnow().isoformat(),
        }
        salvar_dados()

        # Mensagem inicial com botões
        view = SessionControlView(bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt, timeout=None)

        # Construir embed com fichas de cada jogador
        descr = f"Sessão criada por {mestre.mention}.\nSistema configurado: **{SISTEMAS_DISPONIVEIS.get(sistema, {}).get('nome', sistema)}**\n\n**Jogadores convidados:**\n"
        for j in jogadores:
            descr += f"• {j.mention}\n"

        embed = discord.Embed(title="🎲 Sessão de RPG Criada!", description=descr, color=discord.Color.blurple())
        embed.add_field(
            name="🗂️ Como selecionar sua ficha",
            value="Use o comando `!selecionarficha <Nome exato>` aqui neste canal.",
            inline=False,
        )
        await canal.send(embed=embed, view=view)

        # Listar fichas por jogador
        for j in jogadores:
            fichas = _coletar_fichas_usuario(fichas_personagens, j.id)
            lista = _formatar_lista_fichas(fichas)
            await canal.send(
                embed=discord.Embed(
                    title=f"📚 Fichas de {j.display_name}",
                    description=lista,
                    color=discord.Color.dark_teal()
                )
            )

        await ctx.send(f"✅ Sessão criada com sucesso em {canal.mention}")

    # ------------- Comando: selecionarficha -------------
    @bot.command(name="selecionarficha")
    @commands.guild_only()
    async def selecionarficha(ctx: commands.Context, *, nome_personagem: str = None):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado **dentro do canal da sessão**.")
        if not nome_personagem:
            return await ctx.send("❌ Use: `!selecionarficha <Nome da Ficha>`")

        sessao = sessoes_ativas[ctx.channel.id]
        # Verifica se autor faz parte
        if ctx.author.id != sessao["mestre_id"] and ctx.author.id not in sessao["jogadores"]:
            return await ctx.send("⚠️ Você não faz parte desta sessão.")

        # Localiza ficha do usuário pelo nome
        chave_encontrada = None
        conteudo_preview = None
        for chave, ficha in fichas_personagens.items():
            if ficha.get("autor") == ctx.author.id and ficha.get("nome", "").lower() == nome_personagem.lower():
                chave_encontrada = chave
                conteudo_preview = ficha.get("conteudo", "")[:1700]
                break

        if not chave_encontrada:
            return await ctx.send("❌ Ficha não encontrada no seu perfil. Verifique o nome com `!verficha` ou `!minhasfichas`.")

        # Registra
        sessao["fichas"][str(ctx.author.id)] = chave_encontrada
        salvar_dados()

        # Mostra a ficha
        embed = discord.Embed(
            title=f"✅ Ficha Selecionada: {nome_personagem}",
            description=conteudo_preview or "—",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    # ------------- Comando: sessoes -------------
    @bot.command(name="sessoes")
    @commands.guild_only()
    async def sessoes_cmd(ctx: commands.Context):
        guild = ctx.guild
        ativos = [s for s in sessoes_ativas.values() if s.get("guild_id") == guild.id]
        if not ativos:
            return await ctx.send("— Não há sessões ativas neste servidor.")

        linhas = []
        for s in ativos[:20]:
            canal = guild.get_channel(s["channel_id"])
            mestre_txt = _user_mention(guild, s["mestre_id"])
            jogadores = s.get("jogadores", [])
            linhas.append(f"• {canal.mention if canal else '#apagado'} — Mestre: {mestre_txt} — Jogadores: {len(jogadores)} — Sistema: `{s.get('sistema')}` — Status: **{s.get('status')}**")

        embed = discord.Embed(title="📋 Sessões Ativas", description="\n".join(linhas), color=discord.Color.blurple())
        await ctx.send(embed=embed)

    # ------------- Comando: convidarsessao -------------
    @bot.command(name="convidarsessao")
    @commands.guild_only()
    async def convidarsessao(ctx: commands.Context, *novos: discord.Member):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado **no canal da sessão**.")

        sessao = sessoes_ativas[ctx.channel.id]
        if ctx.author.id != sessao["mestre_id"]:
            return await ctx.send("⚠️ Apenas o mestre pode convidar jogadores.")

        if not novos:
            return await ctx.send("❌ Use: `!convidarsessao @NovoJogador [@Outro]`")

        guild = ctx.guild
        canal: discord.TextChannel = ctx.channel  # type: ignore

        # Atualiza permissões e sessão
        adicionados = []
        for m in novos:
            try:
                await canal.set_permissions(m, view_channel=True, send_messages=True, embed_links=True)
                if m.id not in sessao["jogadores"]:
                    sessao["jogadores"].append(m.id)
                adicionados.append(m.mention)
            except Exception:
                pass

            # Lista fichas do novo jogador
            fichas = _coletar_fichas_usuario(fichas_personagens, m.id)
            await ctx.send(
                embed=discord.Embed(
                    title=f"📚 Fichas de {m.display_name}",
                    description=_formatar_lista_fichas(fichas),
                    color=discord.Color.dark_teal()
                )
            )

        salvar_dados()
        if adicionados:
            await ctx.send(f"✅ Adicionados: {', '.join(adicionados)}")

    # ------------- Comando: removerjogador -------------
    @bot.command(name="removerjogador")
    @commands.guild_only()
    async def removerjogador(ctx: commands.Context, jogador: discord.Member):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use este comando **no canal da sessão**.")

        sessao = sessoes_ativas[ctx.channel.id]
        if ctx.author.id != sessao["mestre_id"]:
            return await ctx.send("⚠️ Apenas o mestre pode remover jogadores.")

        canal: discord.TextChannel = ctx.channel  # type: ignore
        try:
            await canal.set_permissions(jogador, overwrite=None)
        except Exception:
            pass

        if jogador.id in sessao["jogadores"]:
            sessao["jogadores"].remove(jogador.id)
        sessao["fichas"].pop(str(jogador.id), None)
        salvar_dados()

        await ctx.send(f"✅ Jogador removido: {jogador.mention}")

    # ------------- Comando: mudarficha -------------
    @bot.command(name="mudarficha")
    @commands.guild_only()
    async def mudarficha(ctx: commands.Context, *, nome_personagem: str = None):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use este comando **no canal da sessão**.")
        if not nome_personagem:
            return await ctx.send("❌ Use: `!mudarficha <Nome da Ficha>`")

        sessao = sessoes_ativas[ctx.channel.id]
        em_andamento = sessao.get("status") == "em_andamento"
        mestre_id = sessao.get("mestre_id")

        # Se já iniciou, precisa de aprovação do mestre (via reação)
        if em_andamento and ctx.author.id != mestre_id:
            msg = await ctx.send(f"⚠️ {_user_mention(ctx.guild, mestre_id)}, aprova a troca de ficha de {ctx.author.mention}? ✅/❌")
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            def check(reaction: discord.Reaction, user: discord.User):
                return reaction.message.id == msg.id and str(reaction.emoji) in ["✅", "❌"] and user.id == mestre_id

            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
                if str(reaction.emoji) == "❌":
                    return await ctx.send("❌ Troca não aprovada pelo mestre.")
            except asyncio.TimeoutError:
                return await ctx.send("⏰ Tempo esgotado — troca não aprovada.")

        # Troca
        chave_encontrada = None
        for chave, ficha in fichas_personagens.items():
            if ficha.get("autor") == ctx.author.id and ficha.get("nome", "").lower() == nome_personagem.lower():
                chave_encontrada = chave
                break

        if not chave_encontrada:
            return await ctx.send("❌ Ficha não encontrada no seu perfil.")

        sessao["fichas"][str(ctx.author.id)] = chave_encontrada
        salvar_dados()
        await ctx.send(f"✅ Ficha atualizada para **{nome_personagem}**.")

    # ------------- Comando: pausarsessao -------------
    @bot.command(name="pausarsessao")
    @commands.guild_only()
    async def pausarsessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use este comando **no canal da sessão**.")
        sessao = sessoes_ativas[ctx.channel.id]
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o mestre pode pausar/retomar.")

        if sessao["status"] == "pausada":
            sessao["status"] = "em_andamento"
            salvar_dados()
            return await ctx.send(embed=discord.Embed(title="▶️ Sessão retomada", color=discord.Color.green()))

        if sessao["status"] in ("preparando", "em_andamento"):
            sessao["status"] = "pausada"
            salvar_dados()
            return await ctx.send(embed=discord.Embed(title="⏸️ Sessão pausada", color=discord.Color.orange()))

        await ctx.send("ℹ️ Estado inalterado.")

    # ------------- Comando: infosessao -------------
    @bot.command(name="infosessao")
    @commands.guild_only()
    async def infosessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado no canal da sessão.")

        sessao = sessoes_ativas[ctx.channel.id]
        embed = _embed_status_sessao(ctx.guild, sessao)
        await ctx.send(embed=embed)

    # ------------- Comando: resumosessao -------------
    @bot.command(name="resumosessao")
    @commands.guild_only()
    async def resumosessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado no canal da sessão.")

        # Captura últimas mensagens
        logs = []
        async for m in ctx.channel.history(limit=50, oldest_first=False):
            if m.author.bot:
                continue
            content = (m.content or "").strip()
            if content:
                logs.append(f"{m.author.display_name}: {content}")
        logs = list(reversed(logs))
        resumo_input = "\n".join(logs[-40:])  # limita tamanho

        sessao = sessoes_ativas[ctx.channel.id]
        sistema = sessao.get("sistema", "dnd5e")
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
            {"role": "user", "content": f"Faça um resumo narrativo (3-5 parágrafos) do seguinte chat de sessão:\n\n{resumo_input}"}
        ]

        await ctx.send("🧠 Gerando resumo com IA…")
        texto = await chamar_groq(mensagens, max_tokens=800)
        await ctx.send(embed=discord.Embed(title="📝 Resumo da Sessão", description=texto[:4000], color=discord.Color.purple()))

    # ------------- Comando: ajudasessao -------------
    @bot.command(name="ajudasessao")
    async def ajudasessao(ctx: commands.Context):
        descr = (
            "**Comandos principais**\n"
            "• `!iniciarsessao @jog1 @jog2` — Cria sessão privada\n"
            "• `!selecionarficha Nome` — Escolhe sua ficha\n"
            "• `!sessoes` — Lista sessões ativas\n"
            "• `!infosessao` — Detalhes da sessão atual\n"
            "• `!resumosessao` — Resumo com IA das últimas mensagens\n"
            "• `!convidarsessao @Novo` — Adiciona jogador\n"
            "• `!removerjogador @Jog` — Remove jogador\n"
            "• `!mudarficha Nome` — Troca de personagem\n"
            "• `!pausarsessao` — Pausa/retoma\n\n"
            "**Botões no canal da sessão**\n"
            "• 🎬 Iniciar Aventura — Inicia a narrativa (mestre)\n"
            "• 📊 Ver Fichas — Mostra status das seleções\n"
            "• 🚪 Encerrar Sessão — Apaga o canal (mestre)"
        )
        await ctx.send(embed=discord.Embed(title="📖 Ajuda — Sessões de RPG", description=descr, color=discord.Color.blurple()))

    # Fim do setup
    return
