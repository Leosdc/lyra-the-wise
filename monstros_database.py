"""
Módulo de monstros - API unificada.
Mantém compatibilidade com código existente enquanto delega para módulos específicos.

Estrutura de cada monstro:
{
    "nome": str,
    "sistema": str,
    "tipo": str (morto-vivo, besta, humanoide, etc),
    "nd": str/int (nível de desafio),
    "tamanho": str,
    "descricao": str,
    "stats": dict (atributos do sistema),
    "habilidades": list,
    "ataques": list,
    "pv": str,
    "ca": str (classe de armadura),
    "especial": str (habilidades únicas)
}
"""

# Importa dados dos módulos modularizados
from data.monstros_dnd import MONSTROS_DND5E, MONSTROS_PATHFINDER
from data.monstros_horror import MONSTROS_CTHULHU
from data.monstros_outros import MONSTROS_VAMPIRE, MONSTROS_SHADOWRUN

# Importa funções auxiliares
from core.monstros_helpers import (
    BASES_MONSTROS,
    buscar_monstro,
    listar_monstros_por_sistema,
    listar_todos_monstros,
    contar_monstros_por_sistema,
    buscar_monstros_por_tipo,
    buscar_monstros_por_nd,
    formatar_monstro,
    formatar_monstro_compacto,
    get_monstro_aleatorio,
    sistema_tem_monstros,
    get_estatisticas_monstros
)

# Re-exporta tudo para manter compatibilidade
__all__ = [
    # Dados (mantidos para compatibilidade)
    'MONSTROS_DND5E',
    'MONSTROS_PATHFINDER',
    'MONSTROS_CTHULHU',
    'MONSTROS_VAMPIRE',
    'MONSTROS_SHADOWRUN',
    'BASES_MONSTROS',
    
    # Funções principais (mantidas para compatibilidade)
    'buscar_monstro',
    'listar_monstros_por_sistema',
    'formatar_monstro',
    
    # Funções auxiliares adicionais
    'listar_todos_monstros',
    'contar_monstros_por_sistema',
    'buscar_monstros_por_tipo',
    'buscar_monstros_por_nd',
    'formatar_monstro_compacto',
    'get_monstro_aleatorio',
    'sistema_tem_monstros',
    'get_estatisticas_monstros'
]