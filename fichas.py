# fichas.py — corrigido e compatível com nova estrutura
import re
import json
import discord
from discord.ext import commands
from utils import (
    chamar_groq, get_system_prompt, salvar_dados, key_from_name
)
from config import fichas_personagens, sistemas_rpg
from sistemas_rpg import SISTEMAS_DISPONIVEIS, resolver_alias


def encontrar_ficha(user_id, nome):
    nome_proc = re.sub(r'[^a-z0-9_]+', '', nome.lower())
    for k, v in fichas_personagens.items():
        if v.get("autor") == user_id:
            nome_limpo = re.sub(r'[^a-z0-9_]+', '', v["nome"].lower())
            if nome_proc in nome_limpo or nome_limpo in nome_proc:
                return k, v
    return None, None


def register(bot: commands.Bot):
    # Remove comandos duplicados antes de registrar novamente
    for cmd in [
        "ficha", "criarficha", "verficha", "editarficha", "deletarficha",
        "minhasfichas", "converterficha", "exportarficha"
    ]:
        try:
            bot.remove_command(cmd)
        except Exception:
            pass

    @bot.command(name="ficha")
    async def ficha_cmd(ctx, *, nome: str = None):
        if not nome:
            await ctx.send("❌ Use `!ficha <nome>` para criar uma ficha automática.")
            return

        sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        system_prompt = get_system_prompt(sistema)

        # CORREÇÃO: Monta o histórico CORRETAMENTE como lista
        historico = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Crie uma ficha de personagem completa para o sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']} chamada {nome}."}
        ]

        await ctx.send(f"📝 Criando ficha de **{nome}** em {SISTEMAS_DISPONIVEIS[sistema]['nome']}...")

        # CORREÇÃO: Passa apenas historico (que já é uma lista) e max_tokens
        conteudo = await chamar_groq(historico, max_tokens=1200)
        
        if not conteudo or "Erro" in conteudo:
            await ctx.send(f"⚠️ Ocorreu um erro ao consultar a IA: {conteudo}")
            return

        chave = key_from_name(f"{ctx.author.id}_{nome}")

        fichas_personagens[chave] = {
            "nome": nome,
            "sistema": sistema,
            "conteudo": conteudo,
            "autor": ctx.author.id
        }
        salvar_dados()

        await ctx.send(
            embed=discord.Embed(
                title=f"✅ Ficha criada: {nome}",
                description=conteudo[:4000],
                color=discord.Color.green(),
            )
        )

    @bot.command(name="minhasfichas")
    async def minhas_fichas(ctx, sistema: str = None):
        user_id = ctx.author.id
        fichas_user = {k: v for k, v in fichas_personagens.items() if v.get("autor") == user_id}
        if not fichas_user:
            await ctx.send("❌ Você não tem fichas salvas ainda.")
            return

        if sistema:
            sistema = resolver_alias(sistema.lower())
            fichas_user = {k: v for k, v in fichas_user.items() if v.get("sistema") == sistema}

        total = len(fichas_user)
        sistemas_dict = {}
        for f in fichas_user.values():
            sistemas_dict.setdefault(f["sistema"], []).append(f)

        descricao = f"Total: {total} ficha(s)\n\n"
        for s, lista in sistemas_dict.items():
            descricao += f"🎲 {SISTEMAS_DISPONIVEIS[s]['nome']} ({len(lista)})\n"
            for f in lista:
                nome = f['nome']
                if f.get("convertida_de"):
                    nome += " (convertida)"
                descricao += f"• {nome}\n"
            descricao += "\n"

        await ctx.send(
            embed=discord.Embed(
                title="📚 Suas Fichas de Personagem",
                description=descricao[:4000],
                color=discord.Color.blurple(),
            ).set_footer(text="Use !verficha <nome> • !converterficha <sistema> <nome>")
        )

    @bot.command(name="verficha")
    async def ver_ficha(ctx, *, nome: str = None):
        if not nome:
            await ctx.send("❌ Use `!verficha <nome>`.")
            return
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
            return

        embed = discord.Embed(
            title=f"📜 {ficha['nome']} ({SISTEMAS_DISPONIVEIS[ficha['sistema']]['nome']})",
            description=ficha["conteudo"][:4000],
            color=discord.Color.gold(),
        )
        await ctx.send(embed=embed)

    @bot.command(name="deletarficha")
    async def deletar_ficha(ctx, *, nome: str = None):
        if not nome:
            await ctx.send("❌ Use `!deletarficha <nome>`.")
            return
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
            return

        del fichas_personagens[chave]
        salvar_dados()
        await ctx.send(f"🗑️ Ficha **{ficha['nome']}** deletada com sucesso.")

    @bot.command(name="converterficha")
    async def converter_ficha(ctx, novo_sistema: str, *, nome_personagem: str = None):
        if not nome_personagem:
            await ctx.send("❌ Use: `!converterficha <sistema> <nome>`")
            return

        novo_sistema = resolver_alias(novo_sistema.lower())
        if novo_sistema not in SISTEMAS_DISPONIVEIS:
            await ctx.send("❌ Sistema inválido.")
            return

        chave, ficha = encontrar_ficha(ctx.author.id, nome_personagem)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada!")
            return

        atual = ficha.get("sistema", "dnd5e")
        if atual == novo_sistema:
            await ctx.send("⚠️ A ficha já é desse sistema.")
            return

        await ctx.send(f"🔄 Convertendo **{ficha['nome']}** para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}...")

        prompt = f"""Converta a ficha a seguir de {SISTEMAS_DISPONIVEIS[atual]['nome']} para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']} mantendo conceito e poder.

FICHA ORIGINAL:
{ficha['conteudo']}
"""

        # CORREÇÃO: Passa historico como lista
        historico = [
            {"role": "system", "content": get_system_prompt(novo_sistema)},
            {"role": "user", "content": prompt},
        ]

        convertido = await chamar_groq(historico, max_tokens=1200)
        
        if not convertido or "Erro" in convertido:
            await ctx.send(f"⚠️ Erro ao converter ficha via IA: {convertido}")
            return

        novo_nome = f"{ficha['nome']} ({SISTEMAS_DISPONIVEIS[novo_sistema]['nome'][:10]})"
        nova_chave = key_from_name(f"{ctx.author.id}_{novo_nome}")

        fichas_personagens[nova_chave] = {
            "nome": novo_nome,
            "sistema": novo_sistema,
            "conteudo": convertido,
            "autor": ctx.author.id,
            "convertida_de": atual,
        }

        salvar_dados()
        await ctx.send(
            embed=discord.Embed(
                title="✅ Ficha Convertida!",
                description=f"Nova ficha: **{novo_nome}**\n\n{convertido[:3000]}",
                color=discord.Color.green(),
            )
        )

    @bot.command(name="exportarficha")
    async def exportar_ficha(ctx, *, nome: str = None):
        if not nome:
            await ctx.send("❌ Use `!exportarficha <nome>`.")
            return
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send("❌ Ficha não encontrada.")
            return

        json_data = json.dumps(ficha, indent=2, ensure_ascii=False)
        arquivo = f"{ficha['nome']}.json"
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(json_data)

        await ctx.send("📦 Ficha exportada!", file=discord.File(arquivo))
        
        # Remove o arquivo temporário
        import os
        os.remove(arquivo)

    print("✅ fichas carregado com sucesso!")