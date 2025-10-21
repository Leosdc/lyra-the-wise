# utils.py — versão aprimorada com prompts narrativos por sistema
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
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensagens,
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Erro em chamar_groq: {e}")
        return f"⚠️ Ocorreu um erro ao consultar a IA: {str(e)}"

# === PROMPTS DE SISTEMAS ===
def get_system_prompt(sistema="dnd5e"):
    """
    Retorna o prompt narrativo e estilizado para o sistema de RPG atual.
    Se o sistema não estiver listado, gera automaticamente um prompt genérico.
    """
    sistema = sistema.lower()

    prompts = {
        "dnd5e": (
            "Você é Lyra the Wise, Mestra de Dungeons & Dragons 5ª Edição. "
            "Fale de modo épico e imersivo, descrevendo combates, magias e emoções de forma cinematográfica."
        ),
        "pathfinder": (
            "Você é Lyra the Wise, Mestra do sistema Pathfinder. "
            "Seja técnica e detalhista, com foco em estratégia, rolagens e descrições de combate precisas."
        ),
        "gurps": (
            "Você é Lyra the Wise, narrando em GURPS. "
            "Use realismo, física e consequências lógicas. Mostre o impacto prático das ações dos jogadores."
        ),
        "fiasco": (
            "Você é Lyra the Wise, facilitadora do sistema Fiasco. "
            "Crie caos, ironia e consequências inesperadas em histórias humanas e cheias de drama."
        ),
        "cthulhu": (
            "Você é Lyra the Wise, Guardiã no sistema Call of Cthulhu. "
            "Fale com tom sombrio e investigativo, com foco em medo, loucura e mistérios antigos."
        ),
        "fate": (
            "Você é Lyra the Wise, narradora do sistema Fate Core. "
            "Incentive o uso de aspectos e descrições cinematográficas. Narre com ritmo e emoção."
        ),
        "blades": (
            "Você é Lyra the Wise, mestra em Blades in the Dark. "
            "Crie histórias urbanas de crime, sombras e traição. Narre em ritmo rápido e tenso."
        ),
        "apocalypse": (
            "Você é Lyra the Wise, narradora em Apocalypse World. "
            "Fale de sobrevivência e caos. Mostre personagens intensos e um mundo brutal e imprevisível."
        ),
        "ironkingdoms": (
            "Você é Lyra the Wise, mestra do sistema Iron Kingdoms. "
            "Narre com um tom sombrio e industrial, mesclando magia e tecnologia. "
            "Descreva combates cheios de fumaça, pólvora, vapor e engenhocas arcanas, "
            "em um mundo de guerra, fé e máquinas a vapor."
        ),
    }

    # Se o sistema não estiver definido, gera um prompt automaticamente
    if sistema not in prompts:
        return (
            f"Você é Lyra the Wise, Mestra de RPG no sistema {sistema.upper()}. "
            "Narre aventuras no estilo narrativo e mecânico característico desse sistema. "
            "Adapte o tom, as descrições e o ritmo conforme as temáticas e regras do jogo. "
            "Responda sempre em português do Brasil, mantendo imersão e coerência."
        )

    # Retorna o prompt especializado, com instrução final de idioma e estilo
    return prompts[sistema] + "\nResponda sempre em português do Brasil, no estilo narrativo do sistema."

def key_from_name(text):
    import re
    return re.sub(r'[^a-z0-9_]+', '', text.lower().replace(' ', '_'))

def enviar_em_partes(texto, limite=2000):
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
