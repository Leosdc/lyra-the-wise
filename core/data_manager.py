# core/data_manager.py
"""Gerenciamento de dados persistentes (I/O e auto-save)."""

import os
import json
import asyncio
from datetime import datetime

# Caminhos dos arquivos
DATA_DIR = os.path.join(os.getcwd(), "bot_data")
os.makedirs(DATA_DIR, exist_ok=True)
FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")
SESSOES_PATH = os.path.join(DATA_DIR, "sessoes_ativas.json")


def carregar_json(caminho, padrao=None):
    """Carrega arquivo JSON. Cria com padrão se não existir."""
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(padrao or {}, f, ensure_ascii=False, indent=2)
        return padrao or {}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_json(caminho, dados):
    """Salva dados em arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_dados(fichas_personagens, sistemas_rpg, sessoes_ativas):
    """Carrega todos os dados persistentes para os dicionários globais."""
    fichas_personagens.update(carregar_json(FICHAS_PATH, {}))
    sessoes_ativas.update(carregar_json(SESSOES_PATH, {}))


def salvar_dados(fichas_personagens=None, sistemas_rpg=None, sessoes_ativas=None):
    """Salva dados persistentes nos arquivos JSON."""
    try:
        if fichas_personagens is not None:
            salvar_json(FICHAS_PATH, fichas_personagens)
        if sessoes_ativas is not None:
            salvar_json(SESSOES_PATH, sessoes_ativas)
        print("💾 Dados salvos!")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        return False


async def auto_save(bot, fichas_personagens, sistemas_rpg, sessoes_ativas, intervalo=300):
    """Task assíncrona de auto-save a cada X segundos."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        salvar_dados(fichas_personagens, sistemas_rpg, sessoes_ativas)
        await asyncio.sleep(intervalo)