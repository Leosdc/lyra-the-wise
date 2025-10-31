"""
Funções auxiliares para trabalhar com monstros.
"""

from data.monstros_dnd import MONSTROS_DND5E, MONSTROS_PATHFINDER
from data.monstros_horror import MONSTROS_CTHULHU
from data.monstros_outros import MONSTROS_VAMPIRE, MONSTROS_SHADOWRUN


# Mapeamento de todos os bancos de monstros
BASES_MONSTROS = {
    "dnd5e": MONSTROS_DND5E,
    "pathfinder": MONSTROS_PATHFINDER,
    "cthulhu": MONSTROS_CTHULHU,
    "vampire": MONSTROS_VAMPIRE,
    "shadowrun": MONSTROS_SHADOWRUN
}


def buscar_monstro(nome, sistema=None):
    """
    Busca um monstro por nome, opcionalmente filtrando por sistema.
    
    Args:
        nome: Nome do monstro a buscar (case-insensitive)
        sistema: Sistema específico para buscar (opcional)
        
    Returns:
        dict: Dados do monstro ou None se não encontrado
    """
    nome_lower = nome.lower()
    
    # Se sistema específico
    if sistema and sistema in BASES_MONSTROS:
        for key, monstro in BASES_MONSTROS[sistema].items():
            if nome_lower in key or nome_lower in monstro["nome"].lower():
                return monstro
        return None
    
    # Busca em todos os sistemas
    for sistema_key, monstros in BASES_MONSTROS.items():
        for key, monstro in monstros.items():
            if nome_lower in key or nome_lower in monstro["nome"].lower():
                return monstro
    
    return None


def listar_monstros_por_sistema(sistema):
    """
    Lista todos os monstros disponíveis para um sistema.
    
    Args:
        sistema: Código do sistema (dnd5e, pathfinder, etc)
        
    Returns:
        list: Lista de nomes de monstros
    """
    if sistema not in BASES_MONSTROS:
        return []
    
    return [m["nome"] for m in BASES_MONSTROS[sistema].values()]


def listar_todos_monstros():
    """
    Lista todos os monstros de todos os sistemas.
    
    Returns:
        dict: {sistema: [nomes]}
    """
    resultado = {}
    for sistema, monstros in BASES_MONSTROS.items():
        resultado[sistema] = [m["nome"] for m in monstros.values()]
    return resultado


def contar_monstros_por_sistema():
    """
    Retorna contagem de monstros por sistema.
    
    Returns:
        dict: {sistema: quantidade}
    """
    return {sistema: len(monstros) for sistema, monstros in BASES_MONSTROS.items()}


def buscar_monstros_por_tipo(tipo, sistema=None):
    """
    Busca monstros por tipo (aberração, morto-vivo, etc).
    
    Args:
        tipo: Tipo do monstro a buscar
        sistema: Sistema específico (opcional)
        
    Returns:
        list: Lista de monstros que correspondem ao tipo
    """
    tipo_lower = tipo.lower()
    resultado = []
    
    bases = {sistema: BASES_MONSTROS[sistema]} if sistema and sistema in BASES_MONSTROS else BASES_MONSTROS
    
    for sistema_key, monstros in bases.items():
        for monstro in monstros.values():
            if tipo_lower in monstro.get("tipo", "").lower():
                resultado.append(monstro)
    
    return resultado


def buscar_monstros_por_nd(nd, sistema=None):
    """
    Busca monstros por nível de desafio.
    
    Args:
        nd: Nível de desafio (pode ser string ou número)
        sistema: Sistema específico (opcional)
        
    Returns:
        list: Lista de monstros com o ND especificado
    """
    nd_str = str(nd)
    resultado = []
    
    bases = {sistema: BASES_MONSTROS[sistema]} if sistema and sistema in BASES_MONSTROS else BASES_MONSTROS
    
    for sistema_key, monstros in bases.items():
        for monstro in monstros.values():
            if "nd" in monstro and str(monstro["nd"]) == nd_str:
                resultado.append(monstro)
    
    return resultado


