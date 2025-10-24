# sistemas_comandos.py — Comandos de sistemas de RPG
import discord
from discord.ext import commands
from sistemas_rpg import SISTEMAS_DISPONIVEIS
from config import sistemas_rpg
from utils import enviar_em_partes

def register(bot: commands.Bot):

    @bot.command(name="sistema")
    async def sistema(ctx, novo_sistema: str = None):
        """Mostra ou muda SEU sistema de RPG pessoal."""
        user_id = ctx.author.id

        if novo_sistema is None:
            atual = sistemas_rpg.get(user_id, "dnd5e")
            nome = SISTEMAS_DISPONIVEIS.get(atual, {}).get("nome", "Desconhecido")
            await ctx.send(
                f"📘 **Seu sistema atual:** {nome} (`{atual}`)\n"
                f"Use `!sistema <código>` para alterar.\n"
                f"💡 Seu sistema é pessoal e será usado em todos os comandos de IA."
            )
            return

        if novo_sistema not in SISTEMAS_DISPONIVEIS:
            await ctx.send("❌ Sistema não encontrado! Use `!sistemas` para ver a lista completa.")
            return

        sistemas_rpg[user_id] = novo_sistema
        
        # ✅ CORREÇÃO: Salva imediatamente no arquivo
        from utils import salvar_dados
        salvar_dados(sistemas_rpg=sistemas_rpg)
        
        nome = SISTEMAS_DISPONIVEIS[novo_sistema]["nome"]
        await ctx.send(
            f"✅ Seu sistema foi alterado para **{nome}** (`{novo_sistema}`).\n"
            f"🎲 Todos os comandos de IA agora usarão este sistema."
        )

    @bot.command(name="sistemas")
    async def sistemas(ctx):
        """Lista todos os sistemas suportados."""
        linhas = [f"**{info['nome']}** (`{codigo}`)" for codigo, info in SISTEMAS_DISPONIVEIS.items()]
        texto = "📚 **Sistemas Suportados:**\n" + "\n".join(linhas)

        partes = enviar_em_partes(texto)  # <- CORRETO
        for parte in partes:
            await ctx.send(parte)

    @bot.command(name="buscarsistema")
    async def buscarsistema(ctx, *, termo: str = None):
        """Busca sistemas por nome."""
        if not termo:
            await ctx.send("❌ Use: `!buscarsistema <nome>`.")
            return

        resultados = [
            f"**{info['nome']}** (`{codigo}`)"
            for codigo, info in SISTEMAS_DISPONIVEIS.items()
            if termo.lower() in info["nome"].lower()
        ]

        if resultados:
            texto = "🔍 **Resultados da busca:**\n" + "\n".join(resultados)
            partes = enviar_em_partes(texto)
            for parte in partes:
                await ctx.send(parte)
        else:
            await ctx.send("❌ Nenhum sistema encontrado com esse nome.")

    @bot.command(name="infosistema")
    async def infosistema(ctx, codigo: str = None):
        """Mostra detalhes de um sistema específico."""
        if not codigo:
            await ctx.send("❌ Use: `!infosistema <código>`.")
            return

        info = SISTEMAS_DISPONIVEIS.get(codigo)
        if not info:
            await ctx.send("❌ Sistema não encontrado! Use `!sistemas` para ver todos.")
            return

        embed = discord.Embed(
            title=f"📘 {info['nome']}",
            description=(
                f"**Código:** `{codigo}`\n"
                f"**Categoria:** {info.get('categoria', 'Desconhecida')}\n"
                f"**Mecânica:** {info.get('mecanicas', 'N/A')}\n\n"
                f"**Descrição:** {info.get('descricao', 'Sem descrição disponível.')}"
            ),
            color=0x4e9bdc,
        )
        embed.add_field(name="🎲 Dados", value=", ".join(info.get("dados", [])), inline=False)
        embed.add_field(name="📊 Atributos", value=", ".join(info.get("atributos", [])), inline=False)
        embed.add_field(name="🧙 Classes", value=", ".join(info.get("classes", []))[:1020], inline=False)
        embed.set_footer(text="Use !sistema <código> para mudar o sistema deste canal.")
        await ctx.send(embed=embed)
