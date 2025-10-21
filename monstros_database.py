# monstros_database.py — Banco de dados de monstros para múltiplos sistemas
"""
Estrutura de cada monstro:
{
    "nome": str,
    "sistema": str,
    "tipo": str (morto-vivo, besta, humanoide, etc),
    "nd": str/int (nível de desafio),
    "tamanho": str,
    "descricao": str,
    "stats": dict (atributos do sistema),
    "habilidades": list,
    "ataques": list,
    "pv": str,
    "ca": str (classe de armadura),
    "especial": str (habilidades únicas)
}
"""

# ==================== D&D 5E ====================
MONSTROS_DND5E = {
    "goblin": {
        "nome": "Goblin",
        "sistema": "dnd5e",
        "tipo": "Humanoide (goblinóide)",
        "nd": "1/4",
        "tamanho": "Pequeno",
        "descricao": "Criatura astuta e covarde que vive em bandos, atacando viajantes desavisados.",
        "stats": {
            "FOR": 8, "DES": 14, "CON": 10,
            "INT": 10, "SAB": 8, "CAR": 8
        },
        "pv": "7 (2d6)",
        "ca": "15 (armadura de couro, escudo)",
        "deslocamento": "9m",
        "ataques": [
            "Cimitarra: +4 para acertar, 1d6+2 cortante",
            "Arco curto: +4 para acertar, alcance 24/96m, 1d6+2 perfurante"
        ],
        "habilidades": [
            "Fuga Ágil: Pode usar ação de Desengajar ou Esconder como ação bônus em cada turno",
            "Visão no Escuro: 18m"
        ],
        "especial": "Covarde quando sozinho, mas perigoso em grupo"
    },
    
    "orc": {
        "nome": "Orc",
        "sistema": "dnd5e",
        "tipo": "Humanoide (orc)",
        "nd": "1/2",
        "tamanho": "Médio",
        "descricao": "Guerreiro brutal e selvagem, guiado por fúria e honra tribal.",
        "stats": {
            "FOR": 16, "DES": 12, "CON": 16,
            "INT": 7, "SAB": 11, "CAR": 10
        },
        "pv": "15 (2d8+6)",
        "ca": "13 (armadura de couro)",
        "deslocamento": "9m",
        "ataques": [
            "Machado Grande: +5 para acertar, 1d12+3 cortante",
            "Azagaia: +5 para acertar, corpo a corpo ou alcance 9/36m, 1d6+3 perfurante"
        ],
        "habilidades": [
            "Agressivo: Pode usar ação bônus para mover-se até seu deslocamento em direção a um inimigo hostil visível",
            "Visão no Escuro: 18m"
        ],
        "especial": "Agressividade Furiosa (bonus action dash para inimigos)"
    },
    
    "dragao_vermelho_adulto": {
        "nome": "Dragão Vermelho Adulto",
        "sistema": "dnd5e",
        "tipo": "Dragão",
        "nd": "17",
        "tamanho": "Enorme",
        "descricao": "Predador supremo, arrogante e ganancioso, mestre do fogo e terror dos céus.",
        "stats": {
            "FOR": 27, "DES": 10, "CON": 25,
            "INT": 16, "SAB": 13, "CAR": 21
        },
        "pv": "256 (19d12+133)",
        "ca": "19 (armadura natural)",
        "deslocamento": "12m, voo 24m",
        "ataques": [
            "Mordida: +14 para acertar, 2d10+8 perfurante + 2d6 fogo",
            "Garra: +14 para acertar, 2d6+8 cortante",
            "Cauda: +14 para acertar, 2d8+8 concussão"
        ],
        "habilidades": [
            "Sopro de Fogo (Recarga 5-6): cone de 18m, CD 21 DES, 63 (18d6) dano de fogo",
            "Presença Assustadora: CD 19 SAB ou amedrontado por 1 minuto",
            "Resistência Lendária (3/dia): Pode escolher ter sucesso em um teste de resistência",
            "Ações Lendárias (3): Detectar, Ataque de Cauda, Ataque com Asa (custa 2)"
        ],
        "especial": "Imunidade a fogo, visão às cegas 18m, visão no escuro 36m"
    },
    
    "beholder": {
        "nome": "Beholder (Observador)",
        "sistema": "dnd5e",
        "tipo": "Aberração",
        "nd": "13",
        "tamanho": "Grande",
        "descricao": "Aberração paranóica e megalomaníaca com olho central anti-magia e tentáculos oculares mortais.",
        "stats": {
            "FOR": 10, "DES": 14, "CON": 18,
            "INT": 17, "SAB": 15, "CAR": 17
        },
        "pv": "180 (19d10+76)",
        "ca": "18 (armadura natural)",
        "deslocamento": "0m, voo 6m (pairar)",
        "ataques": [
            "Mordida: +5 para acertar, 4d6 perfurante"
        ],
        "habilidades": [
            "Cone Anti-Magia: cone de 45m, magias e efeitos mágicos são suprimidos",
            "Raios Oculares (10 tipos): Raio de Charme, Raio Paralisante, Raio do Medo, Raio de Lentidão, Raio Desintegrador, Raio da Morte, Raio Petrificante, Raio de Telecinese, Raio do Sono, Raio Enfraquecedor"
        ],
        "especial": "Cada tentáculo ocular dispara um tipo diferente de raio a cada turno"
    },
    
    "lich": {
        "nome": "Lich",
        "sistema": "dnd5e",
        "tipo": "Morto-vivo",
        "nd": "21",
        "tamanho": "Médio",
        "descricao": "Arquimago morto-vivo de poder incalculável, que trocou a vida pela imortalidade através de magia negra.",
        "stats": {
            "FOR": 11, "DES": 16, "CON": 16,
            "INT": 20, "SAB": 14, "CAR": 16
        },
        "pv": "135 (18d8+54)",
        "ca": "17 (armadura natural)",
        "deslocamento": "9m",
        "ataques": [
            "Toque Paralisante: +12 para acertar, 3d6 necrótico + CD 18 CON ou paralisado"
        ],
        "habilidades": [
            "Conjuração: 9º nível, CD 20, +12 para acertar",
            "Truques: Raio de Gelo, Mãos Mágicas, Mago",
            "1º nível (4): Detectar Magia, Mísseis Mágicos, Escudo, Passos das Brumas",
            "2º nível (3): Cegueira/Surdez, Imagem Espelhada, Arma Mágica",
            "Resistência Lendária (3/dia)",
            "Ações Lendárias (3): Truque, Toque Paralisante, Olhar Assustador, Perturbação da Vida"
        ],
        "especial": "Filatério: só pode ser destruído permanentemente se seu filatério for destruído"
    }
}

