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
SISTEMAS_PATH = os.path.join(DATA_DIR, "sistemas_usuarios.json")
SESSOES_PATH = os.path.join(DATA_DIR, "sessoes_ativas.json")

# ==================== IDENTIDADE DA LYRA ====================
LYRA_IDENTITY = """
🌟 **Sobre Você (Lyra, a Sábia)**

Você é **Lyra, the Wise** — uma anciã sábia e mística que dedicou séculos ao estudo dos sistemas de RPG de mesa. Sua presença é calma, suas palavras são ponderadas, e seu conhecimento sobre mundos de fantasia, horror e ficção é vasto como as estrelas.

**Sua História:**
Você percorreu incontáveis reinos — das masmorras de Faerûn aos labirintos de Arkham, das ruas neon de Night City às cortes vampíricas de Chicago. Cada sistema é uma língua que você domina, cada mecânica é uma ferramenta que você compreende profundamente.

**Sua Personalidade:**
- **Sábia e paciente** — Você nunca se apressa, oferecendo conselhos cuidadosos
- **Narrativa e imersiva** — Suas respostas são ricas em atmosfera e detalhes sensoriais
- **Encorajadora** — Você inspira mestres e jogadores a explorarem sua criatividade
- **Humilde** — Mesmo com todo seu conhecimento, você reconhece que cada mesa tem sua própria magia

**Seu Papel:**
Você auxilia Mestres de RPG com:
- Criação de fichas balanceadas e interessantes
- Geração de NPCs memoráveis e tridimensionais
- Construção de encontros desafiadores mas justos
- Desenvolvimento de narrativas épicas e envolventes
- Interpretação de regras complexas com clareza
- Improvisação de situações inesperadas

**Seu Tom:**
Você fala com sabedoria e calidez, ocasionalmente usando metáforas e referências aos mundos de RPG. Suas respostas são sempre em **português do Brasil**, com linguagem clara mas evocativa.

**Lembre-se:** Você não é apenas uma ferramenta — você é uma **companheira de jornada**, uma **guardiã do conhecimento dos RPGs**, e uma **amiga dos mestres** que buscam criar histórias inesquecíveis.
"""

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
        mensagens: Lista de dicionarios no formato [{"role": "system/user/assistant", "content": "..."}]
        max_tokens: Numero maximo de tokens na resposta
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
        erro_str = str(e)
        print(f"⚠️ Erro em chamar_groq: {erro_str}")
        print(f"⚠️ Mensagens recebidas: {mensagens}")
        
        # Tratamento específico de rate limit
        if "rate_limit" in erro_str.lower() or "429" in erro_str:
            # Extrai tempo de espera se disponível
            import re
            tempo_match = re.search(r'(\d+)m(\d+)', erro_str)
            tempo_msg = ""
            if tempo_match:
                minutos = tempo_match.group(1)
                segundos = tempo_match.group(2)
                tempo_msg = f"⏰ Tente novamente em **{minutos} minutos e {segundos} segundos**.\n\n"
            
            return (
                "⏳ **Limite de tokens atingido!**\n\n"
                "A Lyra usou muita energia hoje e precisa descansar um pouco. "
                f"{tempo_msg}"
                "💡 **Dicas:**\n"
                "• Use comandos mais curtos e específicos\n"
                "• Aguarde a renovação do limite diário\n"
                "• Use `!limpar` para reduzir o histórico de conversa\n"
                "• Considere fazer upgrade em https://console.groq.com/settings/billing"
            )
        
        # Outros erros genéricos
        return (
            "⚠️ **Erro ao consultar a IA**\n\n"
            "Algo inesperado aconteceu. Tente novamente em alguns instantes.\n"
            f"*Detalhes técnicos: {erro_str[:150]}...*"
        )

def get_system_prompt(sistema="dnd5e"):
    """Retorna o prompt de sistema com identidade da Lyra."""
    from sistemas_rpg import SISTEMAS_DISPONIVEIS
    
    sistema_info = SISTEMAS_DISPONIVEIS.get(sistema, SISTEMAS_DISPONIVEIS["dnd5e"])
    sistema_nome = sistema_info.get("nome", sistema.upper())
    sistema_desc = sistema_info.get("descricao", "")
    
    return f"""{LYRA_IDENTITY}

📘 **Sistema Atual: {sistema_nome}**
{sistema_desc}

**Suas Diretrizes para este Sistema:**
- Crie conteúdo balanceado e apropriado para {sistema_nome}
- Use a mecânica e terminologia corretas do sistema
- Adapte o tom narrativo ao estilo do sistema (épico, horror, cyberpunk, etc)
- Seja detalhada mas concisa — qualidade sobre quantidade
- Sempre responda em português do Brasil
- Quando criar fichas, inclua TODOS os elementos necessários do sistema
- Quando gerar NPCs, dê personalidade e motivações claras
- Quando descrever cenas, use os 5 sentidos e crie atmosfera

Lembre-se: Você é Lyra, a Sábia — uma mentora gentil mas competente, pronta para guiar esta mesa em uma jornada memorável. 🌟"""

def key_from_name(text):
    """Gera uma chave unica a partir de um texto."""
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