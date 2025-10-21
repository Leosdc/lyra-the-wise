# utilidades.py — comandos utilitários e administrativos (sem duplicatas)
import os
import discord
from discord.ext import commands
from datetime import datetime
import psutil
import platform
import shutil

def register(bot: commands.Bot):

    @bot.command(name="stats")
    async def stats(ctx):
        """Mostra estatísticas do bot."""
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / 1024**2
        cpu = psutil.cpu_percent()
        uptime = datetime.now() - datetime.fromtimestamp(process.create_time())

        embed = discord.Embed(
            title="📊 Estatísticas do Bot",
            color=discord.Color.blue()
        )
        embed.add_field(name="🧠 CPU", value=f"{cpu:.1f}%", inline=True)
        embed.add_field(name="💾 Memória", value=f"{mem:.1f} MB", inline=True)
        embed.add_field(name="⏱️ Uptime", value=str(uptime).split('.')[0], inline=True)
        embed.add_field(name="💻 Sistema", value=platform.system(), inline=True)
        embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
        embed.add_field(name="📡 Discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="🎲 Servidores", value=str(len(bot.guilds)), inline=True)
        embed.add_field(name="👥 Usuários", value=str(len(bot.users)), inline=True)
        embed.set_footer(text=f"Servidor: {ctx.guild.name if ctx.guild else 'DM'}")
        await ctx.send(embed=embed)

    @bot.command(name="backup")
    @commands.is_owner()
    async def backup(ctx):
        """Cria backup manual dos dados."""
        try:
            await ctx.send("💾 Criando backup...")
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            
            # Cria backup apenas da pasta bot_data
            shutil.make_archive("backup_temp", 'zip', "bot_data")
            os.rename("backup_temp.zip", backup_name)
            
            await ctx.send("✅ Backup criado com sucesso!", file=discord.File(backup_name))
            
            # Remove o arquivo após enviar
            os.remove(backup_name)
        except Exception as e:
            await ctx.send(f"❌ Erro ao criar backup: {e}")

    @bot.command(name="ajuda")
    async def ajuda(ctx):
        """Mostra comandos básicos do bot."""
        msg = (
            "🤖 **Comandos principais do RPG Master Bot:**\n\n"
            "📚 **Ajuda e Informações**\n"
            "• `!rpghelp` — Painel completo de comandos (recomendado)\n"
            "• `!documentacao` — Documentação detalhada\n"
            "• `!ajuda` — Esta mensagem\n"
            "• `!stats` — Estatísticas do sistema\n\n"
            "🎲 **Início Rápido**\n"
            "• `!sistema` — Ver sistema atual\n"
            "• `!sistemas` — Lista todos os sistemas\n"
            "• `!ficha <nome>` — Criar ficha automática\n"
            "• `!rolar 2d6+3` — Rolar dados\n"
            "• `!mestre <pergunta>` — Assistente de IA\n\n"
            "🎮 **Sessões de RPG**\n"
            "• `!iniciarsessao @jogador1 @jogador2` — Criar sessão privada\n"
            "• `!ajudasessao` — Guia completo de sessões\n\n"
            "💡 **Dica:** Use `!rpghelp` para ver todos os comandos organizados por categoria!"
        )
        await ctx.send(embed=discord.Embed(
            title="🆘 Ajuda Rápida",
            description=msg,
            color=discord.Color.green()
        ))

    @bot.command(name="suporte")
    async def suporte(ctx):
        """Link de suporte ou contato."""
        embed = discord.Embed(
            title="📨 Suporte do RPG Master Bot",
            description=(
                "Precisa de ajuda ou encontrou um bug?\n\n"
                "**Opções de suporte:**\n"
                "• Use `!rpghelp` para ver todos os comandos\n"
                "• Use `!documentacao` para ver a documentação completa\n"
                "• Entre em contato com o desenvolvedor\n\n"
                "**Desenvolvedor:** Leosdc_#0001\n"
                "**GitHub:** https://github.com/leosdcdev/RPGMasterBot"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Obrigado por usar o RPG Master Bot! 🎲")
        await ctx.send(embed=embed)

    @bot.command(name="sobre")
    async def sobre(ctx):
        """Informações sobre o bot."""
        embed = discord.Embed(
            title="🎲 RPG Master Bot",
            description=(
                "Um assistente completo para mestres e jogadores de RPG de mesa!\n\n"
                "**Recursos principais:**\n"
                "• 50+ sistemas de RPG suportados\n"
                "• Geração de fichas com IA\n"
                "• Sessões privadas com canais dedicados\n"
                "• Assistente de mestre inteligente\n"
                "• Sistema de rolagem de dados completo\n"
                "• Geração de NPCs, monstros, itens e mais\n\n"
                "**Comandos úteis:**\n"
                "• `!rpghelp` — Ver todos os comandos\n"
                "• `!sistemas` — Ver sistemas suportados\n"
                "• `!stats` — Estatísticas do bot"
            ),
            color=discord.Color.purple()
        )
        embed.add_field(
            name="🔧 Tecnologias",
            value="Python • Discord.py • Groq AI • Llama 3.3",
            inline=False
        )
        embed.add_field(
            name="📊 Estatísticas",
            value=f"Servidores: {len(bot.guilds)} • Usuários: {len(bot.users)}",
            inline=False
        )
        embed.set_footer(text="Desenvolvido por Leosdc_ • Versão 2.0")
        await ctx.send(embed=embed)

    print("✅ utilidades carregado com sucesso!")