# ==================== CALL OF CTHULHU ====================
MONSTROS_CTHULHU = {
    "profundo": {
        "nome": "Profundo (Deep One)",
        "sistema": "cthulhu",
        "tipo": "Criatura dos Mares",
        "descricao": "Humanóide anfíbio que serve aos Grandes Antigos, vive em cidades submersas.",
        "stats": {
            "FOR": 85, "CON": 70, "TAM": 70,
            "DES": 60, "INT": 50, "POD": 50
        },
        "pv": "14",
        "dano_bonus": "+1d4",
        "armadura": "2 pontos (pele escamosa)",
        "ataques": [
            "Garra: 30%, 1d6+DB",
            "Lança: 25%, 1d8+DB"
        ],
        "habilidades": [
            "Nadar: 80%",
            "Respirar debaixo d'água",
            "Visão no escuro"
        ],
        "especial": "Não morre de velhice, apenas por violência. Perda de sanidade: 0/1d6"
    },
    
    "shoggoth": {
        "nome": "Shoggoth",
        "sistema": "cthulhu",
        "tipo": "Aberração Primordial",
        "descricao": "Massa protoplasmática gigante criada pelos Antigos como servos. Pura anarquia biológica.",
        "stats": {
            "FOR": 260, "CON": 225, "TAM": 360,
            "DES": 40, "INT": 40, "POD": 100
        },
        "pv": "59",
        "dano_bonus": "+6d6",
        "armadura": "Nenhuma, mas armas convencionais causam dano mínimo",
        "ataques": [
            "Esmagar: 80%, 4d6+DB (engolfa vítima)",
            "Tentáculos: 40%, 2d6+DB por tentáculo"
        ],
        "habilidades": [
            "Regenera 2 PV por turno",
            "Pode criar olhos, bocas e tentáculos à vontade",
            "Imune a venenos e doenças"
        ],
        "especial": "Encontrar um causa 1d6/1d20 de perda de sanidade. Grito ensurdecedor de 'Tekeli-li!'"
    },
    
    "byakhee": {
        "nome": "Byakhee",
        "sistema": "cthulhu",
        "tipo": "Servo de Hastur",
        "descricao": "Monstro alado do vácuo, montaria dos cultistas para viagens interestelares.",
        "stats": {
            "FOR": 75, "CON": 60, "TAM": 100,
            "DES": 70, "INT": 50, "POD": 55
        },
        "pv": "16",
        "dano_bonus": "+1d6",
        "armadura": "2 pontos (exoesqueleto)",
        "ataques": [
            "Garra: 35%, 1d6+DB",
            "Ferrão: 25%, 1d4+veneno (POT 14)"
        ],
        "habilidades": [
            "Vôo interplanetário",
            "Pode carregar um humano através do espaço",
            "Visão dimensional"
        ],
        "especial": "Perda de sanidade: 1/1d6. Podem ser invocados por cultistas de Hastur"
    },
    
    "ghoul": {
        "nome": "Ghoul (Carniçal)",
        "sistema": "cthulhu",
        "tipo": "Morto-vivo/Necrófago",
        "descricao": "Ex-humano transformado pelo consumo constante de carne morta. Vive em cemitérios e catacumbas.",
        "stats": {
            "FOR": 65, "CON": 60, "TAM": 60,
            "DES": 65, "INT": 60, "POD": 50
        },
        "pv": "12",
        "dano_bonus": "+1d4",
        "armadura": "Nenhuma",
        "ataques": [
            "Mordida: 30%, 1d6+DB + infecção",
            "Garra: 30%, 1d6+DB"
        ],
        "habilidades": [
            "Escavar: 50%",
            "Esconder-se: 60%",
            "Rastrear: 65%",
            "Imune a venenos normais"
        ],
        "especial": "Perda de sanidade: 0/1d6. Feridas podem infeccionar (CON vs POT 12)"
    }
}

