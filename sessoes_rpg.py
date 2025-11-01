# sessoes_rpg.py (REFATORADO)
"""
Sistema de sessões privadas de RPG - ARQUIVO PRINCIPAL
Agora modularizado em:
- views/sessao_views.py (botões interativos)
- core/sessao_helpers.py (funções auxiliares)
- commands/sessoes_commands.py (comandos de sessão)
- commands/sessoes_acao.py (comandos !acao e !cenanarrada)
"""

from discord.ext import commands
from typing import Dict, Any

# Importa módulos modularizados
from commands.sessoes_commands import register_sessoes_commands
from commands.sessoes_acao import register_acao_commands


def setup_sessoes(
    bot: commands.Bot,
    SISTEMAS_DISPONIVEIS: Dict[str, Any],
    fichas_personagens: Dict[str, Any],
    sistemas_rpg: Dict[int, str],
    sessoes_ativas: Dict[int, Dict[str, Any]],
    chamar_groq,
    get_system_prompt,
    salvar_dados,
):
    """
    Registra TODOS os comandos e funcionalidades do sistema de sessões.
    
    Comandos registrados:
    - !iniciarsessao
    - !selecionarficha
    - !sessoes
    - !pausarsessao
    - !resumosessao
    - !acao
    - !cenanarrada
    - !ajudasessao
    """
    
    # Registra comandos de gestão de sessão
    register_sessoes_commands(
        bot=bot,
        SISTEMAS_DISPONIVEIS=SISTEMAS_DISPONIVEIS,
        fichas_personagens=fichas_personagens,
        sistemas_rpg=sistemas_rpg,
        sessoes_ativas=sessoes_ativas,
        chamar_groq=chamar_groq,
        get_system_prompt=get_system_prompt,
        salvar_dados=salvar_dados
    )
    
    # Registra comandos de ação/narrativa
    register_acao_commands(
        bot=bot,
        sessoes_ativas=sessoes_ativas,
        fichas_personagens=fichas_personagens,
        chamar_groq=chamar_groq,
        get_system_prompt=get_system_prompt,
        salvar_dados=salvar_dados
    )

    # ✅ Registra comandos de combate
    from commands.combate_commands import register_combat_commands
    register_combat_commands(
        bot=bot,
        sessoes_ativas=sessoes_ativas,
        fichas_personagens=fichas_personagens,
        salvar_dados=salvar_dados
    )
    
    # Comando de ajuda específico de sessões
    @bot.command(name="ajudasessao")
    async def ajudasessao(ctx: commands.Context):
        """Guia completo do sistema de sessões v3.0."""
        descr = (
        "**🎮 Sistema de Sessões v3.0 — Controle Total do Mestre**\n\n"
        
        "**🎯 NOVA ABORDAGEM:**\n"
        "• Lyra **apenas narra** — não sugere ações nem rolagens\n"
        "• Mestre **controla tudo** — decide quando rolar, combater, etc\n"
        "• Jogadores **declaram ações** — mestre decide o resultado\n\n"
        
        "**📋 Comandos Básicos**\n"
        "• `!iniciarsessao @jog1 @jog2` — Cria sessão privada\n"
        "• `!selecionarficha Nome` — Escolhe sua ficha\n"
        "• `!sessoes` — Lista sessões ativas\n"
        "• `!pausarsessao` — Pausa/retoma\n"
        "• `!resumosessao` — Resumo com IA\n\n"
        
        "**🎭 Durante a Aventura (v3.0)**\n"
        "**[MESTRE]**\n"
        "• `!narrativa <descrição>` — Lyra narra a cena\n"
        "• `!acoespendentes` — Ver ações dos jogadores\n"
        "• `!limparacoes` — Limpar ações após narrativa\n\n"
        
        "**[JOGADORES]**\n"
        "• `!acao <descrição>` — Descrever ação do personagem\n\n"
        
        "**🎮 Botões de Controle do Mestre**\n"
        "Após `!narrativa`, mestre recebe botões:\n"
        "• 🎲 **Solicitar Rolagens** — Escolhe jogadores + tipo de dado\n"
        "• ⚔️ **Iniciar Combate** — Ativa modo tático\n"
        "• 📊 **Status Geral** — HP/CA de todos\n"
        "• 📖 **Ver Ações Pendentes** — Ações declaradas\n\n"
        
        "**⚔️ Sistema de Combate**\n"
        "• `!iniciarcombate` — Ativa modo de combate\n"
        "• `!addinimigo <nome> <HP> <CA>` — Adiciona inimigo\n"
        "• `!rolariniciativa` — Rola para todos\n"
        "• `!statuscombate` — Mostra status atual\n"
        "• `!atacar <alvo> <dano>` — Ataca inimigo\n"
        "• `!curar <alvo> <HP>` — Cura aliado\n"
        "• `!proximoturno` — Avança turno (mestre)\n"
        "• `!encerrarcombate` — Finaliza e salva HP\n\n"
        
        "**🎒 Inventário**\n"
        "• `!inventario` — Ver inventário\n"
        "• `!addinventario <item> [qtd]` — Adicionar item\n"
        "• `!equiparitem <item>` — Equipar arma/armadura\n"
        "• `!usaritem <item>` — Consumir item\n"
        "• `!jogarfora <item>` — Descartar\n"
        "• `!vender <item> [preço]` — Vender item\n\n"
        
        "**📊 XP e Progressão**\n"
        "• `!xp` — Ver XP e progresso\n"
        "• `!darxp <@jogador> <qtd>` — Dar XP individual (mestre)\n"
        "• `!darxpgrupo <qtd>` — Dar XP para todos (mestre)\n\n"
        
        "**💡 Fluxo Completo v3.0:**\n"
        "1️⃣ Mestre: `!iniciarsessao @jogadores`\n"
        "2️⃣ Cada jogador: `!selecionarficha NomePersonagem`\n"
        "3️⃣ Mestre clica **🎬 Iniciar Aventura**\n"
        "4️⃣ Escolhe estilo (Extensa/Concisa)\n"
        "5️⃣ Mestre: `!narrativa Os heróis entram na taverna...`\n"
        "6️⃣ Lyra narra a cena (SEM sugerir ações)\n"
        "7️⃣ Jogadores: `!acao Aproximo do balcão`\n"
        "8️⃣ Mestre: [Clica **Ver Ações Pendentes**]\n"
        "9️⃣ Mestre: [Decide se solicita rolagens ou continua]\n"
        "🔟 Se combate: Mestre clica **⚔️ Iniciar Combate**\n"
        "1️⃣ 1. Durante combate: `!atacar`, `!curar`, `!proximoturno`\n"
        "1️⃣ 2. Fim combate: `!encerrarcombate` (HP salvo automaticamente)\n"
        "1️⃣ 3. Recompensas: `!darxpgrupo 300` + `!addinventario`\n"
        "1️⃣ 4. Fim sessão: `!resumosessao` → **🚪 Encerrar Sessão**\n\n"
        
        "**🆕 Diferenças da v3.0:**\n"
        "❌ Lyra NÃO detecta combate automaticamente\n"
        "❌ Lyra NÃO solicita rolagens sozinha\n"
        "❌ Lyra NÃO toma decisões de mecânica\n"
        "✅ Mestre escolhe QUANDO e QUEM rola dados\n"
        "✅ Mestre decide QUANDO iniciar combate\n"
        "✅ Controle total sobre o ritmo da história"
        )
        
        import discord
        await ctx.send(embed=discord.Embed(
            title="📖 Guia Completo — Sessões v3.0",
            description=descr,
            color=discord.Color.blurple()
        ).set_footer(text="Use !rpghelp para ver todos os comandos do bot v3.0"))
