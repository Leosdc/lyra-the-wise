# documentacao.py — versão final com prevenção de duplicata
import discord
from discord.ext import commands

DOCUMENTACAO_COMPLETA = """📘 RPG Master Bot — Documentação Completa

O RPG Master Bot gerencia mesas de RPG no Discord, com fichas, sessões, rolagens e IA.

⚙️ Configuração
!sistema, !sistemas, !buscarsistema, !infosistema, !limpar

🎲 Dados & Iniciativa
!rolar, !r, !iniciativa

👤 Fichas & Personagens
!ficha, !criarficha, !verficha, !editarficha, !deletarficha,
!converterficha, !minhasfichas, !exportarficha

⚔️ Combate & Conteúdo
!monstro, !encontro, !armadilha, !item, !tesouro, !puzzle, !vilao, !plot, !cena

🎮 Sessões
!iniciarsessao, !sessoes, !infosessao, !convidarsessao,
!removerjogador, !selecionarficha, !resumosessao, !pausarsessao, !ajudasessao

🧠 Administração
!stats, !backup, !reload, !documentacao, !ajuda, !suporte, !troubleshoot

💬 IA
!mestre <texto> — conversa com o Mestre de RPG com contexto do canal."""

def register(bot: commands.Bot):
    # Remove versões antigas do comando se já existirem
    if "documentacao" in bot.all_commands:
        bot.remove_command("documentacao")

    @bot.command(name="documentacao")
    async def documentacao(ctx):
        """Exibe a documentação completa do bot."""
        texto = DOCUMENTACAO_COMPLETA
        if len(texto) <= 2000:
            await ctx.send(texto)
        else:
            partes = [texto[i:i+2000] for i in range(0, len(texto), 2000)]
            for parte in partes:
                await ctx.send(parte)
