# fichas.py — CORREÇÃO: Força salvamento imediato de fichas
import re
import json
import asyncio
import discord
from discord.ext import commands
from utils import (
    chamar_groq, get_system_prompt, key_from_name
)
from config import fichas_personagens, sistemas_rpg, sessoes_ativas
from sistemas_rpg import SISTEMAS_DISPONIVEIS, resolver_alias
import os

# CORREÇÃO: Importa diretamente os caminhos dos arquivos
DATA_DIR = os.path.join(os.getcwd(), "bot_data")
FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")

def salvar_fichas_agora():
    """SALVA FICHAS IMEDIATAMENTE no arquivo JSON."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(FICHAS_PATH, "w", encoding="utf-8") as f:
            json.dump(fichas_personagens, f, ensure_ascii=False, indent=2)
        print(f"💾 FICHAS SALVAS! Total: {len(fichas_personagens)}")
        return True
    except Exception as e:
        print(f"❌ ERRO ao salvar fichas: {e}")
        return False


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

    # ========== CRIAR FICHA INTERATIVA (NOVO) ==========
    @bot.command(name="criarficha")
    async def criar_ficha_interativa(ctx):
        """Cria uma ficha através de perguntas interativas."""
        sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        system_prompt = get_system_prompt(sistema)
        
        await ctx.send(f"📝 **Criação Interativa de Ficha** - Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']}\n\n"
                      f"Vou fazer algumas perguntas para criar sua ficha. Responda cada uma separadamente.\n"
                      f"Digite `cancelar` a qualquer momento para parar.\n\n"
                      f"**1/5** - Qual o **nome** do seu personagem?")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            # Nome
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if msg.content.lower() == 'cancelar':
                return await ctx.send("❌ Criação de ficha cancelada.")
            nome = msg.content
            
            # Raça/Ancestralidade
            await ctx.send(f"**2/5** - Qual a **raça/ancestralidade** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if msg.content.lower() == 'cancelar':
                return await ctx.send("❌ Criação de ficha cancelada.")
            raca = msg.content
            
            # Classe/Arquétipo
            await ctx.send(f"**3/5** - Qual a **classe/profissão** de {nome}?")
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if msg.content.lower() == 'cancelar':
                return await ctx.send("❌ Criação de ficha cancelada.")
            classe = msg.content
            
            # Conceito/Personalidade
            await ctx.send(f"**4/5** - Descreva a **personalidade ou conceito** de {nome} em poucas palavras:")
            msg = await bot.wait_for('message', check=check, timeout=90.0)
            if msg.content.lower() == 'cancelar':
                return await ctx.send("❌ Criação de ficha cancelada.")
            conceito = msg.content
            
            # Background/História
            await ctx.send(f"**5/5** - Qual o **background ou história** de {nome}? (pode ser breve)")
            msg = await bot.wait_for('message', check=check, timeout=120.0)
            if msg.content.lower() == 'cancelar':
                return await ctx.send("❌ Criação de ficha cancelada.")
            historia = msg.content
            
            # Monta prompt para IA
            await ctx.send(f"✨ Gerando ficha completa de **{nome}** com IA...")
            
            prompt = f"""Crie uma ficha de personagem COMPLETA e DETALHADA para o sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']} com as seguintes informações:

Nome: {nome}
Raça/Ancestralidade: {raca}
Classe/Profissão: {classe}
Personalidade/Conceito: {conceito}
Background/História: {historia}

Inclua:
- Todos os atributos/características do sistema
- Habilidades, talentos ou perícias apropriadas
- Equipamento inicial adequado ao background
- Estatísticas de combate (PV, CA, etc)
- Magias ou habilidades especiais (se aplicável)
- Detalhes narrativos que enriqueçam o personagem

Seja completo e balanceado para o sistema escolhido."""

            historico = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            conteudo = await chamar_groq(historico, max_tokens=1500)
            
            if not conteudo or "Erro" in conteudo:
                await ctx.send(f"⚠️ Ocorreu um erro ao gerar a ficha: {conteudo}")
                return
            
            # CORREÇÃO: Salva ficha COM GARANTIA de persistência
            chave = key_from_name(f"{ctx.author.id}_{nome}")
            fichas_personagens[chave] = {
                "nome": nome,
                "sistema": sistema,
                "conteudo": conteudo,
                "autor": ctx.author.id,
                "criada_em": "interativa"
            }
            
            # FORÇA SALVAMENTO IMEDIATO
            if salvar_fichas_agora():
                print(f"✅ Ficha '{nome}' salva para user {ctx.author.id}")
            else:
                await ctx.send("⚠️ Aviso: A ficha foi criada mas pode não ter sido salva corretamente.")
            
            # Mostra resultado
            embed = discord.Embed(
                title=f"✅ Ficha Criada: {nome}",
                description=conteudo[:4000],
                color=discord.Color.green(),
            )
            embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']} | Use !verficha {nome}")
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado! Use `!criarficha` novamente para tentar de novo.")

    # ========== FICHA AUTOMÁTICA ==========
    @bot.command(name="ficha")
    async def ficha_cmd(ctx, *, nome: str = None):
        if not nome:
            await ctx.send("❌ Use `!ficha <nome>` para criar uma ficha automática ou `!criarficha` para modo interativo.")
            return

        sistema = sistemas_rpg.get(ctx.channel.id, "dnd5e")
        system_prompt = get_system_prompt(sistema)

        historico = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Crie uma ficha de personagem completa para o sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']} chamada {nome}."}
        ]

        await ctx.send(f"📝 Criando ficha de **{nome}** em {SISTEMAS_DISPONIVEIS[sistema]['nome']}...")

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
        
        # FORÇA SALVAMENTO IMEDIATO
        if salvar_fichas_agora():
            print(f"✅ Ficha '{nome}' salva para user {ctx.author.id}")
        else:
            await ctx.send("⚠️ Aviso: A ficha foi criada mas pode não ter sido salva corretamente.")

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
            await ctx.send(f"❌ Você não tem fichas salvas ainda.\n💡 Use `!ficha <nome>` ou `!criarficha` para criar uma!")
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
														   
					 
																  
				  
        
        # CORREÇÃO: Verifica se está em uma sessão ativa
        sessao = sessoes_ativas.get(ctx.channel.id)
        
        if sessao:
            # Está em sessão - permite ver fichas de qualquer participante
            participantes = [sessao["mestre_id"]] + sessao["jogadores"]
            ficha_encontrada = None
            
            # Primeiro tenta encontrar entre os participantes da sessão
            for user_id in participantes:
                chave, ficha = encontrar_ficha(user_id, nome)
                if ficha:
                    ficha_encontrada = ficha
                    break
            
            if not ficha_encontrada:
                await ctx.send(f"❌ Ficha '{nome}' não encontrada entre os participantes da sessão!")
                return

            embed = discord.Embed(
                title=f"📜 {ficha_encontrada['nome']} ({SISTEMAS_DISPONIVEIS[ficha_encontrada['sistema']]['nome']})",
                description=ficha_encontrada["conteudo"][:4000],
                color=discord.Color.gold(),
            )
            await ctx.send(embed=embed)
            
        else:
            # Fora de sessão - comportamento normal (apenas próprias fichas)
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
            prompt = f"""Edite a seguinte ficha de personagem conforme a instrução do jogador.
