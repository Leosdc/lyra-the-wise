"""
Banco de dados de monstros para outros sistemas.
Inclui Vampire: The Masquerade, Shadowrun e outros sistemas diversos.
"""

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
    
    "inseto_espirito": {
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