def formatar_monstro(monstro):
    """
    Formata os dados do monstro para exibição.
    
    Args:
        monstro: Dicionário com dados do monstro
        
    Returns:
        str: Texto formatado do monstro
    """
    if not monstro:
        return "Monstro não encontrado."
    
    texto = f"**{monstro['nome']}**\n"
    texto += f"*{monstro.get('tipo', 'Desconhecido')}*\n\n"
    texto += f"{monstro['descricao']}\n\n"
    
    # ND/Desafio
    if 'nd' in monstro:
        texto += f"**ND:** {monstro['nd']}\n"
    if 'tamanho' in monstro:
        texto += f"**Tamanho:** {monstro['tamanho']}\n"
    
    # Stats
    if 'stats' in monstro:
        if isinstance(monstro['stats'], dict):
            stats_texto = ", ".join([f"{k}: {v}" for k, v in monstro['stats'].items()])
            texto += f"**Atributos:** {stats_texto}\n"
        else:
            texto += f"**Atributos:** {monstro['stats']}\n"
    
    # PV e Defesas
    if 'pv' in monstro:
        texto += f"**PV:** {monstro['pv']}\n"
    if 'ca' in monstro:
        texto += f"**CA:** {monstro['ca']}\n"
    if 'armadura' in monstro:
        texto += f"**Armadura:** {monstro['armadura']}\n"
    
    # Ataques
    if 'ataques' in monstro and monstro['ataques']:
        texto += f"\n**Ataques:**\n"
        for ataque in monstro['ataques']:
            texto += f"• {ataque}\n"
    
    # Habilidades
    if 'habilidades' in monstro and monstro['habilidades']:
        texto += f"\n**Habilidades:**\n"
        for hab in monstro['habilidades']:
            if isinstance(hab, str):
                texto += f"• {hab}\n"
            else:
                texto += f"• {hab}\n"
    
    # Disciplinas (para Vampire)
    if 'disciplinas' in monstro:
        texto += f"\n**Disciplinas:**\n"
        for disc, nivel in monstro['disciplinas'].items():
            texto += f"• {disc}: {nivel}\n"
    
    # Especial
    if 'especial' in monstro:
        texto += f"\n**Especial:** {monstro['especial']}\n"
    
    return texto


def formatar_monstro_compacto(monstro):
    """
    Formata monstro de forma compacta (para listas).
    
    Args:
        monstro: Dicionário com dados do monstro
        
    Returns:
        str: Texto formatado compacto
    """
    if not monstro:
        return "Monstro não encontrado."
    
    nd_texto = f" (ND {monstro['nd']})" if 'nd' in monstro else ""
    return f"**{monstro['nome']}**{nd_texto} - {monstro.get('tipo', 'Desconhecido')}"


def get_monstro_aleatorio(sistema=None):
    """
    Retorna um monstro aleatório.
    
    Args:
        sistema: Sistema específico (opcional)
        
    Returns:
        dict: Dados de um monstro aleatório
    """
    import random
    
    if sistema and sistema in BASES_MONSTROS:
        monstros_lista = list(BASES_MONSTROS[sistema].values())
    else:
        # Pega de todos os sistemas
        monstros_lista = []
        for monstros in BASES_MONSTROS.values():
            monstros_lista.extend(monstros.values())
    
    if not monstros_lista:
        return None
    
    return random.choice(monstros_lista)


def sistema_tem_monstros(sistema):
    """
    Verifica se um sistema tem monstros cadastrados.
    
    Args:
        sistema: Código do sistema
        
    Returns:
        bool: True se tem monstros, False caso contrário
    """
    return sistema in BASES_MONSTROS and len(BASES_MONSTROS[sistema]) > 0


def get_estatisticas_monstros():
    """
    Retorna estatísticas gerais sobre os monstros cadastrados.
    
    Returns:
        dict: Estatísticas (total, por sistema, etc)
    """
    total = sum(len(monstros) for monstros in BASES_MONSTROS.values())
    por_sistema = contar_monstros_por_sistema()
    
    return {
        "total": total,
        "por_sistema": por_sistema,
        "sistemas_disponiveis": list(BASES_MONSTROS.keys())
    }