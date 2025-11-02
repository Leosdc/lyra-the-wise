# validate_fichas.py
from utils import carregar_dados

fichas = carregar_dados()

for nome, ficha in fichas.items():
    # Verifica inventário
    inv = ficha.get("progressao", {}).get("inventario")
    assert isinstance(inv, list), f"{nome}: inventário não é lista"
    
    # Verifica XP
    assert "xp_atual" in ficha.get("progressao", {}), f"{nome}: falta XP"
    
    # Verifica HP
    assert "HP Atual" in ficha.get("combate", {}), f"{nome}: falta HP Atual"
    
    print(f"✅ {nome} — estrutura válida")