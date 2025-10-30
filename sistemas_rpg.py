"""
Módulo de sistemas de RPG - API unificada.
Mantém compatibilidade com código existente enquanto delega para módulos específicos.
"""

# Importa dados dos módulos modularizados
from data.sistemas_definicoes import SISTEMAS_DISPONIVEIS, ALIASES
from data.estruturas_fichas import ESTRUTURAS_FICHAS, ESTRUTURA_GENERICA

# Importa funções auxiliares
from core.sistemas_helpers import (
    resolver_alias,
    buscar_sistema,
    listar_por_categoria,
    get_estrutura_ficha,
    listar_todos_sistemas,
    sistema_existe,
    get_dados_sistema,
    get_atributos_sistema,
    get_classes_sistema,
    get_categoria_sistema,
    get_mecanicas_sistema,
    get_nivel_maximo,
    buscar_sistemas_por_categoria,
    buscar_sistemas_por_dado,
    get_info_completa_sistema
)

# Re-exporta tudo para manter compatibilidade
__all__ = [
    # Dados
    'SISTEMAS_DISPONIVEIS',
    'ALIASES',
    'ESTRUTURAS_FICHAS',
    'ESTRUTURA_GENERICA',
    
    # Funções principais (mantidas para compatibilidade)
    'resolver_alias',
    'buscar_sistema',
    'listar_por_categoria',
    'get_estrutura_ficha',
    
    # Funções auxiliares adicionais
    'listar_todos_sistemas',
    'sistema_existe',
    'get_dados_sistema',
    'get_atributos_sistema',
    'get_classes_sistema',
    'get_categoria_sistema',
    'get_mecanicas_sistema',
    'get_nivel_maximo',
    'buscar_sistemas_por_categoria',
    'buscar_sistemas_por_dado',
    'get_info_completa_sistema'
]

print("✅ Sistema de sessões carregado (estrutura de fichas, definições de sistemas, ajuda sobre sistemas)")