#!/usr/bin/env python3
# migrate_to_v3.py
"""
Script de migração de Lyra v2.x para v3.0.
Corrige estruturas de fichas antigas.
"""

import json
import os
from datetime import datetime
from pathlib import Path


# Tabela de XP (D&D 5e)
XP_TABLE = {
    1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
    6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
    11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
    16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
}


def calcular_xp_nivel(nivel: int) -> int:
    """Retorna XP necessário para o próximo nível."""
    return XP_TABLE.get(nivel + 1, 0)


def garantir_estrutura_inventario(ficha: dict) -> dict:
    """Corrige estrutura de inventário."""
    if "progressao" not in ficha:
        ficha["progressao"] = {}
    
    if "inventario" not in ficha["progressao"]:
        ficha["progressao"]["inventario"] = []
    
    # CRÍTICO: Corrige se inventario for string
    if isinstance(ficha["progressao"]["inventario"], str):
        print(f"  ⚠️  Corrigindo inventário (era string)")
        ficha["progressao"]["inventario"] = []
    
    # Garante que é uma lista
    if not isinstance(ficha["progressao"]["inventario"], list):
        print(f"  ⚠️  Inventário inválido (tipo: {type(ficha['progressao']['inventario'])})")
        ficha["progressao"]["inventario"] = []
    
    return ficha


def garantir_estrutura_xp(ficha: dict) -> dict:
    """Adiciona sistema de XP."""
    if "progressao" not in ficha:
        ficha["progressao"] = {}
    
    # XP atual
    if "xp_atual" not in ficha["progressao"]:
        ficha["progressao"]["xp_atual"] = 0
        print(f"  ✅ XP inicializado: 0")
    
    # XP próximo nível
    nivel_str = ficha.get("basico", {}).get("Nível", "1")
    try:
        nivel = int(nivel_str)
    except (ValueError, TypeError):
        nivel = 1
    
    if "xp_proximo_nivel" not in ficha["progressao"]:
        xp_proximo = calcular_xp_nivel(nivel)
        ficha["progressao"]["xp_proximo_nivel"] = xp_proximo
        print(f"  ✅ XP próximo nível: {xp_proximo}")
    
    return ficha


def garantir_estrutura_combate(ficha: dict) -> dict:
    """Garante campos de combate."""
    if "combate" not in ficha:
        ficha["combate"] = {}
    
    # HP Atual
    if "HP Atual" not in ficha["combate"]:
        hp_max = ficha["combate"].get("HP Máximo", 10)
        ficha["combate"]["HP Atual"] = hp_max
        print(f"  ✅ HP Atual definido: {hp_max}")
    
    return ficha


def migrar_ficha(nome: str, ficha: dict) -> tuple[dict, list]:
    """
    Migra uma ficha individual.
    Retorna (ficha_migrada, lista_de_mudancas).
    """
    print(f"\n📋 Migrando: {nome}")
    mudancas = []
    
    # 1. Inventário
    try:
        ficha = garantir_estrutura_inventario(ficha)
        mudancas.append("inventário")
    except Exception as e:
        print(f"  ❌ Erro no inventário: {e}")
    
    # 2. XP
    try:
        ficha = garantir_estrutura_xp(ficha)
        mudancas.append("xp")
    except Exception as e:
        print(f"  ❌ Erro no XP: {e}")
    
    # 3. Combate
    try:
        ficha = garantir_estrutura_combate(ficha)
        mudancas.append("combate")
    except Exception as e:
        print(f"  ❌ Erro no combate: {e}")
    
    # 4. Validação final
    validacoes = []
    
    # Verifica inventário
    if isinstance(ficha.get("progressao", {}).get("inventario"), list):
        validacoes.append("✅ Inventário: lista")
    else:
        validacoes.append("❌ Inventário: inválido")
    
    # Verifica XP
    if "xp_atual" in ficha.get("progressao", {}):
        validacoes.append("✅ XP: configurado")
    else:
        validacoes.append("❌ XP: faltando")
    
    # Verifica HP
    if "HP Atual" in ficha.get("combate", {}):
        validacoes.append("✅ HP: configurado")
    else:
        validacoes.append("❌ HP: faltando")
    
    print(f"  {'  '.join(validacoes)}")
    
    return ficha, mudancas


