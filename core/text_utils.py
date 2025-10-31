# core/text_utils.py
"""Utilidades para manipulação de texto."""

import re


def key_from_name(text):
    """
    Gera uma chave unica a partir de um texto.
    
    Args:
        text: Texto para converter em chave
    
    Returns:
        str: Chave normalizada (apenas letras minúsculas, números e underscores)
    
    Exemplo:
        >>> key_from_name("Aragorn Filho de Arathorn")
        'aragorn_filho_de_arathorn'
    """
    return re.sub(r'[^a-z0-9_]+', '', text.lower().replace(' ', '_'))


def enviar_em_partes(texto, limite=2000):
    """
    Divide texto em partes menores que o limite do Discord.
    
    Args:
        texto: Texto a ser dividido
        limite: Tamanho máximo de cada parte (padrão: 2000 caracteres)
    
    Returns:
        list: Lista de strings, cada uma menor que o limite
    
    Exemplo:
        >>> texto_longo = "..." * 5000
        >>> partes = enviar_em_partes(texto_longo)
        >>> len(partes)
        3
    """
    partes = []
    while len(texto) > limite:
        # Tenta quebrar em uma quebra de linha
        ponto_corte = texto.rfind('\n', 0, limite)
        if ponto_corte == -1:
            ponto_corte = limite
        partes.append(texto[:ponto_corte])
        texto = texto[ponto_corte:].lstrip()
    
    # Adiciona o resto se houver
    if texto:
        partes.append(texto)
    
    return partes