# config.py - VERSÃO CORRIGIDA
import os
import discord
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Discord intents & bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

BOT_PREFIX = "!"
bot = None  # será atribuído em main.py

# Diretórios e arquivos de dados
DATA_DIR = Path("bot_data")
DATA_DIR.mkdir(exist_ok=True)

FICHAS_FILE = DATA_DIR / "fichas_personagens.json"
SISTEMAS_FILE = DATA_DIR / "sistemas_rpg.json"
SESSOES_FILE = DATA_DIR / "sessoes_ativas.json"
SISTEMAS_FILE = DATA_DIR / "sistemas_usuarios.json"

# CORREÇÃO CRÍTICA: Estados compartilhados GLOBAIS
# Estes dicionários são a ÚNICA fonte de verdade para todo o bot
conversation_history = {}  # por canal
sistemas_rpg = {}          # user_id -> sistema
fichas_personagens = {}    # chave -> ficha
sessoes_ativas = {}        # channel_id -> sessão

# Token
DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

print("⚙️ Config carregado - Dicionários globais criados")