def criar_backup(caminho_fichas: Path) -> Path:
    """Cria backup antes de migrar."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = caminho_fichas.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    backup_path = backup_dir / f"fichas_backup_{timestamp}.json"
    
    with open(caminho_fichas, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    return backup_path


def main():
    """Executa migração completa."""
    print("=" * 60)
    print("🔄 MIGRAÇÃO LYRA v2.x → v3.0")
    print("=" * 60)
    
    # Caminho das fichas
    caminho_fichas = Path("data/fichas_personagens.json")
    
    if not caminho_fichas.exists():
        print(f"\n❌ Arquivo não encontrado: {caminho_fichas}")
        print("Certifique-se de estar no diretório raiz do projeto.")
        return
    
    # 1. Backup
    print("\n📦 Criando backup...")
    try:
        backup_path = criar_backup(caminho_fichas)
        print(f"✅ Backup criado: {backup_path}")
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        print("Abortando migração por segurança.")
        return
    
    # 2. Carrega fichas
    print("\n📂 Carregando fichas...")
    try:
        with open(caminho_fichas, 'r', encoding='utf-8') as f:
            fichas = json.load(f)
        print(f"✅ {len(fichas)} fichas carregadas")
    except Exception as e:
        print(f"❌ Erro ao carregar fichas: {e}")
        return
    
    # 3. Migra cada ficha
    print("\n🔄 Iniciando migração...")
    fichas_migradas = {}
    estatisticas = {
        "total": len(fichas),
        "sucesso": 0,
        "falhas": 0,
        "mudancas": []
    }
    
    for nome, ficha in fichas.items():
        try:
            ficha_migrada, mudancas = migrar_ficha(nome, ficha)
            fichas_migradas[nome] = ficha_migrada
            estatisticas["sucesso"] += 1
            estatisticas["mudancas"].extend(mudancas)
        except Exception as e:
            print(f"  ❌ ERRO CRÍTICO: {e}")
            fichas_migradas[nome] = ficha  # Mantém original
            estatisticas["falhas"] += 1
    
    # 4. Salva fichas migradas
    print("\n💾 Salvando fichas migradas...")
    try:
        with open(caminho_fichas, 'w', encoding='utf-8') as f:
            json.dump(fichas_migradas, f, indent=2, ensure_ascii=False)
        print(f"✅ Fichas salvas em: {caminho_fichas}")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        print(f"🔄 Restaure o backup: {backup_path}")
        return
    
    # 5. Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE MIGRAÇÃO")
    print("=" * 60)
    print(f"Total de fichas: {estatisticas['total']}")
    print(f"✅ Migradas com sucesso: {estatisticas['sucesso']}")
    print(f"❌ Falhas: {estatisticas['falhas']}")
    
    # Mudanças aplicadas
    from collections import Counter
    mudancas_count = Counter(estatisticas['mudancas'])
    
    print("\n🔧 Mudanças aplicadas:")
    for mudanca, count in mudancas_count.items():
        print(f"  - {mudanca}: {count} fichas")
    
    print("\n✅ Migração concluída!")
    print(f"📦 Backup disponível em: {backup_path}")
    
    # Próximos passos
    print("\n" + "=" * 60)
    print("📋 PRÓXIMOS PASSOS")
    print("=" * 60)
    print("1. Reinicie o bot: python main.py")
    print("2. No Discord, execute: !migrarinventario")
    print("3. Teste os comandos:")
    print("   - !inventario")
    print("   - !addinventario Espada Longa")
    print("   - !xp")
    print("   - !darxp <jogador> 100")
    print("\n💡 Se houver problemas, restaure o backup:")
    print(f"   cp {backup_path} {caminho_fichas}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n\n❌ ERRO CRÍTICO: {e}")
        print("Por favor, reporte este erro no GitHub Issues.")
