import os
import json
import asyncio
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

DATA_DIR = os.path.join(os.getcwd(), "bot_data")
os.makedirs(DATA_DIR, exist_ok=True)
FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")
SISTEMAS_PATH = os.path.join(DATA_DIR, "sistemas_rpg.json")
SESSOES_PATH = os.path.join(DATA_DIR, "sessoes_ativas.json")

def carregar_json(caminho, padrao=None):
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(padrao or {}, f, ensure_ascii=False, indent=2)
        return padrao or {}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_dados(fichas_personagens, sistemas_rpg, sessoes_ativas):
    fichas_personagens.update(carregar_json(FICHAS_PATH, {}))
    sistemas_rpg.update(carregar_json(SISTEMAS_PATH, {}))
    sessoes_ativas.update(carregar_json(SESSOES_PATH, {}))
    print("💾 Dados carregados!")

def salvar_dados(fichas_personagens=None, sistemas_rpg=None, sessoes_ativas=None):
    try:
        if fichas_personagens is not None:
            salvar_json(FICHAS_PATH, fichas_personagens)
        if sistemas_rpg is not None:
            salvar_json(SISTEMAS_PATH, sistemas_rpg)
        if sessoes_ativas is not None:
            salvar_json(SESSOES_PATH, sessoes_ativas)
        print("💾 Dados salvos!")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        return False

async def auto_save(bot, fichas_personagens, sistemas_rpg, sessoes_ativas, intervalo=300):
    await bot.wait_until_ready()
    while not bot.is_closed():
        salvar_dados(fichas_personagens, sistemas_rpg, sessoes_ativas)
        await asyncio.sleep(intervalo)

async def chamar_groq(mensagens, max_tokens=1000):
    """
    Chama a API Groq para gerar respostas.
    
    Args:
        mensagens: Lista de dicionários no formato [{"role": "system/user/assistant", "content": "..."}]
        max_tokens: Número máximo de tokens na resposta
    """
    try:
        # Valida e corrige max_tokens
        if isinstance(max_tokens, list):
            max_tokens = 1000
        elif not isinstance(max_tokens, int):
            max_tokens = int(max_tokens) if str(max_tokens).isdigit() else 1000

        # Valida mensagens
        if not isinstance(mensagens, list):
            print(f"⚠️ Erro: mensagens deve ser uma lista, recebeu {type(mensagens)}")
            return "⚠️ Erro interno: formato de mensagens inválido."

        # Debug: mostra o que está sendo enviado
        print(f"🔍 Enviando para Groq: {len(mensagens)} mensagens")
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensagens,
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Erro em chamar_groq: {e}")
        print(f"⚠️ Mensagens recebidas: {mensagens}")
        return f"⚠️ Ocorreu um erro ao consultar a IA: {str(e)}"

def get_system_prompt(sistema="dnd5e"):
    """Retorna o prompt de sistema para o Groq."""
    return (
        f"Você é um Mestre de RPG especialista no sistema {sistema.upper()}.\n"
        "Crie descrições, NPCs, monstros e fichas de personagem completas e balanceadas.\n"
        "Responda sempre em português do Brasil, com tom narrativo e imersivo."
    )

def key_from_name(text):
    """Gera uma chave única a partir de um texto."""
    import re
    return re.sub(r'[^a-z0-9_]+', '', text.lower().replace(' ', '_'))

def enviar_em_partes(texto, limite=2000):
    """Divide texto em partes menores que o limite do Discord."""
    partes = []
    while len(texto) > limite:
        ponto_corte = texto.rfind('\n', 0, limite)
        if ponto_corte == -1:
            ponto_corte = limite
        partes.append(texto[:ponto_corte])
        texto = texto[ponto_corte:].lstrip()
    if texto:
        partes.append(texto)
    return partes