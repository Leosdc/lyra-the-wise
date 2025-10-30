# geracao_conteudo.py (REFATORADO)
"""
Sistema de geração de conteúdo - ARQUIVO PRINCIPAL
Agora modularizado em:
- commands/geracao_npc.py - !npc, !vilao, !motivacao
- commands/geracao_mundo.py - !cena, !nome
- commands/geracao_combate.py - !monstro, !encontro, !armadilha
- commands/geracao_itens.py - !item, !tesouro, !puzzle
"""

from discord.ext import commands
from utils import chamar_groq, get_system_prompt
from config import sistemas_rpg
from sistemas_rpg import SISTEMAS_DISPONIVEIS
from monstros_database import buscar_monstro, listar_monstros_por_sistema, formatar_monstro

# Importa os módulos modularizados
from commands.geracao_npc import register_npc_commands
from commands.geracao_mundo import register_mundo_commands
from commands.geracao_combate import register_combate_commands
from commands.geracao_itens import register_itens_commands


def register(bot: commands.Bot):
    """
    Registra TODOS os comandos de geração de conteúdo.
    
    Comandos registrados:
    - NPCs: !npc, !vilao, !motivacao
    - Mundo: !cena, !nome
    - Combate: !monstro, !monstros, !encontro, !armadilha
    - Itens: !item, !tesouro, !puzzle
    """
    
    # Registra comandos de NPCs
    register_npc_commands(
        bot=bot,
        sistemas_rpg=sistemas_rpg,
        SISTEMAS_DISPONIVEIS=SISTEMAS_DISPONIVEIS,
        chamar_groq=chamar_groq,
        get_system_prompt=get_system_prompt
    )
    
    # Registra comandos de mundo/narrativa
    register_mundo_commands(
        bot=bot,
        sistemas_rpg=sistemas_rpg,
        SISTEMAS_DISPONIVEIS=SISTEMAS_DISPONIVEIS,
        chamar_groq=chamar_groq,
        get_system_prompt=get_system_prompt
    )
    
    # Registra comandos de combate
    register_combate_commands(
        bot=bot,
        sistemas_rpg=sistemas_rpg,
        SISTEMAS_DISPONIVEIS=SISTEMAS_DISPONIVEIS,
        chamar_groq=chamar_groq,
        get_system_prompt=get_system_prompt,
        buscar_monstro=buscar_monstro,
        listar_monstros_por_sistema=listar_monstros_por_sistema,
        formatar_monstro=formatar_monstro
    )
    
    # Registra comandos de itens/tesouros
    register_itens_commands(
        bot=bot,
        sistemas_rpg=sistemas_rpg,
        SISTEMAS_DISPONIVEIS=SISTEMAS_DISPONIVEIS,
        chamar_groq=chamar_groq,
        get_system_prompt=get_system_prompt
    )
    
    print("✅ Sistema de geração de conteúdo carregado (combate, itens, mundo, npc)")