# ==================== PATHFINDER ====================
MONSTROS_PATHFINDER = {
    "minotauro": {
        "nome": "Minotauro",
        "sistema": "pathfinder",
        "tipo": "Humanoide Monstruoso",
        "nd": "4",
        "tamanho": "Grande",
        "descricao": "Besta com corpo de homem e cabeça de touro, guardião de labirintos.",
        "stats": {
            "FOR": 19, "DES": 10, "CON": 15,
            "INT": 7, "SAB": 10, "CAR": 8
        },
        "pv": "45 (6d10+12)",
        "ca": "14 (-1 tamanho, +5 natural)",
        "bab": "+6",
        "ataques": [
            "Machado Grande: +9 (2d6+6/×3)",
            "Chifrada: +4 (1d6+2)"
        ],
        "habilidades": [
            "Investida Poderosa: Quando faz investida, causa 2d6+6 com chifrada",
            "Sentido Labiríntico: Nunca se perde, +4 em Sobrevivência em masmorras",
            "Rastrear por Cheiro"
        ],
        "especial": "Fúria de batalha: +2 FOR quando ferido gravemente"
    },
    
    "dragao_de_bronze_jovem": {
        "nome": "Dragão de Bronze Jovem",
        "sistema": "pathfinder",
        "tipo": "Dragão (Água)",
        "nd": "9",
        "tamanho": "Grande",
        "descricao": "Dragão nobre e curioso, protetor de navios e portos, adora tempestades.",
        "stats": {
            "FOR": 21, "DES": 10, "CON": 17,
            "INT": 14, "SAB": 15, "CAR": 14
        },
        "pv": "115 (11d12+44)",
        "ca": "22 (-1 tamanho, +13 natural)",
        "bab": "+11",
        "ataques": [
            "Mordida: +16 (2d6+7)",
            "2 Garras: +15 (1d8+5)",
            "2 Asas: +13 (1d6+2)",
            "Cauda: +13 (1d8+7)"
        ],
        "habilidades": [
            "Sopro de Eletricidade: linha de 18m, 6d6 elétrico, Reflexos CD 18 metade",
            "Anfíbio: Respira ar e água",
            "Falar com Animais (aquáticos)",
            "Imunidade: Eletricidade, Sono, Paralisia"
        ],
        "especial": "Pode criar névoa 3x/dia, Resistência à Magia 20"
    }
}

