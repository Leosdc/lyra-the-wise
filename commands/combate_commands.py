"""
Comandos de combate para Lyra RPG Bot.
"""

import discord
from discord.ext import commands
from typing import Dict, Any, Callable
import random
from core.combat_system import CombatTracker, extract_character_stats


def ensure_combat_tracker(sessao: Dict[str, Any]) -> None:
    """Garante que combat é um CombatTracker, não um dict."""
    if "combat" in sessao and isinstance(sessao["combat"], dict):
        sessao["combat"] = CombatTracker.from_dict(sessao["combat"])
    elif "combat" not in sessao:
        sessao["combat"] = CombatTracker()


def safe_save(sessao: Dict[str, Any], salvar_dados: Callable) -> None:
    """Serializa combat e salva dados de forma segura."""
    if "combat" in sessao and isinstance(sessao["combat"], CombatTracker):
        sessao["combat"] = sessao["combat"].to_dict()
    salvar_dados()


def register_combat_commands(
    bot: commands.Bot,
    sessoes_ativas: Dict[int, Dict[str, Any]],
    fichas_personagens: Dict[str, Any],
    salvar_dados: Callable
):
    """Registra todos os comandos de combate."""
    
    @bot.command(name="iniciarcombate")
    async def start_combat(ctx: commands.Context):
        """Inicia o modo de combate."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o mestre pode iniciar combate.")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        if combat.is_active:
            return await ctx.send("⚠️ Já há um combate ativo!")
        
        combat.start_combat()
        
        # Adiciona jogadores automaticamente
        fichas_sel = sessao.get("fichas", {})
        jogadores_adicionados = 0
        
        print(f"🔍 DEBUG: fichas_sel = {fichas_sel}")
        print(f"🔍 DEBUG: jogadores na sessão = {sessao.get('jogadores', [])}")
        
        for player_id in sessao.get("jogadores", []):
            print(f"\n--- Processando jogador {player_id} ---")
            
            user = bot.get_user(player_id)
            if not user:
                print(f"❌ User não encontrado no Discord")
                continue
            
            # Busca chave da ficha selecionada (formato: "player_id_nome")
            chave_ficha = fichas_sel.get(str(player_id)) or fichas_sel.get(player_id)
            print(f"🔍 chave_ficha selecionada: {chave_ficha}")
            
            if not chave_ficha:
                print(f"❌ Nenhuma ficha selecionada para este jogador")
                await ctx.send(f"⚠️ {user.mention}, você precisa selecionar uma ficha com `!selecionarficha`")
                continue
            
            # Busca a ficha diretamente pela chave (formato: "player_id_nome")
            print(f"🔍 Buscando ficha com chave: {chave_ficha}")
            print(f"🔍 Keys disponíveis em fichas_personagens: {list(fichas_personagens.keys())[:5]}...")
            
            if chave_ficha not in fichas_personagens:
                print(f"❌ Ficha '{chave_ficha}' NÃO encontrada em fichas_personagens")
                await ctx.send(f"⚠️ Ficha de {user.mention} não foi encontrada. Use `!criarficha` ou `!ficha`")
                continue
            
            ficha = fichas_personagens[chave_ficha]
            print(f"✅ Ficha carregada: {ficha.get('nome', 'SEM NOME')}")
            
            # Extrai o nome do personagem
            nome_personagem = ficha.get("nome", f"Jogador_{player_id}")
            print(f"🎭 Nome do personagem: {nome_personagem}")
            
            # Extrai stats da ficha estruturada
            secoes = ficha.get("secoes", {})
            recursos = secoes.get("recursos", {}) if secoes else {}
            combate_data = secoes.get("combate", {}) if secoes else {}
            
            print(f"🔍 secoes encontradas: {list(secoes.keys()) if secoes else 'NENHUMA'}")
            print(f"🔍 recursos: {recursos}")
            print(f"🔍 combate: {combate_data}")
            
            # Garante que são inteiros - busca em múltiplos formatos
            try:
                hp_max = recursos.get("HP Máximo") or recursos.get("HP Máximo") or recursos.get("Pontos de Vida")
                hp_max = int(hp_max) if hp_max else 10
            except (ValueError, TypeError):
                hp_max = 10
            
            try:
                hp_atual = recursos.get("HP Atual") or recursos.get("HP Atual")
                hp_atual = int(hp_atual) if hp_atual else hp_max
            except (ValueError, TypeError):
                hp_atual = hp_max
            
            try:
                ca = combate_data.get("CA") or combate_data.get("Classe de Armadura")
                ca = int(ca) if ca else 10
            except (ValueError, TypeError):
                ca = 10
            
            print(f"✅ Stats extraídos - HP: {hp_atual}/{hp_max}, CA: {ca}")
            
            combat.add_participant(
                name=str(nome_personagem),
                hp=hp_atual,
                max_hp=hp_max,
                ca=ca,
                is_player=True,
                player_id=player_id
            )
            jogadores_adicionados += 1
            print(f"✅ {nome_personagem} adicionado ao combate!")
        
        print(f"\n🎯 TOTAL de jogadores adicionados: {jogadores_adicionados}")
        print(f"🎯 Participantes no combat: {list(combat.participants.keys())}")
        
        safe_save(sessao, salvar_dados)
        
        await ctx.send(
            embed=discord.Embed(
                title="⚔️ Combate Iniciado!",
                description=(
                    f"**Jogadores adicionados:** {jogadores_adicionados}\n\n"
                    f"**Próximos passos:**\n"
                    f"1. Use `!addinimigo <nome> <HP> <CA>` para cada inimigo\n"
                    f"2. Use `!statuscombate` para ver status\n"
                    f"3. Use `!rolariniciativa` para começar\n"
                    f"4. Use `!atacar <alvo> <dano>` para atacar\n"
                    f"5. Use `!curar <HP> <dano>` para curar\n"
                    f"6. Use `!proximoturno` para passar para o próximo turno\n"
                    f"7. Use `!encerrarcombate` para encerrar o combate\n"
                    f"Obs.: Se nome composto, usar aspas duplas + <nome composto>"
                    f"Exemplo: ''nome_personagem'' <HP> <CA>"
                ),
                color=discord.Color.red()
            )
        )
    
    @bot.command(name="addinimigo")
    async def add_enemy(ctx: commands.Context, nome: str, hp: str, ca: str, bonus_ini: str = "0"):
        """Adiciona um inimigo ao combate."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o mestre pode adicionar inimigos.")
        
        # Converte parâmetros
        try:
            hp_int = int(hp)
            ca_int = int(ca)
            bonus_ini_int = int(bonus_ini)
        except ValueError:
            return await ctx.send("❌ HP, CA e bônus de iniciativa devem ser números!")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        if not combat.is_active:
            return await ctx.send("❌ Use `!iniciarcombate` primeiro!")
        
        combat.add_participant(
            name=nome,
            hp=hp_int,
            max_hp=hp_int,
            ca=ca_int,
            is_player=False,
            bonus_ini=bonus_ini_int
        )
        
        safe_save(sessao, salvar_dados)
        
        await ctx.send(f"✅ **{nome}** adicionado ao combate! (HP: {hp_int}, CA: {ca_int}, Bônus Ini: +{bonus_ini_int})")
    
    @bot.command(name="rolariniciativa")
    async def roll_initiative(ctx: commands.Context):
        """Rola iniciativa para todos os participantes do combate."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        if not combat.is_active:
            return await ctx.send("❌ Use `!iniciarcombate` primeiro!")
        
        # Lista para armazenar resultados detalhados
        iniciativas = []
        
        # Rola iniciativa para cada participante
        for nome, participante in combat.participants.items():
            bonus = participante.get("bonus_ini", 0)
            
            # Se for jogador, tenta pegar bônus de Destreza da ficha
            if participante.get("tipo") == "jogador":
                player_id = participante.get("player_id")
                if player_id and player_id in fichas_personagens:
                    ficha_id = fichas_personagens[player_id].get("ficha_selecionada")
                    fichas = fichas_personagens[player_id].get("fichas", {})
                    
                    if ficha_id and ficha_id in fichas:
                        ficha = fichas[ficha_id]
                        atributos = ficha.get("atributos", {})
                        destreza = atributos.get("Destreza", 10)
                        try:
                            destreza_int = int(destreza)
                            bonus = (destreza_int - 10) // 2
                        except (ValueError, TypeError):
                            bonus = 0
            
            # Rola APENAS o d20 puro
            rolagem = random.randint(1, 20)
            # Total = rolagem + bônus (calculado apenas aqui, uma única vez)
            total = rolagem + bonus
            
            # Atualiza iniciativa no combate
            participante["initiative"] = total
            
            iniciativas.append((nome, total, rolagem, bonus, participante["tipo"]))
        
        # Ordena por iniciativa (maior primeiro)
        iniciativas.sort(key=lambda x: x[1], reverse=True)
        combat.turn_order = [nome for nome, *_ in iniciativas]
        combat.current_turn_index = 0
        
        # Monta embed com ordem de iniciativa
        desc = ""
        medalhas = ["🥇", "🥈", "🥉"]
        
        for i, (nome, total, rolagem, bonus, tipo) in enumerate(iniciativas):
            emoji = "👤" if tipo == "jogador" else "👹"
            medal = medalhas[i] if i < 3 else f"**{i+1}.**"
            
            # Mostra o cálculo detalhado
            if bonus != 0:
                desc += f"{medal} {emoji} **{nome}** → 🎲 {rolagem} + {bonus:+d} = **{total}**\n"
            else:
                desc += f"{medal} {emoji} **{nome}** → 🎲 {rolagem} = **{total}**\n"
        
        safe_save(sessao, salvar_dados)
        
        embed = discord.Embed(
            title="⚔️ Iniciativa Rolada!",
            description=desc,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"🎯 Turno de: {combat.turn_order[0]}")
        
        await ctx.send(embed=embed)
    
    @bot.command(name="statuscombate")
    async def combat_status(ctx: commands.Context):
        """Mostra status completo do combate."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        status = combat.get_status()
        await ctx.send(status)
    
    @bot.command(name="atacar")
    async def attack(ctx: commands.Context, alvo: str, dano: int):
        """Ataca um alvo causando dano."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        if not combat.is_active:
            return await ctx.send("❌ Não há combate ativo!")
        
        # Normaliza nome do alvo
        alvo_real = None
        for name in combat.participants.keys():
            if name.lower() == alvo.lower():
                alvo_real = name
                break
        
        if not alvo_real:
            return await ctx.send(f"❌ Alvo '{alvo}' não encontrado no combate!")
        
        # Aplica dano
        died = combat.apply_damage(alvo_real, dano)
        
        if died:
            await ctx.send(f"💀 **{alvo_real}** foi derrotado! ({dano} de dano)")
        else:
            hp_restante = combat.participants[alvo_real]["hp"]
            await ctx.send(f"⚔️ **{alvo_real}** recebeu {dano} de dano! (HP: {hp_restante})")
        
        # Verifica fim de combate
        winner = combat.check_combat_end()
        if winner:
            if winner == "players":
                await ctx.send("🎉 **Vitória!** Todos os inimigos foram derrotados!")
            else:
                await ctx.send("💀 **Derrota...** Todos os jogadores caíram.")
            
            await ctx.send("Use `!encerrarcombate` para finalizar e salvar HP.")
        
        safe_save(sessao, salvar_dados)
    
    @bot.command(name="curar")
    async def heal(ctx: commands.Context, alvo: str, quantidade: int):
        """Cura um aliado."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        if not combat.is_active:
            return await ctx.send("❌ Não há combate ativo!")
        
        # Normaliza nome do alvo
        alvo_real = None
        for name in combat.participants.keys():
            if name.lower() == alvo.lower():
                alvo_real = name
                break
        
        if not alvo_real:
            return await ctx.send(f"❌ Alvo '{alvo}' não encontrado!")
        
        combat.heal(alvo_real, quantidade)
        hp_atual = combat.participants[alvo_real]["hp"]
        hp_max = combat.participants[alvo_real]["max_hp"]
        
        safe_save(sessao, salvar_dados)
        
        await ctx.send(f"💚 **{alvo_real}** foi curado em {quantidade} HP! (HP: {hp_atual}/{hp_max})")
    
    @bot.command(name="proximoturno")
    async def next_turn(ctx: commands.Context):
        """Avança para o próximo turno."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o mestre pode avançar turnos.")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        if not combat.is_active:
            return await ctx.send("❌ Não há combate ativo!")
        
        combat.next_turn()
        current = combat.get_current_turn()
        
        safe_save(sessao, salvar_dados)
        
        await ctx.send(f"⏭️ **Próximo turno:** {current} | Rodada {combat.round}")
    
    @bot.command(name="encerrarcombate")
    async def end_combat(ctx: commands.Context):
        """Encerra o combate e salva HP nas fichas."""
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Não há sessão ativa neste canal.")
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o mestre pode encerrar combate.")
        
        ensure_combat_tracker(sessao)
        combat: CombatTracker = sessao["combat"]
        
        if not combat.is_active:
            return await ctx.send("❌ Não há combate ativo!")
        
        # Pega HP final dos jogadores
        player_hp = combat.end_combat()
        
        # Atualiza fichas
        for player_name, hp in player_hp.items():
            if player_name in fichas_personagens:
                fichas_personagens[player_name]["hp_atual"] = hp
        
        safe_save(sessao, salvar_dados)
        
        await ctx.send(
            embed=discord.Embed(
                title="🏁 Combate Encerrado",
                description="HP dos jogadores foi salvo nas fichas.",
                color=discord.Color.green()
            )
        )