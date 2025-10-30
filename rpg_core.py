# rpg_core.py
"""
Módulo principal de RPG - REFATORADO
Agora apenas orquestra os subcomandos.
"""

from discord.ext import commands
from commands.dados import register_dados_commands
from commands.mestre_ia import register_mestre_ia_commands


def register(bot: commands.Bot):
    """
    Registra TODOS os comandos do RPG Core.
    
    Comandos de Dados:
    - !rolar / !r
    
    Comandos de IA:
    - !limpar
    - !mestre
    - !plot
    - !regra
    - !sessao
    """
    
    # Registra comandos de dados
    register_dados_commands(bot)
    print("✅ Comandos de dados carregados (rolar dados)")
    
    # Registra comandos de IA
    register_mestre_ia_commands(bot)
    print("✅ Comandos de IA carregados (mestre, plot, regra, sessao)")