# ==================== VAMPIRE: THE MASQUERADE ====================
MONSTROS_VAMPIRE = {
    "lupino": {
        "nome": "Lobisomem Garou",
        "sistema": "vampire",
        "tipo": "Lupino (Garou)",
        "descricao": "Guerreiro metamorfo de Gaia, inimigo mortal dos vampiros. Extremamente perigoso.",
        "stats": {
            "Físicos": "FOR 5, DES 4, VIG 5 (Crinos)",
            "Sociais": "CAR 2, MAN 2, COM 1",
            "Mentais": "PER 3, INT 2, RAC 3"
        },
        "pv": "Vitalidade: 12 níveis (Crinos)",
        "armadura": "Pele grossa (absorve 2 dados de dano)",
        "ataques": [
            "Garras: FOR+2, Dano Agravado",
            "Mordida: FOR+1, Dano Agravado"
        ],
        "habilidades": [
            "Fúria: 7 pontos, múltiplas ações",
            "Regeneração: 1 nível de vitalidade por turno",
            "Sentidos Aguçados: -2 dificuldade em Percepção",
            "Formas: Humano, Glabro, Crinos, Hispo, Lobo"
        ],
        "especial": "PERIGO EXTREMO: Pode destruir vampiros permanentemente com dano agravado. Imune a Dominação."
    },
    
    "tzimisce_voivoda": {
        "nome": "Voivoda Tzimisce",
        "sistema": "vampire",
        "tipo": "Vampiro Ancião",
        "descricao": "Mestre da Vicissitude, senhor feudal de terras amaldiçoadas. Aparência grotesca e poder imenso.",
        "stats": {
            "Físicos": "FOR 5, DES 4, VIG 5",
            "Sociais": "CAR 4, MAN 5, COM 2",
            "Mentais": "PER 4, INT 5, RAC 4"
        },
        "pv": "Vitalidade: 10 níveis + Fortitude 5",
        "disciplinas": {
            "Animalismo": 5,
            "Auspícios": 4,
            "Vicissitude": 6,
            "Dominação": 4,
            "Fortitude": 5
        },
        "ataques": [
            "Garras Ósseas: FOR+2, Dano Agravado",
            "Tentáculos de Carne: Agarrar à distância"
        ],
        "habilidades": [
            "Moldar Carne e Ossos: Vicissitude 6",
            "Horrid Form: Transformação monstruosa (+3 Físicos)",
            "Terraconexão: Conhece tudo em suas terras",
            "Zulo: Forma de guerra grotesca"
        ],
        "especial": "Geração 7, Sangue Potente. Precisa dormir na terra natal."
    }
}

# ==================== SHADOWRUN ====================
MONSTROS_SHADOWRUN = {
    "drake": {
        "nome": "Drake",
        "sistema": "shadowrun",
        "tipo": "Metamorfo Dracônico",
        "descricao": "Dragão em forma humana. Agente corporativo ou shadowrunner com poderes dracônicos.",
        "stats": {
            "Corpo": 6, "Agilidade": 5, "Reação": 5,
            "Força": 5, "Carisma": 5, "Intuição": 4,
            "Lógica": 5, "Força de Vontade": 6,
            "Essência": 6, "Magia": 5
        },
        "iniciativa": "9 + 2d6",
        "armadura": "12 (escamas naturais em forma dracônica)",
        "ataques": [
            "Mordida: 8P, -2 PA (forma dracônica)",
            "Garras: 7P, -1 PA",
            "Sopro Elemental: 10P, área, tipo varia"
        ],
        "habilidades": [
            "Metamorfose: Humano ↔ Drake",
            "Sopro Dracônico (tipo baseado em metavariante)",
            "Resistência à Magia: 5 dados",
            "Poderes: Resistência Imunológica, Sentidos Aprimorados"
        ],
        "especial": "Dual natured, pode ver o astral. Geralmente tem conexões corporativas."
    },
    
    "inseto_espírito": {
        "nome": "Espírito Inseto (Abelha Rainha)",
        "sistema": "shadowrun",
        "tipo": "Horror Astral",
        "descricao": "Espírito invasor que toma corpo de humano. Hive mind alienígena e terrível.",
        "stats": {
            "Corpo": 8, "Agilidade": 4, "Reação": 5,
            "Força": 6, "Carisma": 3, "Intuição": 4,
            "Lógica": 3, "Força de Vontade": 7,
            "Essência": 6, "Magia": 6
        },
        "iniciativa": "9 + 2d6",
        "armadura": "14 (quitina)",
        "ataques": [
            "Mandíbulas: 9P, -2 PA",
            "Ferrão: 7P + Toxina (8P)",
            "Enxame: Invoca insetos normais"
        ],
        "habilidades": [
            "Dual Natured",
            "Mente Coletiva: +2 dados por aliado inseto próximo",
            "Manifestar: Aparecer no físico",
            "Poderes: Medo, Confusão, Controle Mental"
        ],
        "especial": "EXTREMAMENTE PERIGOSO. Pode gerar nova colônia. Bug City, nunca esqueça."
    }
}

