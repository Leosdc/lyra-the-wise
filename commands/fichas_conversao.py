# commands/fichas_conversao.py
"""Comandos de conversão e exportação de fichas."""

import discord
from discord.ext import commands
import json
import os

from config import fichas_personagens, sistemas_rpg
from sistemas_rpg import SISTEMAS_DISPONIVEIS, resolver_alias
from utils import chamar_groq, get_system_prompt
from core.ficha_helpers import salvar_fichas_agora, encontrar_ficha
from views.ficha_views import FichaNavigationView


def register_fichas_conversao_commands(bot: commands.Bot):
    """Registra comandos de conversão e exportação."""

    @bot.command(name="converterficha")
    async def converter_ficha(ctx, novo_sistema: str, *, nome_personagem: str = None):
        """Converte ficha entre sistemas mantendo conceito."""
        if not nome_personagem:
            await ctx.send("❌ Use: `!converterficha <sistema> <nome>`\n💡 Exemplo: `!converterficha cthulhu Thorin`")
            return

        novo_sistema_original = novo_sistema
        novo_sistema = resolver_alias(novo_sistema.lower())
        
        if novo_sistema not in SISTEMAS_DISPONIVEIS:
            await ctx.send(f"❌ Sistema `{novo_sistema_original}` inválido.\n💡 Use `!sistemas` para ver todos disponíveis.")
            return

        chave, ficha = encontrar_ficha(ctx.author.id, nome_personagem)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome_personagem}' não encontrada!")
            return

        atual = ficha.get("sistema", "dnd5e")
        if atual == novo_sistema:
            await ctx.send("⚠️ A ficha já é desse sistema.")
            return

        await ctx.send(f"🔄 Convertendo **{ficha['nome']}** de {SISTEMAS_DISPONIVEIS[atual]['nome']} para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}...")

        # Extrai dados da ficha original
        if "secoes" in ficha and ficha["secoes"]:
            # Ficha estruturada - extrai dados-chave
            secoes_orig = ficha["secoes"]
            dados_basicos = secoes_orig.get("basico", {})
            atributos = secoes_orig.get("atributos", {})
            historia_secao = secoes_orig.get("historia", {})
            
            descricao_personagem = f"""
Personagem: {ficha['nome']}
Conceito: {dados_basicos.get('Classe', dados_basicos.get('Arquétipo', 'Aventureiro'))}
Raça/Tipo: {dados_basicos.get('Raça', dados_basicos.get('Metatipo', dados_basicos.get('Clã', 'Humano')))}
Atributos principais: {', '.join([f'{k}:{v}' for k, v in list(atributos.items())[:3]])}
Personalidade: {historia_secao.get('Personalidade', 'A definir')}
História: {historia_secao.get('História', historia_secao.get('Background', 'A definir'))}
"""
        else:
            # Ficha em formato texto - usa conteúdo direto
            descricao_personagem = f"Ficha original:\n{ficha.get('conteudo', '')[:500]}"

        # Monta prompt de conversão
        prompt = f"""Converta o seguinte personagem de {SISTEMAS_DISPONIVEIS[atual]['nome']} para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}.

IMPORTANTE: Mantenha o CONCEITO, PERSONALIDADE e PODER RELATIVO do personagem, mas adapte completamente as mecânicas para o novo sistema.

{descricao_personagem}

Retorne a ficha COMPLETA no formato JSON estruturado:

{{
  "basico": {{}},
  "atributos": {{}},
  "recursos": {{}},
  "combate": {{}},
  "equipamento": {{}},
  "magia": {{}},
  "historia": {{}}
}}

Preencha TODOS os campos apropriados para {SISTEMAS_DISPONIVEIS[novo_sistema]['nome']}. Seja balanceado e completo."""

        historico = [
            {"role": "system", "content": get_system_prompt(novo_sistema)},
            {"role": "user", "content": prompt},
        ]

        convertido = await chamar_groq(historico, max_tokens=2000)
        
        if not convertido or "Erro" in convertido:
            await ctx.send(f"⚠️ Erro ao converter ficha via IA: {convertido}")
            return

        # Tenta parsear JSON estruturado
        try:
            conteudo_limpo = convertido.strip()
            if conteudo_limpo.startswith("```"):
                conteudo_limpo = conteudo_limpo.split("```")[1]
                if conteudo_limpo.startswith("json"):
                    conteudo_limpo = conteudo_limpo[4:]
            
            secoes_convertidas = json.loads(conteudo_limpo)
        except json.JSONDecodeError:
            # Se falhar, usa formato texto mas avisa
            secoes_convertidas = {}
            await ctx.send("⚠️ Conversão em formato texto. Recomendo recriar com `!criarficha`.")

        # Cria nova ficha convertida
        from utils import key_from_name
        
        nome_sistema = SISTEMAS_DISPONIVEIS[novo_sistema]['nome'].strip()
        novo_nome = f"{ficha['nome']} ({nome_sistema})"
        nova_chave = key_from_name(f"{ctx.author.id}_{novo_nome}")

        fichas_personagens[nova_chave] = {
            "nome": novo_nome,
            "sistema": novo_sistema,
            "autor": ctx.author.id,
            "convertida_de": atual,
            "secoes": secoes_convertidas,
            "conteudo": convertido  # Backup
        }

        if salvar_fichas_agora():
            print(f"✅ Ficha convertida '{novo_nome}' salva para user {ctx.author.id}")
        else:
            await ctx.send("⚠️ Aviso: A conversão foi feita mas pode não ter sido salva corretamente.")

        # Mostra resultado com navegação
        if secoes_convertidas:
            view = FichaNavigationView(fichas_personagens[nova_chave], novo_sistema)
            await ctx.send(
                embed=view.get_embed(),
                view=view
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="✅ Ficha Convertida!",
                    description=f"Nova ficha: **{novo_nome}**\n\n{convertido[:3000]}",
                    color=discord.Color.green(),
                ).set_footer(text="Use !verficha para visualizar com navegação")
            )

    @bot.command(name="exportarficha")
    async def exportar_ficha(ctx, *, nome: str = None):
        """Exporta ficha como JSON."""
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
        os.remove(arquivo)