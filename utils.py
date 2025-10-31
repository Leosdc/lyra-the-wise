# utils.py
"""
Módulo de utilidades - REFATORADO
Agora apenas re-exporta funções dos submódulos para manter compatibilidade.
"""

# Importa tudo dos módulos especializados
from core.data_manager import (
    carregar_json,
    salvar_json,
    carregar_dados,
    salvar_dados,
    auto_save,
    DATA_DIR,
    FICHAS_PATH,
    SESSOES_PATH
)

from core.groq_client import (
    chamar_groq,
    get_system_prompt,
    LYRA_IDENTITY,
    groq_client
)

from core.text_utils import (
    key_from_name,
    enviar_em_partes
)

# Re-exporta tudo para manter compatibilidade com código existente
__all__ = [
    # Data Manager
    'carregar_json',
    'salvar_json',
    'carregar_dados',
    'salvar_dados',
    'auto_save',
    'DATA_DIR',
    'FICHAS_PATH',
    'SESSOES_PATH',
    
    # Groq Client
    'chamar_groq',
    'get_system_prompt',
    'LYRA_IDENTITY',
    'groq_client',
    
    # Text Utils
    'key_from_name',
    'enviar_em_partes'
]

print("✅ utils.py carregado (módulos: data_manager, groq_client, text_utils)")