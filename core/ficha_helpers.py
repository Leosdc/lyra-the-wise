# core/ficha_helpers.py
"""Funções auxiliares para o sistema de fichas estruturadas."""

import os
import json
import re
from typing import Optional, Tuple, Dict, Any


DATA_DIR = os.path.join(os.getcwd(), "bot_data")
FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")


def salvar_fichas_agora():
    """SALVA FICHAS IMEDIATAMENTE no arquivo JSON com encoding correto."""
    from config import fichas_personagens
    
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Força encoding UTF-8 explicitamente
        with open(FICHAS_PATH, "w", encoding="utf-8") as f:
            json.dump(fichas_personagens, f, ensure_ascii=False, indent=2)
        
        print(f"💾 FICHAS SALVAS! Total: {len(fichas_personagens)}")
        return True
    except Exception as e:
        print(f"❌ ERRO ao salvar fichas: {e}")
        import traceback
        traceback.print_exc()
        return False


def encontrar_ficha(user_id: int, nome: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """Busca ficha do usuário. Prioriza match exato, depois busca parcial."""
    from config import fichas_personagens
    
    nome_lower = nome.lower().strip()
    
    # 1ª tentativa: Match EXATO (ignora case)
    for k, v in fichas_personagens.items():
        if v.get("autor") == user_id:
            if v.get("nome", "").lower().strip() == nome_lower:
                return k, v
    
    # 2ª tentativa: Match parcial
    nome_proc = re.sub(r'[^a-z0-9_]+', '', nome_lower)
    for k, v in fichas_personagens.items():
        if v.get("autor") == user_id:
            nome_limpo = re.sub(r'[^a-z0-9_]+', '', v.get("nome", "").lower())
            if nome_proc in nome_limpo or nome_limpo in nome_proc:
                return k, v
    
    return None, None


def get_estrutura_ficha(sistema: str) -> Dict[str, Any]:
    """Retorna a estrutura de ficha apropriada para o sistema."""
    from sistemas_rpg import ESTRUTURAS_FICHAS
    
    # Template genérico para sistemas não mapeados
    ESTRUTURA_GENERICA = {
        "secoes": ["basico", "atributos", "recursos", "combate", "equipamento", "historia"],
        "campos": {
            "basico": ["Nome", "Raça/Ancestralidade", "Classe/Arquétipo", "Nível", "Conceito"],
            "atributos": ["Atributos Principais"],
            "recursos": ["Pontos de Vida", "Recursos Especiais"],
            "combate": ["Defesa", "Ataques", "Iniciativa"],
            "equipamento": ["Armas", "Armadura", "Itens", "Dinheiro"],
            "historia": ["Personalidade", "História", "Motivações"]
        }
    }
    
    return ESTRUTURAS_FICHAS.get(sistema, ESTRUTURA_GENERICA)