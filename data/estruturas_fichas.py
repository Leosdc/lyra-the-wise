"""
Estruturas de fichas por sistema de RPG.
Define seções e campos que cada sistema utiliza em suas fichas de personagem.
"""

ESTRUTURAS_FICHAS = {
    "dnd5e": {
        "secoes": ["basico", "atributos", "recursos", "combate", "pericias", "equipamento", "magia", "historia"],
        "campos": {
            "basico": ["Nome", "Raça", "Classe", "Nível", "Antecedente", "Alinhamento", "XP"],
            "atributos": ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"],
            "recursos": ["HP Máximo", "HP Atual", "HP Temporário", "Dados de Vida", "Bônus de Proficiência"],
            "combate": ["CA", "Iniciativa", "Velocidade", "Ataques"],
            "pericias": ["Acrobacia", "Arcanismo", "Atletismo", "Atuação", "Blefar", "Furtividade", "História", "Intimidação", "Intuição", "Investigação", "Lidar com Animais", "Medicina", "Natureza", "Percepção", "Persuasão", "Prestidigitação", "Religião", "Sobrevivência"],
            "equipamento": ["Armas", "Armadura", "Itens Mágicos", "Equipamento Mundano", "Dinheiro (PO)"],
            "magia": ["Nível de Conjurador", "CD de Magia", "Bônus de Ataque Mágico", "Espaços de Magia", "Magias Conhecidas/Preparadas"],
            "historia": ["Personalidade", "Ideais", "Vínculos", "Defeitos", "História", "Aparência"]
        }
    },
    
    "pathfinder": {
        "secoes": ["basico", "atributos", "recursos", "combate", "pericias", "equipamento", "magia", "talentos", "historia"],
        "campos": {
            "basico": ["Nome", "Ancestralidade", "Heritage", "Classe", "Nível", "Background", "Divindade", "Tamanho"],
            "atributos": ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"],
            "recursos": ["HP Máximo", "HP Atual", "Pontos de Resolução", "Pontos Heroicos"],
            "combate": ["CA", "CD de Classe", "Fortitude", "Reflexos", "Vontade", "Velocidade", "Percepção", "Ataques"],
            "pericias": ["Acrobacia", "Arcanismo", "Atletismo", "Artesanato", "Diplomacia", "Enganação", "Furtividade", "Intimidação", "Conhecimento", "Medicina", "Natureza", "Ocultismo", "Performance", "Religião", "Sociedade", "Sobrevivência", "Ladinagem"],
            "equipamento": ["Armas", "Armadura", "Escudo", "Itens Investidos", "Bulk Atual/Máximo", "Dinheiro (PO)"],
            "magia": ["Tradição Mágica", "CD de Magia", "Ataque Mágico", "Pontos de Foco", "Magias Preparadas", "Cantrips"],
            "talentos": ["Talentos de Ancestralidade", "Talentos de Classe", "Talentos de Perícia", "Talentos Gerais"],
            "historia": ["Personalidade", "Crenças", "História", "Aparência", "Idade"]
        }
    },
    
    "cthulhu": {
        "secoes": ["basico", "caracteristicas", "recursos", "combate", "pericias", "equipamento", "historia"],
        "campos": {
            "basico": ["Nome", "Ocupação", "Idade", "Sexo", "Residência", "Local de Nascimento"],
            "caracteristicas": ["FOR (Força)", "CON (Constituição)", "TAM (Tamanho)", "DES (Destreza)", "APA (Aparência)", "INT (Inteligência)", "POD (Poder)", "EDU (Educação)", "SOR (Sorte)"],
            "recursos": ["HP Máximo", "HP Atual", "Sanidade Máxima", "Sanidade Atual", "Pontos de Magia", "Movimento", "Dano Bônus", "Constituição"],
            "combate": ["Esquiva", "Lutar (Briga)", "Armas de Fogo", "Armas"],
            "pericias": ["Antropologia", "Arremessar", "Arte/Ofício", "Avaliação", "Charme", "Ciência", "Consertos Elétricos", "Consertos Mecânicos", "Contabilidade", "Dirigir Auto", "Direito", "Disfarce", "Encontrar", "Escutar", "Esquivar", "Furtividade", "História", "Hipnose", "Intimidação", "Lábia", "Língua Própria", "Medicina", "Mitos de Cthulhu", "Natação", "Navegação", "Nível de Crédito", "Ocultismo", "Operar Maquinaria Pesada", "Persuasão", "Pilotar", "Primeiros Socorros", "Psicanálise", "Psicologia", "Rastrear", "Saltar", "Treinar Animais"],
            "equipamento": ["Armas", "Equipamento de Investigação", "Itens Pessoais", "Dinheiro"],
            "historia": ["Descrição Pessoal", "Ideologia/Crenças", "Pessoas Importantes", "Locais Significativos", "Posses Valiosas", "Traços", "Fobias e Manias", "Feridas e Cicatrizes", "Encontros com o Estranho"]
        }
    },
    
    "vampire": {
        "secoes": ["basico", "atributos", "habilidades", "recursos", "disciplinas", "vantagens", "historia"],
        "campos": {
            "basico": ["Nome", "Conceito", "Crônica", "Ambição", "Desejo", "Predador", "Clã", "Geração", "Sire"],
            "atributos": ["Força", "Destreza", "Vigor", "Carisma", "Manipulação", "Compostura", "Inteligência", "Raciocínio", "Perseverança"],
            "habilidades": ["Atletismo", "Armas Brancas", "Briga", "Condução", "Armas de Fogo", "Furtividade", "Sobrevivência", "Empatia com Animais", "Etiqueta", "Intuição", "Intimidação", "Liderança", "Performance", "Persuasão", "Lábia", "Manha", "Acadêmicos", "Consciência", "Finanças", "Investigação", "Medicina", "Ocultismo", "Política", "Ciência", "Tecnologia"],
            "recursos": ["Saúde", "Força de Vontade", "Humanidade", "Fome", "Potência do Sangue", "Pontos de Experiência"],
            "disciplinas": ["Disciplinas de Clã", "Disciplinas Adquiridas", "Poderes", "Rituais de Sangue"],
            "vantagens": ["Antecedentes", "Méritos", "Lençóis de Lenda", "Vínculo de Clã"],
            "historia": ["Convicções", "Pilares", "Máscara", "Juramentos", "Coterie", "História", "Aparência", "Idade Aparente", "Idade Verdadeira"]
        }
    },
    
    "shadowrun": {
        "secoes": ["basico", "atributos", "recursos", "pericias", "equipamento", "magia_ressonancia", "historia"],
        "campos": {
            "basico": ["Nome", "Metatipo", "Arquétipo", "Idade", "Sexo", "Etnia", "Estilo de Vida"],
            "atributos": ["Corpo", "Agilidade", "Reação", "Força", "Força de Vontade", "Lógica", "Intuição", "Carisma", "Essência", "Magia", "Ressonância"],
            "recursos": ["Monitor de Dano Físico", "Monitor de Dano Atordoante", "Borda", "Iniciativa", "Karma", "Nuyen", "Limite de Essência"],
            "pericias": ["Armas de Fogo", "Armas Brancas", "Atletismo", "Briga", "Condução", "Furtividade", "Percepção", "Computadores", "Cibercombate", "Hacking Eletrônico", "Software", "Conjuração", "Encantamento", "Invocação", "Banimento", "Contrabandos", "Etiqueta", "Intimidação", "Liderança", "Negociação", "Medicina"],
            "equipamento": ["Cyberware", "Bioware", "Armas", "Armadura", "Equipamento Matriz", "Veículos", "Drones", "Nuyen"],
            "magia_ressonancia": ["Tradição Mágica", "Feitiços", "Formas de Conjuração", "Espíritos Vinculados", "Sprites Registrados", "Formas Complexas"],
            "historia": ["Conceito", "Contatos", "Inimigos", "História", "Aparência"]
        }
    },
    
    "fate_core": {
        "secoes": ["basico", "aspectos", "pericias", "facanhas", "recursos", "consequencias"],
        "campos": {
            "basico": ["Nome", "Descrição", "Campanha", "Nível de Poder"],
            "aspectos": ["Conceito", "Dificuldade", "Aspecto 3", "Aspecto 4", "Aspecto 5"],
            "pericias": ["Lista de Perícias (Nível Ótimo +4)", "Nível Bom +3", "Nível Razoável +2", "Nível Regular +1"],
            "facanhas": ["Façanha 1", "Façanha 2", "Façanha 3"],
            "recursos": ["Recarga de Pontos de Destino", "Pontos de Destino Atuais", "Estresse Físico", "Estresse Mental"],
            "consequencias": ["Consequência Suave (2)", "Consequência Moderada (4)", "Consequência Severa (6)"]
        }
    },
    
    "dungeon_world": {
        "secoes": ["basico", "atributos", "movimentos", "recursos", "equipamento", "vinculos", "aparencia"],
        "campos": {
            "basico": ["Nome", "Classe", "Raça", "Nível", "XP"],
            "atributos": ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"],
            "movimentos": ["Movimentos Básicos", "Movimentos de Classe", "Movimentos Especiais"],
            "recursos": ["HP Máximo", "HP Atual", "Armadura", "Dano"],
            "equipamento": ["Carga Atual", "Carga Máxima", "Moedas", "Equipamento", "Armas"],
            "vinculos": ["Vínculo 1", "Vínculo 2", "Vínculo 3"],
            "aparencia": ["Olhos", "Corpo", "Roupas", "Descrição"]
        }
    },
    
    "blades": {
        "secoes": ["basico", "acoes", "atributos_resistencia", "recursos", "trauma_vice", "equipamento", "contatos"],
        "campos": {
            "basico": ["Nome", "Playbook", "Herança", "Background", "Conceito"],
            "acoes": ["Enganar", "Finesse", "Caçar", "Esgueirar", "Comandar", "Consorciar", "Manipular", "Estudar", "Pesquisar", "Reparar", "Demolir", "Desarmar"],
            "atributos_resistencia": ["Insight", "Prowess", "Resolve"],
            "recursos": ["Estresse (Max 9)", "Trauma", "Armadura", "Carga Pesada", "Carga Normal", "Carga Leve"],
            "trauma_vice": ["Traumas", "Vício", "Purveyor"],
            "equipamento": ["Itens de Carga", "Equipamento Especial de Playbook"],
            "contatos": ["Amigos", "Rivais", "Vítimas"]
        }
    },
    
    "numenera": {
        "secoes": ["basico", "pools", "pericias", "habilidades", "equipamento", "cyphers", "historia"],
        "campos": {
            "basico": ["Nome", "Tipo (Glaive/Jack/Nano)", "Descritor", "Foco", "Tier", "Esforço", "XP"],
            "pools": ["Might (Máx)", "Might (Atual)", "Speed (Máx)", "Speed (Atual)", "Intellect (Máx)", "Intellect (Atual)"],
            "pericias": ["Treinado em", "Especializado em", "Inabilidade em"],
            "habilidades": ["Habilidades de Tipo", "Habilidades de Descritor", "Habilidades de Foco"],
            "equipamento": ["Armas", "Armadura (Redutor de Velocidade)", "Equipamento", "Shins"],
            "cyphers": ["Cypher 1 (Nível)", "Cypher 2 (Nível)", "Artefatos", "Oddities"],
            "historia": ["Conexão com Outros PCs", "Background", "Notas"]
        }
    }
}

# Estrutura genérica para sistemas sem estrutura específica definida
ESTRUTURA_GENERICA = {
    "secoes": ["basico", "atributos", "recursos", "combate", "equipamento", "historia"],
    "campos": {
        "basico": ["Nome", "Raça/Ancestralidade", "Classe/Profissão", "Nível/Experiência", "Conceito"],
        "atributos": ["Atributos Principais do Sistema"],
        "recursos": ["Pontos de Vida/Saúde", "Recursos Especiais"],
        "combate": ["Defesa/CA", "Ataques", "Iniciativa"],
        "equipamento": ["Armas", "Armadura", "Itens", "Dinheiro"],
        "historia": ["Personalidade", "História", "Motivações", "Aparência"]
    }
}