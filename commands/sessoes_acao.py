# commands/sessoes_acao.py
"""Comandos !acao e !cenanarrada com sistema de rolagens interativo."""

import discord
from discord.ext import commands
import re

from views.sessao_views import RollRequestView, ContinueStoryView


def register_acao_commands(
    bot: commands.Bot,
    sessoes_ativas,
    fichas_personagens,
    chamar_groq,
    get_system_prompt,
    salvar_dados
):
    """Registra comandos de ação e narrativa."""

    @bot.command(name="acao")
    @commands.guild_only()
    async def acao(ctx: commands.Context, *, descricao: str = None):
        """Jogadores descrevem suas ações durante a sessão."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use **no canal da sessão**.")
        
        if not descricao:
            return await ctx.send("❌ Use: `!acao <descrição do que seu personagem faz>`")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        if ctx.author.id != sessao["mestre_id"] and ctx.author.id not in sessao["jogadores"]:
            return await ctx.send("⚠️ Você não faz parte desta sessão.")
        
        if sessao.get("status") != "em_andamento":
            return await ctx.send("⚠️ A aventura ainda não começou!")
        
        # Pega nome do personagem
        fichas_sel = sessao.get("fichas", {})
        chave_ficha = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
        nome_personagem = chave_ficha.split('_', 1)[-1].replace('_', ' ').title() if chave_ficha else ctx.author.display_name
        
        # SISTEMA DE TURNOS - Verifica se há iniciativa ativa
        iniciativa_ativa = sessao.get("iniciativa_ativa", False)
        if iniciativa_ativa:
            # Inicializa controle de turnos se não existir
            if "turnos_agidos" not in sessao:
                sessao["turnos_agidos"] = []
            
            # Verifica se já agiu neste turno
            if ctx.author.id in sessao["turnos_agidos"]:
                return await ctx.send("⚠️ Você já agiu neste turno! Aguarde os outros jogadores.")
            
            # Marca que este jogador agiu
            sessao["turnos_agidos"].append(ctx.author.id)
            salvar_dados()
        
        # Adiciona ao histórico
        historia = sessao.get("historia", [])
        historia.append({"role": "user", "content": f"Ação de {nome_personagem}: {descricao}"})
        
        # Envia mensagem visual
        await ctx.send(embed=discord.Embed(
            title=f"🎭 {nome_personagem} age!",
            description=descricao,
            color=discord.Color.blue()
        ).set_footer(text=f"Jogador: {ctx.author.display_name}"))
        
        # VERIFICA SE TODOS JÁ AGIRAM NESTE TURNO
        if iniciativa_ativa:
            jogadores_total = len(sessao.get("jogadores", []))
            jogadores_agidos = len(sessao["turnos_agidos"])
            
            if jogadores_agidos < jogadores_total:
                # Ainda faltam jogadores
                faltam = jogadores_total - jogadores_agidos
                ordem_iniciativa = sessao.get("ordem_iniciativa", [])
                
                # Descobre quem ainda não agiu
                proximos = []
                for nome, _ in ordem_iniciativa:
                    # Verifica se este nome corresponde a algum jogador que não agiu
                    for jid in sessao.get("jogadores", []):
                        if jid not in sessao["turnos_agidos"]:
                            chave = fichas_sel.get(str(jid)) or fichas_sel.get(jid)
                            if chave:
                                nome_ficha = chave.split('_', 1)[-1].replace('_', ' ').title()
                                if nome_ficha == nome:
                                    membro = ctx.guild.get_member(jid)
                                    if membro:
                                        proximos.append(membro.mention)
                                        break
                
                await ctx.send(
                    embed=discord.Embed(
                        title="⏳ Aguardando Outros Jogadores",
                        description=f"Faltam **{faltam}** jogador{'es' if faltam > 1 else ''} agir neste turno.\n\n"
                                  f"**Próximos:** {', '.join(proximos[:3]) if proximos else 'Verifique a ordem de iniciativa'}",
                        color=discord.Color.orange()
                    )
                )
                return  # NÃO gera resposta da IA ainda
            else:
                # TODOS AGIRAM - Reseta turnos para próximo round
                sessao["turnos_agidos"] = []
                salvar_dados()
                
                await ctx.send(
                    embed=discord.Embed(
                        title="✅ Turno Completo!",
                        description="Todos os jogadores agiram. A IA narrará as consequências e iniciará o próximo turno.",
                        color=discord.Color.green()
                    )
                )
        
        await ctx.send("✨ *A história se desenrola...*")
        
        # Gera resposta da IA
        sistema = sessao.get("sistema", "dnd5e")
        estilo = sessao.get("estilo_narrativo", "extenso")
        
        if estilo == "extenso":
            max_tokens = 1200
            instrucao = "Narre as consequências em 2-4 parágrafos detalhados."
        else:
            max_tokens = 600
            instrucao = "Narre em 1 parágrafo breve (máx 4 frases). SEJA DIRETO."
        
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema) + "\n\n**IMPORTANTE:** Quando apropriado, solicite rolagens de dados aos jogadores. Use o formato EXATO:\n[ROLL: 1d20+modificador, jogadores]\n\nEXEMPLOS CORRETOS:\n- [ROLL: 1d20+3, todos]\n- [ROLL: 2d6, Elara]\n- [ROLL: 1d20, todos]\n\nNUNCA use nomes de perícias ou atributos, APENAS dados (1d20, 2d6, etc)."},
        ] + historia_recente + [
            {"role": "user", "content": f"{instrucao} Se requer teste/combate, SOLICITE rolagem com [ROLL: dado, jogadores]."}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=max_tokens)
        
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        salvar_dados()
        
        # Detecta solicitação de rolagem
        roll_match = re.search(r'\[ROLL:\s*([^,\]]+),\s*([^\]]+)\]', resposta, re.IGNORECASE)
        
        if roll_match:
            roll_type = roll_match.group(1).strip()
            players_str = roll_match.group(2).strip()
            resposta_limpa = re.sub(r'\[ROLL:[^\]]+\]', '', resposta).strip()
            
            # Determina quem deve rolar
            if players_str.lower() in ['todos', 'all', 'grupo', 'party']:
                players_needed = sessao.get("jogadores", [])
            else:
                players_needed = []
                for jid in sessao.get("jogadores", []):
                    chave = fichas_sel.get(str(jid)) or fichas_sel.get(jid)
                    if chave:
                        nome = chave.split('_', 1)[-1].replace('_', ' ').lower()
                        if nome in players_str.lower():
                            players_needed.append(jid)
                if not players_needed:
                    players_needed = sessao.get("jogadores", [])
            
            # Envia narrativa
            await ctx.send(embed=discord.Embed(
                title="📖 A História Continua...",
                description=resposta_limpa[:4000],
                color=discord.Color.gold()
            ).set_footer(text=f"Estilo: {estilo.upper()}"))
            
            # Solicita rolagens
            jogadores_nomes = [ctx.guild.get_member(uid).mention for uid in players_needed if ctx.guild.get_member(uid)]
            
            roll_embed = discord.Embed(
                title="🎲 Rolagem Necessária!",
                description=f"**Tipo:** `{roll_type}`\n**Jogadores:** {', '.join(jogadores_nomes)}\n\nClique no botão abaixo!",
                color=discord.Color.blue()
            )
            
            view = RollRequestView(bot, sessoes_ativas, salvar_dados, ctx.channel.id, roll_type, players_needed)
            await ctx.send(embed=roll_embed, view=view)
        else:
            # Sem rolagem
            embed = discord.Embed(
                title="📖 A História Continua...",
                description=resposta[:4000],
                color=discord.Color.purple()
            ).set_footer(text=f"Estilo: {estilo.upper()}")
            
            view = ContinueStoryView(bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt)
            await ctx.send(embed=embed, view=view)

    @bot.command(name="cenanarrada")
    @commands.guild_only()
    async def cena_narrada(ctx: commands.Context, *, descricao: str = None):
        """Mestre narra uma cena e a IA expande."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use **no canal da sessão**.")
        
        if not descricao:
            return await ctx.send("❌ Use: `!cenanarrada <descrição da cena>`")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o **mestre** pode narrar cenas. Use `!acao` para ações.")
        
        if sessao.get("status") != "em_andamento":
            return await ctx.send("⚠️ Use o botão 'Iniciar Aventura' primeiro.")
        
        historia = sessao.get("historia", [])
        historia.append({"role": "user", "content": f"Mestre descreve nova cena: {descricao}"})
        
        await ctx.send("🎬 *Expandindo a cena...*")
        
        sistema = sessao.get("sistema", "dnd5e")
        estilo = sessao.get("estilo_narrativo", "extenso")
        
        if estilo == "extenso":
            max_tokens = 1200
            instrucao = "Expanda em 2-4 parágrafos cinematográficos."
        else:
            max_tokens = 600
            instrucao = "MÁXIMO 4 frases. Cenário + elemento principal + momento crítico."

        historia_recente = historia[-20:]
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema) + "\n\n**IMPORTANTE:** Quando apropriado, solicite rolagens de dados aos jogadores. Use o formato EXATO:\n[ROLL: 1d20+modificador, jogadores]\n\nEXEMPLOS CORRETOS:\n- [ROLL: 1d20+3, todos]\n- [ROLL: 2d6, Elara]\n- [ROLL: 1d20, todos]\n\nNUNCA use nomes de perícias ou atributos, APENAS dados (1d20, 2d6, etc)."},
        ] + historia_recente + [
            {"role": "user", "content": f"{instrucao} Se requer rolagens (percepção, combate), SOLICITE com [ROLL: dado, jogadores]."}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=max_tokens)
        
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        salvar_dados()
        
        # Detecta rolagem
        roll_match = re.search(r'\[ROLL:\s*([^,\]]+),\s*([^\]]+)\]', resposta, re.IGNORECASE)
        
        if roll_match:
            roll_type = roll_match.group(1).strip()
            players_str = roll_match.group(2).strip()
            resposta_limpa = re.sub(r'\[ROLL:[^\]]+\]', '', resposta).strip()
            
            fichas_sel = sessao.get("fichas", {})
            players_needed = sessao.get("jogadores", []) if players_str.lower() in ['todos', 'all'] else sessao.get("jogadores", [])
            
            await ctx.send(embed=discord.Embed(
                title="🎬 Nova Cena",
                description=resposta_limpa[:4000],
                color=discord.Color.purple()
            ).set_footer(text=f"Estilo: {estilo.upper()}"))
            
            jogadores_nomes = [ctx.guild.get_member(uid).mention for uid in players_needed if ctx.guild.get_member(uid)]
            
            roll_embed = discord.Embed(
                title="🎲 Rolagem Necessária!",
                description=f"**Tipo:** `{roll_type}`\n**Jogadores:** {', '.join(jogadores_nomes)}",
                color=discord.Color.blue()
            )
            
            view = RollRequestView(bot, sessoes_ativas, salvar_dados, ctx.channel.id, roll_type, players_needed)
            await ctx.send(embed=roll_embed, view=view)
        else:
            embed = discord.Embed(
                title="🎬 Nova Cena",
                description=resposta[:4000],
                color=discord.Color.purple()
            ).set_footer(text=f"Estilo: {estilo.upper()}")
            
            view = ContinueStoryView(bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt)
            await ctx.send(embed=embed, view=view)