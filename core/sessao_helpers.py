# core/sessao_helpers.py
"""Funções auxiliares para o sistema de sessões de RPG."""

import discord
from typing import Dict, List, Optional, Any

SESSOES_CATEGORY_NAME = "🎲 Sessões RPG"


def user_mention(guild: discord.Guild, user_id: int) -> str:
    """Retorna mention do usuário."""
    member = guild.get_member(user_id)
    return member.mention if member else f"<@{user_id}>"


def coletar_fichas_usuario(fichas_personagens: Dict[str, Any], user_id: int) -> List[Dict[str, Any]]:
    """Retorna lista de fichas válidas do usuário."""
    fichas_validas = []
    for chave, ficha in fichas_personagens.items():
        if ficha.get("autor") == user_id and ficha.get("nome") and ficha.get("conteudo"):
            fichas_validas.append(ficha)
    return fichas_validas


def formatar_lista_fichas(fichas: List[Dict[str, Any]], SISTEMAS_DISPONIVEIS: Dict) -> str:
    """Formata lista de fichas para exibição."""
    if not fichas:
        return "— Nenhuma ficha encontrada."
    
    linhas = []
    for f in fichas[:25]:
        sistema = f.get("sistema", "dnd5e")
        sistema_nome = SISTEMAS_DISPONIVEIS.get(sistema, {}).get("nome", sistema)
        nome = f.get("nome", "Sem nome")
        linhas.append(f"• **{nome}** *(Sistema: {sistema_nome})*")
    
    if len(fichas) > 25:
        linhas.append(f"… e mais {len(fichas) - 25}")
    
    return "\n".join(linhas)


async def garantir_categoria(guild: discord.Guild) -> discord.CategoryChannel:
    """Garante que a categoria de sessões existe."""
    cat = discord.utils.get(guild.categories, name=SESSOES_CATEGORY_NAME)
    if cat:
        return cat
    return await guild.create_category(SESSOES_CATEGORY_NAME, reason="Categoria para sessões RPG")


async def criar_canal_de_sessao(
    guild: discord.Guild,
    categoria: discord.CategoryChannel,
    mestre: discord.Member,
    jogadores: List[discord.Member],
    bot_member: discord.Member,
    nome_sugerido: Optional[str] = None,
) -> tuple[discord.TextChannel, discord.VoiceChannel]:
    """Cria canal de texto E voz para a sessão."""
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        bot_member: discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True, connect=True, speak=True),
        mestre: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True, move_members=True),
    }
    
    for j in jogadores:
        overwrites[j] = discord.PermissionOverwrite(view_channel=True, send_messages=True, connect=True, speak=True)

    nome = nome_sugerido or f"sessao-{mestre.name.lower()}"
    
    text_channel = await guild.create_text_channel(name=nome, category=categoria, overwrites=overwrites)
    voice_channel = await guild.create_voice_channel(name=f"🎙️ {nome}", category=categoria, overwrites=overwrites)
    
    return text_channel, voice_channel
