# fichas_estruturadas.py
"""
Sistema de fichas estruturadas - REFATORADO
Agora apenas orquestra os subcomandos.
"""

from discord.ext import commands
from commands.fichas_crud import register_fichas_crud_commands
from commands.fichas_edicao import register_fichas_edicao_commands
from commands.fichas_conversao import register_fichas_conversao_commands


def register(bot: commands.Bot):
    """
    Registra TODOS os comandos do sistema de fichas estruturadas.
    
    Comandos CRUD:
    - !ficha
    - !verficha
    - !minhasfichas
    - !deletarficha
    
    Comandos de Edição:
    - !criarficha
    - !editarficha
    
    Comandos de Conversão:
    - !converterficha
    - !exportarficha
    """
    
    # Remove comandos duplicados (segurança)
    for cmd in ["ficha", "criarficha", "verficha", "editarficha", "deletarficha",
                "minhasfichas", "converterficha", "exportarficha"]:
        try:
            bot.remove_command(cmd)
        except Exception:
            pass
    
    # Registra comandos CRUD
    register_fichas_crud_commands(bot)
    print("✅ Comandos CRUD de fichas carregados (ficha, verficha, minhasfichas, deletarficha)")
    
    # Registra comandos de edição
    register_fichas_edicao_commands(bot)
    print("✅ Comandos de edição carregados (criarficha, editarficha)")
    
    # Registra comandos de conversão
    register_fichas_conversao_commands(bot)
    print("✅ Comandos de conversão carregados (converterficha, exportarficha)")