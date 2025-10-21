# admin.py — módulo administrativo com reload e troubleshoot
import importlib
import traceback
from discord.ext import commands

def register(bot: commands.Bot):

    @bot.command(name="reload")
    @commands.is_owner()
    async def reload(ctx, module: str):
        """Recarrega dinamicamente um módulo do bot."""
        try:
            importlib.reload(__import__(module))
            await ctx.send(f"✅ Módulo `{module}` recarregado com sucesso!")
        except Exception as e:
            await ctx.send(f"❌ Erro ao recarregar {module}: {e}")
            traceback.print_exc()

    @bot.command(name="troubleshoot")
    @commands.is_owner()
    async def troubleshoot(ctx):
        """Executa diagnóstico em todos os comandos do bot."""
        await ctx.send("🔍 Iniciando diagnóstico dos comandos...")

        resultados = []
        total = 0
        erros = 0

        for nome, comando in bot.all_commands.items():
            total += 1
            try:
                # Verifica se o callback é válido
                if not callable(comando.callback):
                    erros += 1
                    resultados.append(f"⚠️ {nome}: callback inválido")
                    continue

                # Checa se há docstring
                if not comando.callback.__doc__:
                    resultados.append(f"ℹ️ {nome}: sem docstring (não é erro)")

                # Checa parâmetros válidos
                if not hasattr(comando, "params"):
                    erros += 1
                    resultados.append(f"❌ {nome}: não possui parâmetros válidos")

            except Exception as e:
                erros += 1
                resultados.append(f"❌ {nome}: erro ao verificar → {e}")

        resumo = f"✅ {total - erros} OK / ❌ {erros} com problemas\nTotal: {total} comandos"
        msg = "\n".join(resultados[:30])
        if len(resultados) > 30:
            msg += f"\n... (+{len(resultados) - 30} mais ocultos)"

        await ctx.send(f"🧩 **Diagnóstico completo:**\n{resumo}\n\n```{msg}```")
