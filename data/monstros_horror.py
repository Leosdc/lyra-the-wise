"""
Banco de dados de monstros para sistemas de horror.
Inclui Call of Cthulhu e outros sistemas de horror cósmico.
"""

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