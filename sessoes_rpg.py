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
    
    # Comando de ajuda específico de sessões
    @bot.command(name="ajudasessao")
    async def ajudasessao(ctx: commands.Context):
        """Guia completo do sistema de sessões."""
        descr = (
            "**🎮 Como Criar e Gerenciar Sessões**\n\n"
            
            "**📋 Comandos Básicos**\n"
            "• `!iniciarsessao @jog1 @jog2` — Cria sessão privada\n"
            "• `!selecionarficha Nome` — Escolhe sua ficha\n"
            "• `!sessoes` — Lista sessões ativas\n"
            "• `!pausarsessao` — Pausa/retoma\n"
            "• `!resumosessao` — Resumo com IA\n\n"
            
            "**🎭 Durante a Aventura**\n"
            "• `!acao <descrição>` — Jogadores descrevem ações\n"
            "• `!cenanarrada <descrição>` — Mestre narra cenas\n\n"
            
            "**🎲 Sistema de Rolagens Inteligente**\n"
            "Quando a IA solicita, aparecem botões:\n"
            "• 🎲 Rolar Dados — Rola os dados\n"
            "• 🚫 Não Fazer Nada — Cancela ação\n"
            "• ✏️ Outra Ação — Descreve ação diferente\n\n"
            
            "**🎬 Botões de Controle**\n"
            "• 🎬 Continuar História — Pede próxima cena\n"
            "• ⚔️ Rolar Iniciativa — Rola para TODOS\n\n"
            
            "**💡 Fluxo Completo:**\n"
            "1️⃣ `!iniciarsessao @jogadores`\n"
            "2️⃣ Cada jogador: `!selecionarficha NomePersonagem`\n"
            "3️⃣ Mestre clica **🎬 Iniciar Aventura**\n"
            "4️⃣ Escolhe estilo (Extensa/Concisa)\n"
            "5️⃣ Jogadores usam `!acao`\n"
            "6️⃣ Mestre usa `!cenanarrada`\n"
            "7️⃣ Ao final: `!resumosessao`\n"
            "8️⃣ Clica **🚪 Encerrar Sessão**"
        )
        
        import discord
        await ctx.send(embed=discord.Embed(
            title="📖 Guia Completo — Sessões de RPG",
            description=descr,
            color=discord.Color.blurple()
        ).set_footer(text="Use !rpghelp para ver todos os comandos do bot"))
    
    print("✅ Sistema de sessões carregado (MODULARIZADO)")
