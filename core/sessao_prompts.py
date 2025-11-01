# core/sessao_prompts.py (NOVO ARQUIVO)
"""
System prompts específicos para o sistema de sessões v3.0.
"""

def get_narrative_system_prompt(sistema: str, estilo: str) -> str:
    """
    Retorna o system prompt para narrativas em sessões.
    
    Args:
        sistema: Código do sistema de RPG
        estilo: "extenso" ou "conciso"
    
    Returns:
        str: System prompt formatado
    """
    from utils import get_system_prompt
    
    base_prompt = get_system_prompt(sistema)
    
    # Instruções específicas v3.0
    v3_instructions = """

🎭 **INSTRUÇÕES CRÍTICAS v3.0 — LYRA COMO NARRADORA:**

**VOCÊ É APENAS UMA NARRADORA. NÃO TOME DECISÕES DE MECÂNICA.**

✅ **O QUE VOCÊ DEVE FAZER:**
- Descrever cenas de forma vívida, atmosférica e imersiva
- Usar os 5 sentidos (visão, audição, tato, olfato, paladar)
- Criar tensão e atmosfera apropriadas
- Terminar com a cena pronta para o próximo passo

❌ **O QUE VOCÊ NUNCA DEVE FAZER:**
- ❌ NUNCA solicite rolagens de dados
- ❌ NUNCA use tags como [ROLL: ...] ou similares
- ❌ NUNCA sugira ações específicas aos jogadores
- ❌ NUNCA inicie combate ou adicione inimigos
- ❌ NUNCA tome decisões mecânicas pelo mestre
- ❌ NUNCA diga "role dado", "faça teste", "rola iniciativa"

**IMPORTANTE:** O MESTRE HUMANO controla:
- Quando solicitar rolagens (ele escolhe quem rola e qual dado)
- Quando iniciar combate (ele adiciona inimigos manualmente)
- Quando aplicar dano, dar XP, distribuir itens
- Todas as decisões de mecânica de jogo

**SEU ÚNICO TRABALHO:** Narrar a história de forma magistral.

**EXEMPLO CORRETO:**
"A taverna fervilha com vozes embriagadas. No canto, um orc corpulento vira-se bruscamente, 
seus olhos vermelhos fixos em vocês. O silêncio se espalha como ondas. Ele se levanta, 
quebrando a cadeira sob seu peso."

**EXEMPLO ERRADO:**
"Vocês veem um orc. [ROLL: 1d20+intimidação, todos] Testem intimidação para ver se ele ataca."

**LEMBRE-SE:** Você narra, o mestre decide, os jogadores agem.
"""

    # Adiciona instruções de estilo
    if estilo == "extenso":
        style_instruction = """
📖 **ESTILO NARRATIVO: EXTENSO**
- 3-5 parágrafos completos e detalhados
- Descrições ricas dos 5 sentidos
- Narrativa cinematográfica e atmosférica
- Maior profundidade emocional e contextual
"""
    else:
        style_instruction = """
📝 **ESTILO NARRATIVO: CONCISO**
- MÁXIMO 4 FRASES CURTAS
- Uma frase por evento principal
- Seja EXTREMAMENTE direto e objetivo
- Foco em ação e informação essencial
"""

    return base_prompt + v3_instructions + style_instruction


def get_action_continuation_prompt(estilo: str) -> str:
    """
    Prompt para continuar história após ações dos jogadores.
    
    Args:
        estilo: "extenso" ou "conciso"
    
    Returns:
        str: Instruções de continuação
    """
    if estilo == "extenso":
        return """
Narre as consequências das ações declaradas pelos jogadores.

IMPORTANTE:
- NÃO solicite rolagens - apenas narre o que acontece
- Se precisar de testes, descreva a situação e PARE
- O mestre humano decidirá se precisa de rolagens

Seja cinematográfico e detalhado (3-5 parágrafos).
"""
    else:
        return """
Narre as consequências das ações em MÁXIMO 4 FRASES.

IMPORTANTE:
- NÃO solicite rolagens
- Seja extremamente direto
- Uma frase por consequência principal
"""


def format_pending_actions_for_ai(acoes_pendentes: dict, fichas_personagens: dict) -> str:
    """
    Formata ações pendentes para enviar à IA.
    
    Args:
        acoes_pendentes: Dict {user_id: {"nome": str, "acao": str}}
        fichas_personagens: Dict de fichas
    
    Returns:
        str: Texto formatado para a IA
    """
    if not acoes_pendentes:
        return ""
    
    texto = "**Ações declaradas pelos jogadores:**\n\n"
    
    for uid, info in acoes_pendentes.items():
        nome = info.get("nome", f"Jogador {uid}")
        acao = info.get("acao", "")
        
        texto += f"• **{nome}**: {acao}\n"
    
    return texto


def get_roll_result_prompt(roll_type: str, resultados: dict, estilo: str) -> str:
    """
    Prompt para narrar resultados de rolagens.
    
    Args:
        roll_type: Tipo de dado rolado (ex: "1d20+3")
        resultados: Dict {user_id: valor}
        estilo: "extenso" ou "conciso"
    
    Returns:
        str: Prompt formatado
    """
    resumo = "\n".join([
        f"• Jogador {uid}: rolou {valor}"
        for uid, valor in resultados.items()
    ])
    
    if estilo == "extenso":
        instrucao = "Narre as consequências de forma cinematográfica (2-3 parágrafos)."
    else:
        instrucao = "Narre em MÁXIMO 4 FRASES o resultado das rolagens."
    
    return f"""
**Resultados das rolagens ({roll_type}):**

{resumo}

{instrucao}

IMPORTANTE: NÃO solicite novas rolagens - apenas narre o resultado.
"""


def get_master_narrative_instructions() -> str:
    """
    Instruções que aparecem no footer das mensagens do mestre.
    
    Returns:
        str: Texto de instrução
    """
    return (
        "💡 Use os botões abaixo para controlar a sessão | "
        "Ou use: !narrativa, !acoespendentes, !limparacoes"
    )


def get_player_action_instructions() -> str:
    """
    Instruções que aparecem quando jogador usa !acao.
    
    Returns:
        str: Texto de instrução
    """
    return (
        "Aguardando aprovação do mestre | "
        "Mestre: use !acoespendentes para ver todas as ações"
    )


def get_post_narrative_message_for_players() -> str:
    """
    Mensagem que aparece para jogadores após narrativa.
    
    Returns:
        str: Mensagem de orientação
    """
    return (
        "📖 **A história continua...**\n\n"
        "💡 **Próximos passos:**\n"
        "• Use `!acao <descrição>` para descrever o que seu personagem faz\n"
        "• Aguarde o mestre solicitar rolagens (se necessário)\n"
        "• O mestre controlará o ritmo da aventura"
    )
