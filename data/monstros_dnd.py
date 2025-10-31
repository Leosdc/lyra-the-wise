"""
Banco de dados de monstros para sistemas D&D e derivados.
Inclui D&D 5e e Pathfinder.
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
            "Resistência Legendária (3/dia): Pode escolher ter sucesso em um teste de resistência",
            "Ações Legendárias (3): Detectar, Ataque de Cauda, Ataque com Asa (custa 2)"
        ],
        "especial": "Imunidade a fogo, visão às cegas 18m, visão no escuro 36m"
    },
    
    "beholder": {
        "nome": "Beholder (Observador)",
        "sistema": "dnd5e",
        "tipo": "Aberração",
        "nd": "13",
        "tamanho": "Grande",
        "descricao": "Aberração paranoica e megalomaníaca com olho central anti-magia e tentáculos oculares mortais.",
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
            "Resistência Legendária (3/dia)",
            "Ações Legendárias (3): Truque, Toque Paralisante, Olhar Assustador, Perturbação da Vida"
        ],
        "especial": "Filatério: só pode ser destruído permanentemente se seu filatério for destruído"
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