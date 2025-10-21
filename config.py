
# config.py
import os
import discord
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Discord intents & bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # útil para permissões em canais privados

BOT_PREFIX = "!"
bot = None  # será atribuído em main.py

# Diretórios e arquivos de dados
DATA_DIR = Path("bot_data")
DATA_DIR.mkdir(exist_ok=True)

FICHAS_FILE = DATA_DIR / "fichas_personagens.json"
SISTEMAS_FILE = DATA_DIR / "sistemas_rpg.json"
SESSOES_FILE = DATA_DIR / "sessoes_ativas.json"

# Estados compartilhados
conversation_history = {}  # por canal
sistemas_rpg = {}          # channel_id -> sistema
fichas_personagens = {}    # chave -> ficha
sessoes_ativas = {}        # channel_id -> sessão

# Token
DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
