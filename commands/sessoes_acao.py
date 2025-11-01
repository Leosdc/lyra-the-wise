# commands/sessoes_acao.py
"""Comandos !acao e !cenanarrada com sistema de rolagens interativo."""

import discord
from discord.ext import commands
import re

from views.sessao_roll_views import RollRequestView
from views.sessao_continue_views import ContinueStoryView


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

        # SISTEMA DE CONTROLE DE AÇÕES - Inicializa se não existir
        if "acoes_pendentes" not in sessao:
            sessao["acoes_pendentes"] = {}
        
        # Se há rolagem/ação ativa definida pela IA, registra que este jogador agiu
        if "players_needed_action" in sessao and sessao["players_needed_action"]:
            if ctx.author.id in sessao["players_needed_action"]:
                sessao["acoes_pendentes"][ctx.author.id] = descricao
                salvar_dados()
                
                # Verifica se todos já agiram
                total_esperados = len(sessao["players_needed_action"])
                # Conta quem já respondeu (rolls + skipped + acoes)
                # Observação: listas podem ser preenchidas pela View de rolagem
                rolls_done = len(sessao.get("rolls_done_ids", []))
                skipped = len(sessao.get("players_skipped_ids", []))
                acoes = len(sessao["acoes_pendentes"])
                
                total_respostas = rolls_done + skipped + acoes
                
                if total_respostas < total_esperados:
                    # Ainda faltam pessoas — mostra a ação do jogador e aguarda
                    await ctx.send(embed=discord.Embed(
                        title=f"🎭 {nome_personagem} age!",
                        description=descricao,
                        color=discord.Color.blue()
                    ).set_footer(text=f"Jogador: {ctx.author.display_name}"))
                    
                    faltam = total_esperados - total_respostas
                    await ctx.send(
                        f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} responder (rolar, não fazer nada ou !acao)..."
                    )
                    return  # ❗ NÃO gera resposta ainda e NÃO adiciona ao histórico
                else:
                    # TODOS responderam! Limpa flags e continua o fluxo normal
                    sessao.pop("players_needed_action", None)
                    sessao.pop("rolls_done_ids", None)
                    sessao.pop("players_skipped_ids", None)
                    sessao["acoes_pendentes"] = {}
                    salvar_dados()
                    
                    await ctx.send(
                        embed=discord.Embed(
                            title="✅ Todos Responderam!",
                            description="Gerando consequências...",
                            color=discord.Color.green()
                        )
                    )

        # Adiciona ao histórico (apenas quando já podemos prosseguir)
        historia = sessao.get("historia", [])
        historia.append({"role": "user", "content": f"Ação de {nome_personagem}: {descricao}"})
        
        # Envia mensagem visual da ação
        await ctx.send(embed=discord.Embed(
            title=f"🎭 {nome_personagem} age!",
            description=descricao,
            color=discord.Color.blue()
        ).set_footer(text=f"Jogador: {ctx.author.display_name}"))
        
        # VERIFICA SE TODOS JÁ AGIRAM NESTE TURNO (iniciativa)
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
            max_tokens = 400
            instrucao = "MÁXIMO 4 FRASES CURTAS. Uma frase por evento principal. SEJA EXTREMAMENTE DIRETO."
        
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

        # ✅ DETECÇÃO AUTOMÁTICA DE COMBATE
        from core.combat_system import detect_combat_in_text
        
        is_combat, enemies_found = detect_combat_in_text(resposta)
        
        if is_combat and not sessao.get("combat"):
            # Iniciou combate! Notifica e sugere adicionar inimigos
            await ctx.send(
                embed=discord.Embed(
                    title="⚔️ Combate Detectado!",
                    description=(
                        f"A narrativa indica início de combate!\n\n"
                        f"**Inimigos detectados:** {', '.join(enemies_found) if enemies_found else 'Não identificados'}\n\n"
                        f"**Próximos passos:**\n"
                        f"1. Use `!iniciarcombate` para ativar sistema\n"
                        f"2. Use `!addinimigo <nome> <HP> <CA>` para cada inimigo\n"
                        f"3. Use o botão **⚔️ Rolar Iniciativa** para começar"
                    ),
                    color=discord.Color.red()
                ).set_footer(text="💡 Combate é opcional — você pode continuar narrativamente também")
            )
        
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
                description=(
                    f"**Tipo:** `{roll_type}`\n"
                    f"**Jogadores:** {', '.join(jogadores_nomes)}\n\n"
                    f"**Opções:**\n"
                    f"🎲 Rolar os dados solicitados\n"
                    f"🚫 Não fazer nada (ignorar ação)\n"
                    f"✏️ Usar `!acao <descrição>` para fazer outra coisa"
                ),
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
            max_tokens = 400
            instrucao = "MÁXIMO 3 FRASES. Cenário em 1 frase + gancho em 1 frase. NADA MAIS."

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

        # ✅ DETECÇÃO AUTOMÁTICA DE COMBATE COM AUTO-ADICIONAR
        from core.combat_system import detect_combat_in_text, CombatTracker
        
        is_combat, enemies_data = detect_combat_in_text(resposta)
        
        if is_combat and not sessao.get("combat"):
            # Iniciou combate! Cria tracker e adiciona inimigos automaticamente
            await ctx.send(
                embed=discord.Embed(
                    title="⚔️ Combate Detectado!",
                    description="A IA detectou início de combate! Preparando sistema...",
                    color=discord.Color.red()
                )
            )
            
            # Cria combat tracker
            from core.combat_system import CombatTracker, extract_character_stats
            
            combat = CombatTracker()
            combat.start_combat()
            
            # Adiciona jogadores automaticamente
            for player_id in sessao.get("jogadores", []):
                user = ctx.guild.get_member(player_id) if ctx.guild else None
                if not user:
                    continue
                
                # Busca ficha do jogador
                ficha_nome = sessao.get("fichas_selecionadas", {}).get(player_id)
                if not ficha_nome:
                    # Usa fichas alternativas
                    fichas_sel = sessao.get("fichas", {})
                    chave = fichas_sel.get(str(player_id)) or fichas_sel.get(player_id)
                    if chave:
                        ficha_nome = chave
                
                if ficha_nome:
                    ficha = fichas_personagens.get(ficha_nome)
                    if ficha:
                        hp_max, hp_atual, ca = extract_character_stats(ficha)
                        nome_personagem = ficha.get("nome", user.display_name)
                        combat.add_participant(
                            name=nome_personagem,
                            hp=hp_atual,
                            max_hp=hp_max,
                            ca=ca,
                            is_player=True
                        )
            
            # Adiciona inimigos detectados automaticamente
            inimigos_adicionados = []
            if enemies_data:
                for enemy in enemies_data:
                    quantidade = enemy["quantidade"]
                    tipo = enemy["nome"]
                    hp = enemy["hp_sugerido"]
                    ca = enemy["ca_sugerido"]
                    
                    if quantidade == 1:
                        nome_inimigo = tipo
                        combat.add_participant(
                            name=nome_inimigo,
                            hp=hp,
                            max_hp=hp,
                            ca=ca,
                            is_player=False
                        )
                        inimigos_adicionados.append(f"• {nome_inimigo} (HP: {hp}, CA: {ca})")
                    else:
                        for i in range(1, quantidade + 1):
                            nome_inimigo = f"{tipo} {i}"
                            combat.add_participant(
                                name=nome_inimigo,
                                hp=hp,
                                max_hp=hp,
                                ca=ca,
                                is_player=False
                            )
                            inimigos_adicionados.append(f"• {nome_inimigo} (HP: {hp}, CA: {ca})")
            
            sessao["combat"] = combat.to_dict()
            salvar_dados()
            
            # Notifica
            if inimigos_adicionados:
                await ctx.send(
                    embed=discord.Embed(
                        title="✅ Combate Iniciado Automaticamente!",
                        description=(
                            f"**Inimigos adicionados:**\n" + "\n".join(inimigos_adicionados) + "\n\n"
                            f"**Próximos passos:**\n"
                            f"1. Use `!rolariniciativa` para rolar iniciativa\n"
                            f"2. Use `!statuscombate` para ver status\n"
                            f"3. Use `!atacar <alvo> <dano>` para atacar\n"
                            f"4. Use `!encerrarcombate` quando terminar"
                        ),
                        color=discord.Color.green()
                    )
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="⚠️ Combate Iniciado - Adicione Inimigos",
                        description=(
                            "A IA detectou combate mas não identificou inimigos específicos.\n\n"
                            "**Adicione manualmente:**\n"
                            "`!addinimigo <nome> <HP> <CA>`\n\n"
                            "Depois use `!rolariniciativa`"
                        ),
                        color=discord.Color.orange()
                    )
                )
        
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
