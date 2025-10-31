# commands/fichas_crud.py
"""Comandos básicos de CRUD de fichas (criar, ver, listar, deletar)."""

import discord
from discord.ext import commands
import json

from config import fichas_personagens, sistemas_rpg
from sistemas_rpg import SISTEMAS_DISPONIVEIS
from utils import chamar_groq, get_system_prompt, key_from_name
from core.ficha_helpers import salvar_fichas_agora, encontrar_ficha, get_estrutura_ficha
from views.ficha_views import FichaNavigationView


def register_fichas_crud_commands(bot: commands.Bot):
    """Registra comandos básicos de fichas (CRUD)."""

    @bot.command(name="ficha")
    async def ficha_cmd(ctx, *, nome: str = None):
        """Cria ficha rápida ESTRUTURADA com IA."""
        if not nome:
            await ctx.send("❌ Use `!ficha <nome>` para criação rápida ou `!criarficha` para modo interativo estruturado.")
            return

        sistema = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema)
        estrutura = get_estrutura_ficha(sistema)
        sistema_nome = SISTEMAS_DISPONIVEIS[sistema]['nome']

        await ctx.send(f"📝 Criando ficha estruturada de **{nome}** em {sistema_nome}...")

        # Gera exemplo JSON dinâmico baseado na estrutura
        exemplo_secoes = []
        for secao in estrutura["secoes"]:
            campos = estrutura["campos"][secao]
            campos_exemplo = {campo: f"[preencher {campo}]" for campo in campos}
            exemplo_secoes.append(f'  "{secao}": {json.dumps(campos_exemplo, ensure_ascii=False, indent=4)}')
        
        exemplo_json = "{\n" + ",\n".join(exemplo_secoes) + "\n}"

        prompt = f"""Crie uma ficha de personagem COMPLETA e BALANCEADA para {sistema_nome}.

**PERSONAGEM:** {nome}

**INSTRUÇÕES OBRIGATÓRIAS:**
1. PREENCHA 100% dos campos - NUNCA deixe vazio, com "—" ou "A definir"
2. Crie valores apropriados para o sistema {sistema_nome}
3. Seja criativo mas coerente com as regras do sistema
4. História deve ter 3-4 parágrafos completos
5. Todos os valores numéricos devem ser calculados corretamente

**USE ESTA ESTRUTURA JSON EXATA:**

{exemplo_json}

**REGRAS:**
- Nome do personagem: {nome}
- TODOS os campos devem ter valores reais e completos
- Use terminologia correta do sistema
- Seja detalhado em descrições e história
- Calcule valores numéricos apropriados

**RETORNE APENAS O JSON - SEM MARKDOWN, SEM TEXTO EXTRA.**"""

        historico = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        conteudo_bruto = await chamar_groq(historico, max_tokens=2500)
        
        # Parser JSON MUITO MAIS ROBUSTO
        secoes_estruturadas = None
        parse_success = False
        
        try:
            import re
            conteudo_limpo = conteudo_bruto.strip()
            
            # 1. Remove markdown (```json ou ```)
            if "```" in conteudo_limpo:
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', conteudo_limpo, re.DOTALL)
                if json_match:
                    conteudo_limpo = json_match.group(1)
            
            # 2. Extrai apenas o JSON (encontra primeiro { até último })
            inicio = conteudo_limpo.find('{')
            fim = conteudo_limpo.rfind('}') + 1
            if inicio >= 0 and fim > inicio:
                conteudo_limpo = conteudo_limpo[inicio:fim]
            
            # 3. Tenta parsear diretamente
            secoes_estruturadas = json.loads(conteudo_limpo)
            
            # 4. Valida que não está vazio
            if not isinstance(secoes_estruturadas, dict) or not secoes_estruturadas:
                raise ValueError("JSON vazio ou inválido")
            
            # 5. Valida que tem pelo menos 3 seções válidas
            secoes_validas = sum(1 for v in secoes_estruturadas.values() if isinstance(v, dict) and v)
            if secoes_validas < 3:
                raise ValueError(f"Apenas {secoes_validas} seções válidas encontradas")
            
            parse_success = True
            print(f"✅ Ficha estruturada criada: {len(secoes_estruturadas)} seções, {secoes_validas} válidas")
            
        except Exception as e:
            print(f"⚠️ Erro ao parsear JSON: {e}")
            print(f"Conteúdo recebido (primeiros 500 chars): {conteudo_bruto[:500]}...")
            parse_success = False
        
        # FALLBACK INTELIGENTE - Gera ficha completa via segunda chamada à IA
        if not parse_success or not secoes_estruturadas:
            await ctx.send("⚙️ Ajustando abordagem... gerando ficha completa...")
            
            # Prompt mais direto e específico
            fallback_prompt = f"""Crie uma ficha COMPLETA para {nome} em {sistema_nome}.

Retorne APENAS este formato JSON (sem markdown, sem explicações):

{{
  "basico": {{
    "Nome": "{nome}",
    "Raça": "[escolha uma raça apropriada]",
    "Classe": "[escolha uma classe apropriada]",
    "Nível": 3,
    "Conceito": "[conceito em 1 frase]"
  }},
  "atributos": {{
    "Força": [8-18],
    "Destreza": [8-18],
    "Constituição": [8-18],
    "Inteligência": [8-18],
    "Sabedoria": [8-18],
    "Carisma": [8-18]
  }},
  "recursos": {{
    "HP Máximo": [calcule],
    "HP Atual": [igual ao máximo],
    "Recursos Especiais": "[liste recursos da classe]"
  }},
  "combate": {{
    "CA": [calcule 10 + DES + armadura],
    "Iniciativa": "[bônus de DES]",
    "Ataques": ["[Arma]: +[bônus] dano [dado]"]
  }},
  "equipamento": {{
    "Armas": ["[liste 2-3 armas]"],
    "Armadura": "[tipo de armadura]",
    "Itens": ["[liste 5-8 itens]"],
    "Dinheiro": "[quantidade] PO"
  }},
  "historia": {{
    "Personalidade": "[3-4 traços]",
    "História": "[2-3 parágrafos completos sobre origem, vida passada e motivações]"
  }}
}}

CRÍTICO: Retorne APENAS o JSON válido, nada antes ou depois."""

            historico_fallback = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": fallback_prompt}
            ]
            
            try:
                conteudo_fallback = await chamar_groq(historico_fallback, max_tokens=2000)
                
                # Parse do fallback
                conteudo_limpo = conteudo_fallback.strip()
                if "```" in conteudo_limpo:
                    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', conteudo_limpo, re.DOTALL)
                    if json_match:
                        conteudo_limpo = json_match.group(1)
                
                inicio = conteudo_limpo.find('{')
                fim = conteudo_limpo.rfind('}') + 1
                if inicio >= 0 and fim > inicio:
                    conteudo_limpo = conteudo_limpo[inicio:fim]
                
                secoes_estruturadas = json.loads(conteudo_limpo)
                print(f"✅ Fallback bem-sucedido: {len(secoes_estruturadas)} seções")
                
            except Exception as e2:
                print(f"⚠️ Fallback também falhou: {e2}")
                
                # ÚLTIMO RECURSO - Ficha hardcoded mas completa
                secoes_estruturadas = {
                    "basico": {
                        "Nome": nome,
                        "Raça": "Humano",
                        "Classe": "Guerreiro",
                        "Nível": 3,
                        "Conceito": "Aventureiro corajoso em busca de glória"
                    },
                    "atributos": {
                        "Força": 16,
                        "Destreza": 14,
                        "Constituição": 14,
                        "Inteligência": 10,
                        "Sabedoria": 12,
                        "Carisma": 10
                    },
                    "recursos": {
                        "HP Máximo": 28,
                        "HP Atual": 28,
                        "Recursos Especiais": "Segunda Rajada (1/descanso curto)"
                    },
                    "combate": {
                        "CA": 16,
                        "Iniciativa": "+2",
                        "Ataques": [
                            "Espada Longa: +5 para acertar, 1d8+3 cortante",
                            "Arco Longo: +4 para acertar, 1d8+2 perfurante"
                        ]
                    },
                    "equipamento": {
                        "Armas": ["Espada Longa", "Arco Longo", "20 Flechas"],
                        "Armadura": "Cota de Malha",
                        "Itens": ["Mochila", "Corda 15m", "Pederneira", "Ração (5 dias)", "Cantil", "Tocha (3x)", "Kit de Primeiros Socorros"],
                        "Dinheiro": "15 PO"
                    },
                    "historia": {
                        "Personalidade": "Corajoso, leal aos companheiros, direto ao ponto, às vezes impulsivo",
                        "História": f"{nome} cresceu em uma pequena vila nas fronteiras do reino, filho de um ferreiro. Desde jovem, sonhava em se tornar um herói e proteger os inocentes. Após sua vila ser atacada por bandidos, jurou nunca mais permitir que o mal prevalecesse. Pegou a espada que seu pai forjou e partiu em busca de aventuras, determinado a fazer a diferença no mundo."
                    }
                }
                
                await ctx.send("⚠️ Usando template padrão. Você pode personalizar com `!editarficha`!")
        
        # Salva ficha
        chave = key_from_name(f"{ctx.author.id}_{nome}")
        fichas_personagens[chave] = {
            "nome": nome,
            "sistema": sistema,
            "autor": ctx.author.id,
            "criada_em": "estruturada_rapida",
            "secoes": secoes_estruturadas,
            "conteudo": conteudo_bruto if parse_success else json.dumps(secoes_estruturadas, ensure_ascii=False, indent=2)
        }
        
        salvar_fichas_agora()
        print(f"✅ Ficha '{nome}' salva para sistema {sistema}")
        
        # Mostra ficha com navegação
        view = FichaNavigationView(fichas_personagens[chave], sistema)
        
        if parse_success:
            mensagem = f"✅ **Ficha Criada: {nome}**\n💡 Use `!criarficha` para modo interativo detalhado."
        else:
            mensagem = f"✅ **Ficha Criada: {nome}**\n⚠️ Alguns campos podem precisar de ajuste. Use `!editarficha {nome}` para personalizar."
        
        await ctx.send(
            content=mensagem,
            embed=view.get_embed(),
            view=view
        )

    @bot.command(name="verficha")
    async def ver_ficha(ctx, *, nome: str = None):
        """Visualiza uma ficha com navegação por páginas."""
        from config import sessoes_ativas
        
        if not nome:
            await ctx.send("❌ Use `!verficha <nome>`.")
            return
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        
        if sessao:
            # Em sessão - permite ver fichas dos participantes
            participantes = [sessao["mestre_id"]] + sessao["jogadores"]
            ficha_encontrada = None
            sistema_encontrado = None
            
            for user_id in participantes:
                chave, ficha = encontrar_ficha(user_id, nome)
                if ficha:
                    ficha_encontrada = ficha
                    sistema_encontrado = ficha.get("sistema", "dnd5e")
                    break
            
            if not ficha_encontrada:
                await ctx.send(f"❌ Ficha '{nome}' não encontrada entre os participantes!")
                return
            
            view = FichaNavigationView(ficha_encontrada, sistema_encontrado)
            await ctx.send(embed=view.get_embed(), view=view)
            
        else:
            # Fora de sessão - apenas próprias fichas
            chave, ficha = encontrar_ficha(ctx.author.id, nome)
            if not ficha:
                await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
                return
            
            sistema = ficha.get("sistema", "dnd5e")
            view = FichaNavigationView(ficha, sistema)
            await ctx.send(embed=view.get_embed(), view=view)

    @bot.command(name="minhasfichas")
    async def minhas_fichas(ctx, sistema_filtro: str = None):
        """Lista suas fichas."""
        user_id = ctx.author.id
        fichas_user = {k: v for k, v in fichas_personagens.items() if v.get("autor") == user_id}
        
        if not fichas_user:
            await ctx.send(f"❌ Você não tem fichas salvas ainda.\n💡 Use `!ficha <nome>` ou `!criarficha` para criar uma!")
            return

        if sistema_filtro:
            from sistemas_rpg import resolver_alias
            sistema_filtro = resolver_alias(sistema_filtro.lower())
            fichas_user = {k: v for k, v in fichas_user.items() if v.get("sistema") == sistema_filtro}

        total = len(fichas_user)
        sistemas_dict = {}
        for f in fichas_user.values():
            sistemas_dict.setdefault(f["sistema"], []).append(f)

        descricao = f"Total: {total} ficha(s)\n\n"
        for s, lista in sistemas_dict.items():
            descricao += f"🎲 {SISTEMAS_DISPONIVEIS[s]['nome']} ({len(lista)})\n"
            for f in lista:
                nome = f['nome']
                tipo = " 📋" if "secoes" in f and f["secoes"] else " 📄"
                descricao += f"• {nome}{tipo}\n"
            descricao += "\n"

        await ctx.send(
            embed=discord.Embed(
                title="📚 Suas Fichas de Personagem",
                description=descricao[:4000],
                color=discord.Color.blurple(),
            ).set_footer(text="📋 = Estruturada (com páginas) | 📄 = Formato antigo | Use !verficha <nome>")
        )

    @bot.command(name="deletarficha")
    async def deletar_ficha(ctx, *, nome: str = None):
        """Deleta uma ficha."""
        if not nome:
            await ctx.send("❌ Use `!deletarficha <nome>`.")
            return
        
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
            return

        del fichas_personagens[chave]
        salvar_fichas_agora()
        
        await ctx.send(f"🗑️ Ficha **{ficha['nome']}** deletada com sucesso.")