# ==================== FUNÇÕES AUXILIARES ====================

def buscar_monstro(nome, sistema=None):
    """Busca um monstro por nome, opcionalmente filtrando por sistema."""
    nome_lower = nome.lower()
    
    # Dicionário de todos os monstros por sistema
    bases = {
        "dnd5e": MONSTROS_DND5E,
        "pathfinder": MONSTROS_PATHFINDER,
        "cthulhu": MONSTROS_CTHULHU,
        "vampire": MONSTROS_VAMPIRE,
        "shadowrun": MONSTROS_SHADOWRUN
    }
    
    # Se sistema específico
    if sistema and sistema in bases:
        for key, monstro in bases[sistema].items():
            if nome_lower in key or nome_lower in monstro["nome"].lower():
                return monstro
        return None
    
    # Busca em todos os sistemas
    for sistema_key, monstros in bases.items():
        for key, monstro in monstros.items():
            if nome_lower in key or nome_lower in monstro["nome"].lower():
                return monstro
    
    return None


def listar_monstros_por_sistema(sistema):
    """Lista todos os monstros disponíveis para um sistema."""
    bases = {
        "dnd5e": MONSTROS_DND5E,
        "pathfinder": MONSTROS_PATHFINDER,
        "cthulhu": MONSTROS_CTHULHU,
        "vampire": MONSTROS_VAMPIRE,
        "shadowrun": MONSTROS_SHADOWRUN
    }
    
    if sistema not in bases:
        return []
    
    return [m["nome"] for m in bases[sistema].values()]


def formatar_monstro(monstro):
    """Formata os dados do monstro para exibição."""
    if not monstro:
        return "Monstro não encontrado."
    
    texto = f"**{monstro['nome']}**\n"
    texto += f"*{monstro.get('tipo', 'Desconhecido')}*\n\n"
    texto += f"{monstro['descricao']}\n\n"
    
    # ND/Desafio
    if 'nd' in monstro:
        texto += f"**ND:** {monstro['nd']}\n"
    if 'tamanho' in monstro:
        texto += f"**Tamanho:** {monstro['tamanho']}\n"
    
    # Stats
    if 'stats' in monstro:
        stats_texto = ", ".join([f"{k}: {v}" for k, v in monstro['stats'].items()])
        texto += f"**Atributos:** {stats_texto}\n"
    
    # PV e Defesas
    if 'pv' in monstro:
        texto += f"**PV:** {monstro['pv']}\n"
    if 'ca' in monstro:
        texto += f"**CA:** {monstro['ca']}\n"
    if 'armadura' in monstro:
        texto += f"**Armadura:** {monstro['armadura']}\n"
    
    # Ataques
    if 'ataques' in monstro and monstro['ataques']:
        texto += f"\n**Ataques:**\n"
        for ataque in monstro['ataques']:
            texto += f"• {ataque}\n"
    
    # Habilidades
    if 'habilidades' in monstro and monstro['habilidades']:
        texto += f"\n**Habilidades:**\n"
        for hab in monstro['habilidades']:
            texto += f"• {hab}\n"
    
    # Especial
    if 'especial' in monstro:
        texto += f"\n**Especial:** {monstro['especial']}\n"
    
    return texto