Mantenha toda a estrutura e informações não mencionadas. Apenas altere o que foi solicitado.

FICHA ATUAL:
{ficha['conteudo']}

INSTRUÇÃO DE EDIÇÃO:
{instrucao}

Retorne a ficha completa atualizada, mantendo o formato original."""

            historico = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            conteudo_novo = await chamar_groq(historico, max_tokens=1500)
            
            if not conteudo_novo or "Erro" in conteudo_novo:
                await ctx.send(f"⚠️ Erro ao editar ficha: {conteudo_novo}")
                return
            
            # Atualiza ficha
            fichas_personagens[chave]["conteudo"] = conteudo_novo
            
            # FORÇA SALVAMENTO IMEDIATO
            if salvar_fichas_agora():
                print(f"✅ Ficha '{ficha['nome']}' atualizada para user {ctx.author.id}")
            else:
                await ctx.send("⚠️ Aviso: A edição foi feita mas pode não ter sido salva corretamente.")
            
            embed = discord.Embed(
                title=f"✅ Ficha Atualizada: {ficha['nome']}",
                description=conteudo_novo[:4000],
                color=discord.Color.blue(),
            )
            embed.set_footer(text="Use !verficha para ver a ficha completa")
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado! Use `!editarficha <nome>` novamente.")

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
        
        # FORÇA SALVAMENTO IMEDIATO
        if salvar_fichas_agora():
            print(f"✅ Ficha '{ficha['nome']}' deletada para user {ctx.author.id}")
        else:
            await ctx.send("⚠️ Aviso: A ficha foi deletada mas a mudança pode não ter sido salva corretamente.")
        
        await ctx.send(f"🗑️ Ficha **{ficha['nome']}** deletada com sucesso.")

    @bot.command(name="converterficha")
    async def converter_ficha(ctx, novo_sistema: str, *, nome_personagem: str = None):
        if not nome_personagem:
            await ctx.send("❌ Use: `!converterficha <sistema> <nome>`")
            return

        novo_sistema_original = novo_sistema
        novo_sistema = resolver_alias(novo_sistema.lower())
        
        # CORREÇÃO: Debug para identificar problemas
        if novo_sistema not in SISTEMAS_DISPONIVEIS:
            sistemas_cyberpunk = [s for s in SISTEMAS_DISPONIVEIS.keys() if "cyber" in s or "red" in s]
            sistemas_disponiveis = ", ".join([f"`{s}`" for s in sistemas_cyberpunk])
            await ctx.send(f"❌ Sistema `{novo_sistema_original}` (resolvido para `{novo_sistema}`) inválido.\n💡 Sistemas cyberpunk disponíveis: {sistemas_disponiveis}")
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

        historico = [
            {"role": "system", "content": get_system_prompt(novo_sistema)},
            {"role": "user", "content": prompt},
        ]

        convertido = await chamar_groq(historico, max_tokens=1200)
        
        if not convertido or "Erro" in convertido:
            await ctx.send(f"⚠️ Erro ao converter ficha via IA: {convertido}")
            return

        nome_sistema = SISTEMAS_DISPONIVEIS[novo_sistema]['nome'].strip()
        novo_nome = f"{ficha['nome']} ({nome_sistema})"
        nova_chave = key_from_name(f"{ctx.author.id}_{novo_nome}")

        fichas_personagens[nova_chave] = {
            "nome": novo_nome,
            "sistema": novo_sistema,
            "conteudo": convertido,
            "autor": ctx.author.id,
            "convertida_de": atual,
        }

        # FORÇA SALVAMENTO IMEDIATO
        if salvar_fichas_agora():
            print(f"✅ Ficha convertida '{novo_nome}' salva para user {ctx.author.id}")
        else:
            await ctx.send("⚠️ Aviso: A conversão foi feita mas pode não ter sido salva corretamente.")

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