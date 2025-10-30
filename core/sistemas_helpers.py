"""
Funções auxiliares para trabalhar com sistemas de RPG.
"""

from data.sistemas_definicoes import SISTEMAS_DISPONIVEIS, ALIASES
from data.estruturas_fichas import ESTRUTURAS_FICHAS, ESTRUTURA_GENERICA


def resolver_alias(alias: str):
    """Resolve um alias para a chave do sistema, mantendo busca case-insensitive."""
    if not isinstance(alias, str):
        return alias
    key = alias.strip().lower()
    return ALIASES.get(key, key)


def buscar_sistema(sistema_key: str):
    """
    Retorna o dicionário de um sistema pelo código ou alias.
    Se não encontrado, retorna D&D 5e como padrão.
    """
    key = resolver_alias(sistema_key)
    return SISTEMAS_DISPONIVEIS.get(key, SISTEMAS_DISPONIVEIS["dnd5e"])


def listar_por_categoria():
    """Agrupa sistemas por categoria, retornando dict[Categoria] -> [(codigo, nome)]."""
    categorias = {}
    for codigo, info in SISTEMAS_DISPONIVEIS.items():
        cat = info.get("categoria", "Outros")
        categorias.setdefault(cat, []).append((codigo, info.get("nome", codigo)))
    return categorias


def get_estrutura_ficha(sistema_key: str):
    """
    Retorna a estrutura de ficha apropriada para o sistema.
    Se não houver estrutura específica, retorna estrutura genérica.
    """
    key = resolver_alias(sistema_key)
    
    if key in ESTRUTURAS_FICHAS:
        return ESTRUTURAS_FICHAS[key]
    
    return ESTRUTURA_GENERICA


def listar_todos_sistemas():
    """Retorna lista de tuplas (codigo, nome) de todos os sistemas disponíveis."""
    return [(codigo, info["nome"]) for codigo, info in SISTEMAS_DISPONIVEIS.items()]


def sistema_existe(sistema_key: str) -> bool:
    """Verifica se um sistema existe (por código ou alias)."""
    key = resolver_alias(sistema_key)
    return key in SISTEMAS_DISPONIVEIS


def get_dados_sistema(sistema_key: str) -> list:
    """Retorna a lista de dados utilizados por um sistema."""
    sistema = buscar_sistema(sistema_key)
    return sistema.get("dados", ["d20"])


def get_atributos_sistema(sistema_key: str) -> list:
    """Retorna a lista de atributos de um sistema."""
    sistema = buscar_sistema(sistema_key)
    return sistema.get("atributos", [])


def get_classes_sistema(sistema_key: str) -> list:
    """Retorna a lista de classes/profissões de um sistema."""
    sistema = buscar_sistema(sistema_key)
    return sistema.get("classes", [])


def get_categoria_sistema(sistema_key: str) -> str:
    """Retorna a categoria de um sistema."""
    sistema = buscar_sistema(sistema_key)
    return sistema.get("categoria", "Outros")


def get_mecanicas_sistema(sistema_key: str) -> str:
    """Retorna a descrição das mecânicas de um sistema."""
    sistema = buscar_sistema(sistema_key)
    return sistema.get("mecanicas", "Mecânicas não especificadas")


def get_nivel_maximo(sistema_key: str):
    """Retorna o nível máximo de um sistema."""
    sistema = buscar_sistema(sistema_key)
    return sistema.get("nivel_max", "N/A")


def buscar_sistemas_por_categoria(categoria: str) -> list:
    """Retorna lista de sistemas de uma categoria específica."""
    return [
        (codigo, info["nome"]) 
        for codigo, info in SISTEMAS_DISPONIVEIS.items() 
        if info.get("categoria", "").lower() == categoria.lower()
    ]


def buscar_sistemas_por_dado(tipo_dado: str) -> list:
    """Retorna lista de sistemas que usam um tipo específico de dado."""
    return [
        (codigo, info["nome"]) 
        for codigo, info in SISTEMAS_DISPONIVEIS.items() 
        if tipo_dado.lower() in [d.lower() for d in info.get("dados", [])]
    ]


def get_info_completa_sistema(sistema_key: str) -> dict:
    """Retorna todas as informações de um sistema, incluindo estrutura de ficha."""
    sistema = buscar_sistema(sistema_key)
    estrutura = get_estrutura_ficha(sistema_key)
    
    return {
        **sistema,
        "estrutura_ficha": estrutura
    }