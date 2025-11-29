# commands/fichas_edicao.py (CORRIGIDO - Parte 1)
"""Comandos de criação interativa e edição de fichas."""

import discord
from discord.ext import commands
import asyncio
import json

from config import fichas_personagens, sistemas_rpg
from sistemas_rpg import SISTEMAS_DISPONIVEIS
from utils import chamar_groq, get_system_prompt, key_from_name
from core.ficha_helpers import salvar_fichas_agora, encontrar_ficha, get_estrutura_ficha
from views.ficha_views import FichaNavigationView


def register_fichas_edicao_commands(bot: commands.Bot):
    """Registra comandos de criação interativa e edição."""

    @bot.command(name="criarficha")
    async def criar_ficha_estruturada(ctx):
        """Cria uma ficha estruturada através de perguntas interativas."""
        sistema = sistemas_rpg.get(ctx.author.id, "dnd5e")
        system_prompt = get_system_prompt(sistema)
        estrutura = get_estrutura_ficha(sistema)
        
        # Deleta comando do usuário
        try:
            await ctx.message.delete()
        except:
            pass
        
        # Envia tudo por DM
        try:
            # Mensagem inicial com preview das perguntas
            await ctx.author.send(
                f"📝 **Criação de Ficha Estruturada**\n"
                f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}\n\n"
                f"**Farei estas 8 perguntas para você:**\n"
                f"1️⃣ Nome do personagem\n"
                f"2️⃣ Raça/Ancestralidade\n"
                f"3️⃣ Classe/Profissão\n"
                f"4️⃣ Nível ou Idade\n"
                f"5️⃣ Personalidade (3-5 traços)\n"
                f"6️⃣ Aparência física\n"
                f"7️⃣ Background/Origem\n"
                f"8️⃣ Objetivos/Motivações\n\n"
                f"💡 **Dica importante:** Para evitar timeout durante a criação, "
                f"prepare suas respostas mais longas (história, aparência, objetivos) "
                f"em outro lugar e cole quando chegar a pergunta!\n\n"
                f"Digite `cancelar` a qualquer momento para parar.\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"**1/8** - Qual o **nome** do seu personagem?"
            )
            
            is_dm = isinstance(ctx.channel, discord.DMChannel)

            if not is_dm:
                await ctx.send(
                    f"✅ {ctx.author.mention}, processo de criação iniciado no privado! "
                    f"Confira sua DM.",
                    delete_after=10
                )
        
        except discord.Forbidden:
            await ctx.send(
                f"❌ {ctx.author.mention}, não consigo te enviar DM! "
                f"Habilite mensagens diretas nas configurações.",
                delete_after=15
            )
            return
        
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
        
        try:
            # Nome
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            nome = msg.content
            
            # Raça/Ancestralidade
            await ctx.author.send(f"**2/8** - Qual a **raça/ancestralidade** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            raca = msg.content
            
            # Classe/Arquétipo
            await ctx.author.send(f"**3/8** - Qual a **classe/profissão** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            classe = msg.content
            
            # Nível/Idade
            await ctx.author.send(f"**4/8** - Qual o **nível ou idade** de {nome}? (Ex: Nível 5, ou 28 anos)")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            nivel = msg.content
            
            # Conceito/Personalidade
            await ctx.author.send(f"**5/8** - Descreva a **personalidade** de {nome} (3-5 traços):")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            conceito = msg.content
            
            # Aparência
            await ctx.author.send(f"**6/8** - Descreva a **aparência física** de {nome}:")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            aparencia = msg.content
            
            # Background/História
            await ctx.author.send(f"**7/8** - Qual o **background ou origem** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            historia = msg.content
            
            # Objetivos/Motivações
            await ctx.author.send(f"**8/8** - Quais os **objetivos ou motivações** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=None)
            if msg.content.lower() == 'cancelar':
                return await ctx.author.send("❌ Criação de ficha cancelada.")
            objetivos = msg.content
            
            # Gera ficha estruturada com IA
            await ctx.author.send(f"✨ Gerando ficha estruturada de **{nome}** com IA...")
            
            # Monta prompt específico para formato estruturado
            prompt = f"""Crie uma ficha de personagem COMPLETA, DETALHADA e BALANCEADA para {SISTEMAS_DISPONIVEIS[sistema]['nome']}.

**INFORMAÇÕES FORNECIDAS PELO JOGADOR:**
- Nome: {nome}
- Raça/Ancestralidade: {raca}
- Classe/Profissão: {classe}
- Nível/Idade: {nivel}
- Personalidade: {conceito}
- Aparência Física: {aparencia}
- Background/Origem: {historia}
- Objetivos/Motivações: {objetivos}

**INSTRUÇÕES OBRIGATÓRIAS:**
1. EXPANDA todas as informações - transforme respostas curtas em descrições ricas
2. CALCULE todos os valores numéricos apropriados ao nível
3. PREENCHA 100% dos campos - NENHUM campo pode ficar vazio, com "—" ou "A definir"
4. CRIE equipamento inicial completo e apropriado
5. ADICIONE habilidades de classe do nível apropriado
6. DESENVOLVA história em 3-4 parágrafos envolventes
7. SEMPRE inclua seções "equipamento" com "Inventário": [] e "Equipado": {{"Arma": "—", "Armadura": "—"}}

**FORMATO JSON OBRIGATÓRIO - PREENCHA TODOS OS CAMPOS:**

{{
  "basico": {{
    "Nome": "{nome}",
    "Raça": "[EXPANDIR {raca} com detalhes de sub-raça]",
    "Classe": "[EXPANDIR {classe} com arquétipo/caminho]",
    "Nível": "[EXTRAIR número de: {nivel}]",
    "Antecedente": "[CRIAR baseado em: {historia}]",
    "Alinhamento": "[DEFINIR baseado na personalidade]"
  }},
  "atributos": {{
    "Força": [VALOR 8-18],
    "Destreza": [VALOR 8-18],
    "Constituição": [VALOR 8-18],
    "Inteligência": [VALOR 8-18],
    "Sabedoria": [VALOR 8-18],
    "Carisma": [VALOR 8-18]
  }},
  "recursos": {{
    "HP Máximo": [CALCULAR: dado_classe × nível + CON×nível],
    "HP Atual": [IGUAL ao HP Máximo],
    "Dados de Vida": "[Ex: 5d8 para Paladino nível 5]",
    "Proficiência": "[+2 até nível 4, +3 para nível 5-8, +4 para 9-12, +5 para 13-16, +6 para 17-20]"
  }},
  "combate": {{
    "CA": [CALCULAR: 10 + mod_DES + armadura],
    "Iniciativa": "[modificador de Destreza com sinal: +2, -1, etc]",
    "Velocidade": "9m",
    "Ataques": ["[ARMA 1]: +[bônus] para acertar, [dano]+[mod]", "[ARMA 2]: +[bônus] para acertar, [dano]+[mod]"]
  }},
  "equipamento": {{
    "Armas": ["[LISTAR 2-3 armas apropriadas]"],
    "Armadura": "[TIPO de armadura apropriada]",
    "Itens": ["[LISTAR 6-10 itens: poções, ferramentas, itens mundanos]"],
    "Inventário": [],
    "Equipado": {{"Arma": "[nome da arma principal]", "Armadura": "[tipo de armadura]"}},
    "Dinheiro": "[QUANTIDADE apropriada] PO"
  }},
  "magia": {{
    "Nível de Conjurador": "[NÚMERO ou 'Não possui']",
    "CD de Magia": "[CALCULAR: 8 + proficiência + modificador_atributo ou 'N/A']",
    "Bônus de Ataque": "[proficiência + modificador ou 'N/A']",
    "Espaços de Magia": "[Ex: 4/3/2 ou por nível conforme classe ou 'N/A']",
    "Magias Conhecidas": ["[LISTAR 8-12 magias apropriadas ao nível e classe, ou 'Não possui magias']"]
  }},
  "historia": {{
    "Personalidade": "[EXPANDIR {conceito} em 2-3 frases detalhadas]",
    "Ideais": "[CRIAR 1-2 ideais baseados na personalidade e background]",
    "Vínculos": "[CRIAR 1-2 vínculos baseados em {historia} e {objetivos}]",
    "Defeitos": "[CRIAR 1-2 defeitos interessantes e balanceados]",
    "História": "[ESCREVER 3-4 parágrafos completos integrando: {aparencia}, {historia}, {objetivos} de forma coesa e envolvente]"
  }}
}}

**RETORNE APENAS O JSON PURO - SEM TEXTO ANTES OU DEPOIS, SEM MARKDOWN, SEM EXPLICAÇÕES.**"""

            historico = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            conteudo_bruto = await chamar_groq(historico, max_tokens=2500)
            
            # Tenta parsear JSON estruturado
            secoes_estruturadas = None
            try:
                conteudo_limpo = conteudo_bruto.strip()
                
                # Remove markdown
                if "```" in conteudo_limpo:
                    import re
                    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', conteudo_limpo, re.DOTALL)
                    if json_match:
                        conteudo_limpo = json_match.group(1)
                
                # Extrai JSON
                inicio = conteudo_limpo.find('{')
                fim = conteudo_limpo.rfind('}') + 1
                if inicio >= 0 and fim > inicio:
                    conteudo_limpo = conteudo_limpo[inicio:fim]
                
                # Parseia
                secoes_estruturadas = json.loads(conteudo_limpo)
                
                # Valida
                if not isinstance(secoes_estruturadas, dict) or not secoes_estruturadas:
                    raise ValueError("JSON inválido")
                
                print(f"✅ JSON OK! {len(secoes_estruturadas)} seções")
                
            except Exception as e:
                print(f"⚠️ Erro JSON: {e}")
                # Fallback básico
                secoes_estruturadas = {
                    "basico": {"Nome": nome, "Raça": raca, "Classe": classe, "Nível": nivel},
                    "atributos": {"Força": 10, "Destreza": 10, "Constituição": 10, "Inteligência": 10, "Sabedoria": 10, "Carisma": 10},
                    "recursos": {},
                    "combate": {},
                    "equipamento": {
                        "Inventário": [],
                        "Equipado": {"Arma": "—", "Armadura": "—"}
                    },
                    "magia": {},
                    "historia": {"Personalidade": conceito, "Aparência": aparencia, "História": historia, "Objetivos": objetivos}
                }
                await ctx.author.send("⚠️ IA teve dificuldades. Criada ficha básica. Use `!editarficha` para completar!")
            
            if "equipamento" in secoes_estruturadas:
                if "Inventário" not in secoes_estruturadas["equipamento"]:
                    secoes_estruturadas["equipamento"]["Inventário"] = []
                
                if "Equipado" not in secoes_estruturadas["equipamento"]:
                    secoes_estruturadas["equipamento"]["Equipado"] = {
                        "Arma": "—",
                        "Armadura": "—"
                    }
            
            # Salva ficha
            chave = key_from_name(f"{ctx.author.id}_{nome}")
            fichas_personagens[chave] = {
                "nome": nome,
                "sistema": sistema,
                "autor": ctx.author.id,
                "criada_em": "estruturada",
                "secoes": secoes_estruturadas,
                "conteudo": conteudo_bruto
            }
            
            if salvar_fichas_agora():
                print(f"✅ Ficha estruturada '{nome}' salva para user {ctx.author.id}")
            
            # Mostra ficha com navegação
            if secoes_estruturadas and any(secoes_estruturadas.values()):
                view = FichaNavigationView(fichas_personagens[chave], sistema)
                await ctx.author.send(
                    content="✅ **Ficha Criada com Sucesso!**",
                    embed=view.get_embed(),
                    view=view
                )
            else:
                await ctx.author.send(
                    embed=discord.Embed(
                        title=f"⚠️ Ficha Criada (Formato Simplificado)",
                        description=(
                            f"**{nome}** foi criado, mas em formato simplificado.\n\n"
                            f"**Dados Básicos:**\n"
                            f"• Raça: {raca}\n"
                            f"• Classe: {classe}\n"
                            f"• Conceito: {conceito}\n\n"
                            f"**História:** {historia[:200]}...\n\n"
                            f"💡 **Dica:** Use `!editarficha {nome}` para adicionar atributos e equipamento."
                        ),
                        color=discord.Color.orange()
                    ).set_footer(text="Sistema: " + SISTEMAS_DISPONIVEIS[sistema]['nome'])
                )
            
        except asyncio.TimeoutError:
            await ctx.author.send(
                "⏰ Tempo esgotado!\n\n"
                "💡 **Dica:** Prepare suas respostas longas (história, aparência) "
                "em um editor de texto antes e cole quando chegar a pergunta.\n\n"
                "Use `!criarficha` novamente quando estiver pronto!"
            )

    @bot.command(name="editarficha")
    async def editar_ficha(ctx, *, nome: str = None):
        """Edita uma ficha existente de forma interativa."""
        if not nome:
            await ctx.send("❌ Use `!editarficha <nome>`.")
            return
        
        chave, ficha = encontrar_ficha(ctx.author.id, nome)
        if not ficha:
            await ctx.send(f"❌ Ficha '{nome}' não encontrada!")
            return
        
        sistema = ficha.get("sistema", "dnd5e")
        
        await ctx.send(
            f"✏️ **Editando ficha: {ficha['nome']}**\n\n"
            f"O que você deseja fazer?\n"
            f"1️⃣ - Editar atributos/estatísticas\n"
            f"2️⃣ - Adicionar equipamento/item\n"
            f"3️⃣ - Modificar história/background\n"
            f"4️⃣ - Edição livre (descreva o que quer mudar)\n"
            f"❌ - Digite `cancelar` para sair\n\n"
            f"Digite o número da opção:"
        )
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            # Escolha da opção
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if msg.content.lower() == 'cancelar':
                return await ctx.send("❌ Edição cancelada.")
            
            opcao = msg.content.strip()
            
            if opcao == "1":
                await ctx.send("📊 Descreva as mudanças nos atributos/estatísticas (ex: 'aumentar Força para 18, adicionar +2 em Constituição'):")
                msg = await bot.wait_for('message', check=check, timeout=120.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = f"Atualize os atributos e estatísticas conforme solicitado: {msg.content}"
                
            elif opcao == "2":
                await ctx.send("⚔️ Descreva o equipamento/item a adicionar:")
                msg = await bot.wait_for('message', check=check, timeout=120.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = f"Adicione o seguinte equipamento ao inventário do personagem: {msg.content}"
                
            elif opcao == "3":
                await ctx.send("📖 Descreva as mudanças na história/background:")
                msg = await bot.wait_for('message', check=check, timeout=180.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = f"Atualize a história e background do personagem: {msg.content}"
                
            elif opcao == "4":
                await ctx.send("✍️ Descreva livremente o que deseja mudar na ficha:")
                msg = await bot.wait_for('message', check=check, timeout=180.0)
                if msg.content.lower() == 'cancelar':
                    return await ctx.send("❌ Edição cancelada.")
                instrucao = msg.content
                
            else:
                return await ctx.send("❌ Opção inválida! Use `!editarficha <nome>` novamente.")
            
            # Processa edição com IA
            await ctx.send(f"✨ Processando alterações em **{ficha['nome']}**...")
            
            system_prompt = get_system_prompt(sistema)
            
            # Extrai conteúdo atual (estruturado ou texto)
            if "secoes" in ficha and ficha["secoes"]:
                conteudo_atual = json.dumps(ficha["secoes"], indent=2, ensure_ascii=False)
                formato = "JSON estruturado"
            else:
                conteudo_atual = ficha.get("conteudo", "")
                formato = "texto"
            
            prompt = f"""Você receberá uma ficha de personagem completa e uma instrução de edição.

**SISTEMA:** {SISTEMAS_DISPONIVEIS[sistema]['nome']}

**INSTRUÇÃO DO JOGADOR:**
{instrucao}

**FICHA ATUAL COMPLETA (formato {formato}):**
{conteudo_atual}

**INSTRUÇÕES CRÍTICAS:**
1. Leia toda a ficha acima
2. Aplique APENAS as mudanças mencionadas na instrução
3. RETORNE A FICHA COMPLETA com as alterações aplicadas
4. MANTENHA todos os outros campos EXATAMENTE como estão
5. Se a instrução pedir para ADICIONAR itens, adicione à lista existente (não substitua)
6. Se a instrução pedir para ALTERAR valores, altere apenas esses valores
7. Valores calculados (HP, CA, bônus) devem ser recalculados se atributos mudarem
8. Se a instrução criar NOVOS campos/seções que não existiam, ADICIONE-os ao JSON (ex: "adicione uma nova seção X" ou "crie um campo Y")
9. SEMPRE inclua "Inventário": [] e "Equipado": {{"Arma": "...", "Armadura": "..."}} na seção "equipamento"

**FORMATO DE RETORNO:**
Retorne o JSON COMPLETO da ficha com as modificações aplicadas.
NÃO retorne apenas os campos alterados.
NÃO adicione texto explicativo antes ou depois.
NÃO use markdown (```json).

**EXEMPLO 1:**
Se a instrução for "aumentar Força para 18", você deve:
- Alterar o campo "Força" de [valor atual] para 18
- Recalcular bônus de ataque corpo a corpo se necessário
- Recalcular dano de armas corpo a corpo
- MANTER todos os outros campos inalterados
- RETORNAR a ficha completa com essas alterações

**EXEMPLO 2:**
Se a instrução for "adicionar nova seção 'segredos' com campo 'segredo_pessoal'", você deve:
- ADICIONAR nova seção "segredos": {{"segredo_pessoal": "[conteúdo apropriado]"}}
- MANTER todos os outros campos inalterados
- RETORNAR a ficha completa incluindo a nova seção

Agora, retorne a ficha COMPLETA com as alterações aplicadas:"""

            historico = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            conteudo_novo = await chamar_groq(historico, max_tokens=2500)
            
            if not conteudo_novo or "Erro" in conteudo_novo:
                await ctx.send(f"⚠️ Erro ao editar ficha: {conteudo_novo}")
                return
            
            # Parser
            if "secoes" in ficha and ficha["secoes"]:
                try:
                    import re
                    conteudo_limpo = conteudo_novo.strip()
                    
                    # Remove markdown
                    if "```" in conteudo_limpo:
                        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', conteudo_limpo, re.DOTALL)
                        if json_match:
                            conteudo_limpo = json_match.group(1)
                    
                    # Remove texto antes/depois do JSON
                    inicio = conteudo_limpo.find('{')
                    fim = conteudo_limpo.rfind('}') + 1
                    if inicio >= 0 and fim > inicio:
                        conteudo_limpo = conteudo_limpo[inicio:fim]
                    
                    # Parseia
                    nova_secao = json.loads(conteudo_limpo)
                    
                    # VALIDAÇÃO: Verifica se tem pelo menos as mesmas seções
                    secoes_antigas = set(ficha["secoes"].keys())
                    secoes_novas = set(nova_secao.keys())
                    
                    secoes_removidas = secoes_antigas - secoes_novas
                    if len(secoes_removidas) > len(secoes_antigas) * 0.3:  # Perdeu mais de 30% das seções
                        raise ValueError(f"Edição incompleta: {len(secoes_removidas)} seções removidas")
                    
                    # VALIDAÇÃO: Conta campos não-vazios
                    campos_preenchidos = 0
                    campos_totais = 0
                    
                    for secao_nome, conteudo_secao in nova_secao.items():
                        if isinstance(conteudo_secao, dict):
                            for campo, valor in conteudo_secao.items():
                                campos_totais += 1
                                if valor and valor not in ["—", "A definir", "", None]:
                                    campos_preenchidos += 1
                    
                    if campos_totais > 0 and campos_preenchidos / campos_totais < 0.5:
                        raise ValueError(f"Muitos campos vazios: {campos_preenchidos}/{campos_totais} preenchidos")
                    
                    # Detecta mudanças
                    campos_editados = []
                    campos_novos = []
                    
                    for secao_nome, conteudo_secao in nova_secao.items():
                        # Seção nova?
                        if secao_nome not in ficha["secoes"]:
                            campos_novos.append(f"Nova seção: {secao_nome}")
                            continue
                        
                        if isinstance(conteudo_secao, dict):
                            for campo, valor in conteudo_secao.items():
                                # Campo novo?
                                if campo not in ficha["secoes"].get(secao_nome, {}):
                                    campos_novos.append(f"{secao_nome}.{campo}")
                                    continue
                                
                                # Campo editado?
                                valor_antigo = ficha["secoes"][secao_nome].get(campo)
                                if str(valor) != str(valor_antigo):
                                    campos_editados.append(f"{secao_nome}.{campo}: {valor_antigo} → {valor}")
                    
                    if not campos_editados and not campos_novos:
                        await ctx.send("⚠️ Nenhuma mudança foi detectada. A IA pode não ter entendido a instrução. Tente ser mais específico.")
                        return
                    
                    # ✅ Aplica mudanças (incluindo novas seções/campos)
                    fichas_personagens[chave]["secoes"] = nova_secao
                    
                    print(f"✅ {len(campos_editados)} campos editados, {len(campos_novos)} novos:")
                    for mudanca in (campos_editados + campos_novos)[:10]:
                        print(f"  - {mudanca}")
                    
                except json.JSONDecodeError as je:
                    print(f"⚠️ Erro JSON: {je}")
                    await ctx.send(
                        f"⚠️ A IA retornou dados inválidos.\n"
                        f"**Tente novamente com uma instrução mais simples.**\n"
                        f"Exemplo: `Aumentar Força para 18`"
                    )
                    return
                    
                except ValueError as ve:
                    print(f"⚠️ Validação falhou: {ve}")
                    await ctx.send(
                        f"⚠️ A edição ficou incompleta.\n"
                        f"**Detalhes:** {ve}\n\n"
                        f"💡 Tente uma instrução mais específica:\n"
                        f"• `Aumentar Força para 18 e Destreza para 16`\n"
                        f"• `Adicionar Espada Longa +1 ao equipamento`\n"
                        f"• `Mudar história para: [nova história]`"
                    )
                    return
            else:
                fichas_personagens[chave]["conteudo"] = conteudo_novo
            
            if salvar_fichas_agora():
                print(f"✅ Ficha '{ficha['nome']}' atualizada para user {ctx.author.id}")
            else:
                await ctx.send("⚠️ Aviso: A edição foi feita mas pode não ter sido salva corretamente.")
            
            # Mostra resultado
            if "secoes" in fichas_personagens[chave] and fichas_personagens[chave]["secoes"]:
                view = FichaNavigationView(fichas_personagens[chave], sistema)
                
                # Feedback detalhado
                resumo_mudancas = "\n".join([f"• {m}" for m in (campos_editados + campos_novos)[:10]])
                if len(campos_editados) + len(campos_novos) > 10:
                    resumo_mudancas += f"\n• ... e mais {len(campos_editados) + len(campos_novos) - 10} mudanças"
                
                await ctx.send(
                    content=f"✅ **Ficha Atualizada com Sucesso!**\n\n**Mudanças aplicadas:**\n{resumo_mudancas}",
                    embed=view.get_embed(),
                    view=view
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title=f"✅ Ficha Atualizada: {ficha['nome']}",
                        description=conteudo_novo[:4000],
                        color=discord.Color.blue(),
                    ).set_footer(text="Use !verficha para ver a ficha completa")
                )
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado! Use `!editarficha <nome>` novamente.")