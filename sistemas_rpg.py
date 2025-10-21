"""
Banco de dados com todos os sistemas de RPG suportados.
Cada sistema tem: nome, descricao (narrativa), categoria, dados, atributos, classes, mecanicas e nivel_max.
"""

# ===== D&D E DERIVADOS =====
SISTEMAS_DISPONIVEIS = {
    "dnd5e": {
        "nome": "D&D 5ª Edição",
        "descricao": "Fantasia heróica de masmorras e dragões, onde aventureiros crescem de novatos a lendas guiados pelo d20.",
        "categoria": "D&D",
        "dados": ["d4","d6","d8","d10","d12","d20","d100"],
        "atributos": ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
        "classes": ["Bárbaro","Bardo","Clérigo","Druida","Guerreiro","Monge","Paladino","Ranger","Ladino","Feiticeiro","Bruxo","Mago","Artífice"],
        "mecanicas": "Teste d20 + modificadores vs CD/CA; vantagens/desvantagens; magias por espaços.",
        "nivel_max": 20
    },
    "dnd35": {
        "nome": "D&D 3.5",
        "descricao": "Uma caixa de ferramentas enorme: talentos, perícias e conjurações que permitem heróis minuciosamente construídos.",
        "categoria": "D&D",
        "dados": ["d4","d6","d8","d10","d12","d20","d100"],
        "atributos": ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
        "classes": ["Bárbaro","Bardo","Clérigo","Druida","Guerreiro","Monge","Paladino","Ranger","Ladino","Feiticeiro","Mago"],
        "mecanicas": "d20 + modificadores vs CD/CA; multiclasse livre; perícias detalhadas.",
        "nivel_max": 20
    },
    "pathfinder1e": {
        "nome": "Pathfinder 1ª Edição",
        "descricao": "Descendência de D&D 3.5, repleta de opções; otimização e profundidade para campanhas longas e épicas.",
        "categoria": "D&D",
        "dados": ["d4","d6","d8","d10","d12","d20","d100"],
        "atributos": ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
        "classes": ["Bárbaro","Bardo","Clérigo","Druida","Guerreiro","Monge","Paladino","Ranger","Ladino","Feiticeiro","Mago","Alquimista","Cavaleiro","Inquisidor","Oráculo","Invocador","Bruxo"],
        "mecanicas": "d20 + modificadores; talentos vastos; perícias extensas.",
        "nivel_max": 20
    },
    "pathfinder": {
        "nome": "Pathfinder 2ª Edição",
        "descricao": "Aventuras táticas em ritmo ágil: três ações por turno, graus de sucesso e equilíbrio entre arquétipos.",
        "categoria": "D&D",
        "dados": ["d4","d6","d8","d10","d12","d20"],
        "atributos": ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
        "classes": ["Alquimista","Bárbaro","Bardo","Campeão","Clérigo","Druida","Guerreiro","Monge","Ranger","Ladino","Feiticeiro","Mago","Inventor","Investigador","Oráculo","Bruxo"],
        "mecanicas": "Sistema de 3 ações; quatro graus de sucesso; proficiências progressivas.",
        "nivel_max": 20
    },
    "13thage": {
        "nome": "13th Age",
        "descricao": "Heroísmo cinematográfico movido por ícones míticos, com regras leves e cenas cheias de estilo.",
        "categoria": "D&D",
        "dados": ["d4","d6","d8","d10","d12","d20"],
        "atributos": ["Força","Constituição","Destreza","Inteligência","Sabedoria","Carisma"],
        "classes": ["Bárbaro","Bardo","Clérigo","Guerreiro","Paladino","Ranger","Ladino","Feiticeiro","Mago","Monge","Necromante","Invocador"],
        "mecanicas": "Escalonamento de dano; relações com ícones; foco em cenas-chave.",
        "nivel_max": 10
    },

    # ===== HORROR / INVESTIGAÇÃO =====
    "cthulhu": {
        "nome": "Call of Cthulhu 7ª Edição",
        "descricao": "Mistérios sombrios e saber proibido; coragem e sanidade testadas contra horrores cósmicos.",
        "categoria": "Horror",
        "dados": ["d4","d6","d8","d10","d20","d100"],
        "atributos": ["FOR","CON","TAM","DES","APA","INT","POD","EDU","SOR"],
        "classes": ["Investigador"],
        "mecanicas": "Percentual (d100) vs perícia; perdas de Sanidade; falhas críticas.",
        "nivel_max": "N/A"
    },

    # ===== WORLD / CHRONICLES OF DARKNESS =====
    "cofd": {
        "nome": "Chronicles of Darkness",
        "descricao": "Segredos modernos e monstros elegantes; histórias pessoais entre o medo e o desejo.",
        "categoria": "World of Darkness",
        "dados": ["d10"],
        "atributos": ["Inteligência","Raciocínio","Perseverança","Força","Destreza","Vigor","Presença","Manipulação","Autocontrole"],
        "classes": ["Mortal","Vampiro","Lobisomem","Mago","Prometeano","Changeling","Caçador","Múmia","Demônio","Besta"],
        "mecanicas": "Pool de d10; 8+ sucesso; 10 explode; condições e méritos.",
        "nivel_max": "N/A"
    },
    "vampire": {
        "nome": "Vampire: The Masquerade (V5)",
        "descricao": "Sede, política e máscaras — vampiros disputam poder enquanto agarram os últimos fios de humanidade.",
        "categoria": "World of Darkness",
        "dados": ["d10"],
        "atributos": ["Força","Destreza","Vigor","Carisma","Manipulação","Compostura","Inteligência","Raciocínio","Perseverança"],
        "classes": ["Brujah","Gangrel","Malkaviano","Nosferatu","Toreador","Tremere","Ventrue","Caitiff","Thin-blood"],
        "mecanicas": "Pool de d10; Fome; Compulsões; Máscara e Juramentos.",
        "nivel_max": "N/A"
    },
    "werewolf": {
        "nome": "Werewolf: The Apocalypse",
        "descricao": "Garra e espírito: guerreiros lupinos lutam pela Terra contra a corrupção do Wyrm.",
        "categoria": "World of Darkness",
        "dados": ["d10"],
        "atributos": ["Força","Destreza","Vigor","Carisma","Manipulação","Aparência","Percepção","Inteligência","Raciocínio"],
        "classes": ["Ahroun","Galliard","Philodox","Ragabash","Theurge"],
        "mecanicas": "Pool de d10; Fúria, Gnose e Honra; múltiplas formas.",
        "nivel_max": "N/A"
    },
    "mage": {
        "nome": "Mage: The Ascension",
        "descricao": "Vontade molda a realidade — mas desafiar o paradigma cobra seu preço em paradoxo.",
        "categoria": "World of Darkness",
        "dados": ["d10"],
        "atributos": ["Força","Destreza","Vigor","Carisma","Manipulação","Aparência","Percepção","Inteligência","Raciocínio"],
        "classes": ["Akashic Brotherhood","Celestial Chorus","Cult of Ecstasy","Dreamspeakers","Euthanatos","Order of Hermes","Sons of Ether","Verbena","Virtual Adepts"],
        "mecanicas": "Pool de d10; Esferas; Paradoxo; roteiros de efeito.",
        "nivel_max": "N/A"
    },

    # ===== FICÇÃO CIENTÍFICA =====
    "shadowrun": {
        "nome": "Shadowrun 5ª/6ª Edição",
        "descricao": "Fios de neon e espíritos antigos: elfos hackers e magos corporativos em assaltos ousados.",
        "categoria": "Sci-Fi Cyberpunk",
        "dados": ["d6"],
        "atributos": ["Corpo","Agilidade","Reação","Força","Força de Vontade","Lógica","Intuição","Carisma","Essência","Magia"],
        "classes": ["Street Samurai","Decker","Rigger","Mago","Xamã","Adeptus Físico","Face"],
        "mecanicas": "Pool de d6; 5+ sucesso; matriz, magia e chrome.",
        "nivel_max": "N/A"
    },
    "cyberpunk2020": {
        "nome": "Cyberpunk 2020",
        "descricao": "As ruas têm seu próprio ritmo: trilha de neon, dívidas e balas em Night City.",
        "categoria": "Sci-Fi Cyberpunk",
        "dados": ["d6","d10"],
        "atributos": ["INT","REF","TECH","COOL","ATTR","LUCK","MA","BODY","EMP"],
        "classes": ["Rockerboy","Solo","Netrunner","Techie","Medtech","Media","Cop","Corporate","Fixer","Nomad"],
        "mecanicas": "d10 + atributo + perícia vs dificuldade; estilo é tudo.",
        "nivel_max": "N/A"
    },
    "cyberpunkred": {
        "nome": "Cyberpunk RED",
        "descricao": "Depois das cinzas, sobreviventes pintam de vermelho as ruas: gigs, implantes e netrunning revisado.",
        "categoria": "Sci-Fi Cyberpunk",
        "dados": ["d6","d10"],
        "atributos": ["INT","REF","DEX","TECH","COOL","WILL","LUCK","MOVE","BODY","EMP"],
        "classes": ["Rockerboy","Solo","Netrunner","Tech","Medtech","Media","Lawman","Exec","Fixer","Nomad"],
        "mecanicas": "d10 + stat + skill vs DV; netrunning tático.",
        "nivel_max": "N/A"
    },
    "eclipse": {
        "nome": "Eclipse Phase 2ª Edição",
        "descricao": "Mentes que migram; corpos descartáveis; conspirações pós-humanas à sombra de horrores TITAN.",
        "categoria": "Sci-Fi Transumano",
        "dados": ["d10","d100"],
        "atributos": ["Cognição","Intuição","Reflexos","Sagacidade","Somática","Força de Vontade"],
        "classes": ["Backgrounds e facções em vez de classes rígidas"],
        "mecanicas": "d100 vs perícia; sleeves (corpos) e morphs; resleeving.",
        "nivel_max": "N/A"
    },
    "startrek": {
        "nome": "Star Trek Adventures (Modiphius)",
        "descricao": "Explorar o desconhecido com diplomacia, ciência e bravura sob a bandeira da Frota Estelar.",
        "categoria": "Sci-Fi Space Opera",
        "dados": ["d6","d20"],
        "atributos": ["Controle","Fitness","Presença","Razão","Insight","Destreza"],
        "classes": ["Comando","Operações","Ciências","Medicina","Segurança","Engenharia"],
        "mecanicas": "2d20; sucessos vs dificuldade; Momentum e Threat.",
        "nivel_max": "N/A"
    },
    "starwars_d20": {
        "nome": "Star Wars RPG (d20/Saga)",
        "descricao": "Sabres de luz, blasters e a Força em crônicas cinematográficas de heróis contra impérios.",
        "categoria": "Sci-Fi Space Opera",
        "dados": ["d4","d6","d8","d10","d12","d20"],
        "atributos": ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
        "classes": ["Jedi","Soldado","Batedor","Nobre","Cafajeste","Técnico"],
        "mecanicas": "d20 + modificadores; talentos por nível; Força como poderes.",
        "nivel_max": 20
    },
    "starwars_ffg": {
        "nome": "Star Wars RPG (FFG)",
        "descricao": "Destinos traçados em dados narrativos — triunfos, ameaças e escolhas morais na galáxia distante.",
        "categoria": "Sci-Fi Space Opera",
        "dados": ["dados narrativos"],
        "atributos": ["Agilidade","Astúcia","Inteligência","Vigor","Presença","Força de Vontade"],
        "classes": ["Carreiras e especializações variadas"],
        "mecanicas": "Dados personalizados (sucesso/falha, vantagem/ameaça, triunfo/desespero).",
        "nivel_max": "N/A"
    },

    # ===== WARHAMMER =====
    "wfrp1e": {
        "nome": "Warhammer Fantasy 1ª Edição",
        "descricao": "Lama, aço e desespero: o Velho Mundo engole tolos — a sorte salva, o Caos cobra.",
        "categoria": "Grimdark Fantasy",
        "dados": ["d6","d10","d100"],
        "atributos": ["WS","BS","S","T","I","A","Dex","Ld","Int","Cl","WP","Fel"],
        "classes": ["Carreiras variadas (Soldado, Ladrão, Mago, etc.)"],
        "mecanicas": "d100 vs atributo; eventos cruéis e carreiras mortais.",
        "nivel_max": "N/A"
    },
    "wfrp4e": {
        "nome": "Warhammer Fantasy 4ª Edição",
        "descricao": "O mesmo mundo cruel, agora com regras polidas — avanços medidos em cicatrizes e moedas.",
        "categoria": "Grimdark Fantasy",
        "dados": ["d10","d100"],
        "atributos": ["WS","BS","S","T","I","Ag","Dex","Int","WP","Fel"],
        "classes": ["Múltiplas carreiras e especializações"],
        "mecanicas": "d100 vs atributo; níveis de sucesso (SL) e riscos constantes.",
        "nivel_max": "N/A"
    },

    # ===== GENÉRICOS / UNIVERSAIS =====
    "gurps": {
        "nome": "GURPS 4ª Edição",
        "descricao": "Qualquer mundo, qualquer era: a sua imaginação define o cenário, os pontos definem os heróis.",
        "categoria": "Universal",
        "dados": ["d6"],
        "atributos": ["ST","DX","IQ","HT"],
        "classes": ["Criação por pontos (sem classes fixas)"],
        "mecanicas": "3d6 sob atributo/perícia; realismo modular; vantagens e desvantagens.",
        "nivel_max": "N/A"
    },
    "fate_core": {
        "nome": "FATE Core",
        "descricao": "Histórias dirigidas por Aspectos: invoque destinos, reescreva a cena — a ficção vem primeiro.",
        "categoria": "Universal Narrativo",
        "dados": ["dF"],
        "atributos": ["Customizáveis (Approaches/Skills)"],
        "classes": ["Sem classes; conceitos e Aspectos"],
        "mecanicas": "4dF + perícia vs oposição; Pontos de Destino; Aspectos e Façanhas.",
        "nivel_max": "N/A"
    },
    "fate_accelerated": {
        "nome": "FATE Accelerated",
        "descricao": "A essência do FATE em movimento: seis abordagens, ação elegante e improviso veloz.",
        "categoria": "Universal Narrativo",
        "dados": ["dF"],
        "atributos": ["Ágil","Cuidadoso","Esperto","Estiloso","Poderoso","Sorrateiro"],
        "classes": ["Sem classes; Aspectos definem papéis"],
        "mecanicas": "4dF + abordagem; façanhas simples; criação de vantagens.",
        "nivel_max": "N/A"
    },
    "savage": {
        "nome": "Savage Worlds",
        "descricao": "Pulp de sangue quente: regras rápidas, ação furiosa e qualquer gênero ao alcance.",
        "categoria": "Universal",
        "dados": ["d4","d6","d8","d10","d12"],
        "atributos": ["Agilidade","Astúcia","Espírito","Força","Vigor"],
        "classes": ["Construção por edges/hindrances"],
        "mecanicas": "Atributos por dado; Wild Die; cartas na iniciativa.",
        "nivel_max": "N/A"
    },
    "cortex": {
        "nome": "Cortex Prime",
        "descricao": "Engrenagens narrativas sob medida — componha seu conjunto de dados e conte sua própria série.",
        "categoria": "Universal Modular",
        "dados": ["d4","d6","d8","d10","d12"],
        "atributos": ["Modulares (definidos por jogo)"],
        "classes": ["Sem classes; módulos e SFX"],
        "mecanicas": "Pool de dados; escolhe dois para total e um para efeito; Distinções e Complicações.",
        "nivel_max": "N/A"
    },

    # ===== POWERED BY THE APOCALYPSE (PbtA) =====
    "apocalypse": {
        "nome": "Apocalypse World",
        "descricao": "Poeira, gasolina e desejo: o fim do mundo é íntimo e violento — jogue pra ver o que acontece.",
        "categoria": "PbtA",
        "dados": ["d6"],
        "atributos": ["Cool","Hard","Hot","Sharp","Weird"],
        "classes": ["Angel","Battlebabe","Brainer","Chopper","Driver","Gunlugger","Hardholder","Hocus","Savvyhead","Skinner"],
        "mecanicas": "2d6 + stat; 10+ sucesso, 7-9 complicado, 6- MC move.",
        "nivel_max": "N/A"
    },
    "dungeon_world": {
        "nome": "Dungeon World",
        "descricao": "Exploração fantástica em ritmo narrativo: jogue para descobrir a história, não para lembrar tabelas.",
        "categoria": "PbtA Fantasy",
        "dados": ["d6"],
        "atributos": ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"],
        "classes": ["Bárbaro","Bardo","Clérigo","Druida","Guerreiro","Paladino","Ranger","Ladino","Mago"],
        "mecanicas": "2d6 + mod; 10+ pleno, 7-9 custo/risco; movimentos do GM.",
        "nivel_max": 10
    },
    "monster_week": {
        "nome": "Monster of the Week",
        "descricao": "Caçadores enfrentam pesadelos semanais em tramas urbanas: mistério, perigo e drama pessoal.",
        "categoria": "PbtA Horror Moderno",
        "dados": ["d6"],
        "atributos": ["Charm","Cool","Sharp","Tough","Weird"],
        "classes": ["The Chosen","The Expert","The Flake","The Initiate","The Monstrous","The Mundane","The Professional","The Spooky","The Wronged"],
        "mecanicas": "2d6 + stat; investigação e caça com tom seriado.",
        "nivel_max": "N/A"
    },

    # ===== FORGED IN THE DARK =====
    "blades": {
        "nome": "Blades in the Dark",
        "descricao": "Lâminas, fantasmas e ambição: uma gangue ergue-se nas sombras de uma cidade industrial assombrada.",
        "categoria": "FitD Crime Fantasy",
        "dados": ["d6"],
        "atributos": ["Insight","Prowess","Resolve"],
        "classes": ["Cutter","Hound","Leech","Lurk","Slide","Spider","Whisper"],
        "mecanicas": "Posição & Efeito; estresse; flashbacks; crew e território.",
        "nivel_max": "N/A"
    },

    # ===== OUTROS POPULARES =====
    "7thsea": {
        "nome": "7th Sea 2ª Edição",
        "descricao": "Mantos esvoaçantes, duelos e intrigas: heroísmo maior que a vida em mares de aventura.",
        "categoria": "Swashbuckling",
        "dados": ["d10"],
        "atributos": ["Brawn","Finesse","Resolve","Wits","Panache"],
        "classes": ["Escolas de esgrima e nações variadas"],
        "mecanicas": "Pool de d10; forma pares que viram Raises; riscos e consequências.",
        "nivel_max": "N/A"
    },
    "shadowdemon": {
        "nome": "Shadow of the Demon Lord",
        "descricao": "Magia perigosa e aço manchado: um mundo que cambaleia rumo ao fim — sobreviva, se puder.",
        "categoria": "Dark Fantasy",
        "dados": ["d6","d20"],
        "atributos": ["Força","Agilidade","Intelecto","Vontade"],
        "classes": ["Paths: Novice → Expert → Master"],
        "mecanicas": "d20 + modificadores; boons/banes; progressão enxuta.",
        "nivel_max": 10
    },
    "mutants": {
        "nome": "Mutants & Masterminds 3ª Edição",
        "descricao": "Quadrinhos em mesa: construa qualquer super, do vigilante urbano ao semideus interestelar.",
        "categoria": "Super-heróis",
        "dados": ["d20"],
        "atributos": ["Força","Agilidade","Combate","Consciência","Destreza","Resistência","Intelecto","Presença"],
        "classes": ["Criação livre por efeitos/poderes"],
        "mecanicas": "d20 + rank vs defesa; PL define limites; salvamentos.",
        "nivel_max": "PL 1-20"
    },
    "champions": {
        "nome": "Champions / Hero System",
        "descricao": "Personalização absoluta de poderes — a física é um contrato social entre heróis e dados.",
        "categoria": "Super-heróis",
        "dados": ["d6"],
        "atributos": ["STR","DEX","CON","BODY","INT","EGO","PRE","COM"],
        "classes": ["Criação por pontos detalhada"],
        "mecanicas": "3d6 sob perícia; compra de poderes; frameworks.",
        "nivel_max": "N/A"
    },
    "faserip": {
        "nome": "Marvel Super Heroes (FASERIP)",
        "descricao": "Cores, ação e destino em uma tabela universal: do amigão da vizinhança a titãs cósmicos.",
        "categoria": "Super-heróis",
        "dados": ["d10","d100"],
        "atributos": ["Fighting","Agility","Strength","Endurance","Reason","Intuition","Psyche"],
        "classes": ["Criação por ranks e poderes"],
        "mecanicas": "d100 na Tabela Universal; Karma; escalas absurdas.",
        "nivel_max": "N/A"
    },
    "deadlands": {
        "nome": "Deadlands (Savage Worlds)",
        "descricao": "Poeira, pólvora e o sobrenatural: o Velho Oeste onde o destino é jogado em cartas.",
        "categoria": "Weird West",
        "dados": ["d4","d6","d8","d10","d12"],
        "atributos": ["Agilidade","Astúcia","Espírito","Força","Vigor"],
        "classes": ["Arquetipos variados (Pistoleiro, Xamã, Huckster...)"],
        "mecanicas": "Motor Savage; poker/magia; iniciativa com baralho.",
        "nivel_max": "N/A"
    },
    "fiasco": {
        "nome": "Fiasco",
        "descricao": "Comédia de erros sem mestre: ambição, incompetência e consequências deliciosamente trágicas.",
        "categoria": "Narrativo GMless",
        "dados": ["d6"],
        "atributos": ["Relações","Objetos","Locais","Necessidades"],
        "classes": ["Sem classes; playsets guiam a história"],
        "mecanicas": "Cenas alternadas; dados decidem rumo; Tilt & Aftermath.",
        "nivel_max": "N/A"
    },
    "microlite20": {
        "nome": "Microlite20",
        "descricao": "D&D destilado em poucas páginas — leve, direto e pronto para aventuras rápidas.",
        "categoria": "D&D Ultra-Lite",
        "dados": ["d4","d6","d8","d10","d12","d20"],
        "atributos": ["Força","Destreza","Mente"],
        "classes": ["Guerreiro","Ladino","Mago"],
        "mecanicas": "d20 + perícia + atributo vs CD; ultra-simplificado.",
        "nivel_max": 20
    },
    "tiny_dungeon": {
        "nome": "Tiny Dungeon 2ª Edição",
        "descricao": "Fantasia minimalista: regras pequenas, imaginação gigante — ideal para iniciantes.",
        "categoria": "Minimalista Fantasy",
        "dados": ["d6"],
        "atributos": ["Traços (traits) definem capacidades"],
        "classes": ["Heritages e opções simples"],
        "mecanicas": "2d6 (5+ sucesso); vantagem/desvantagem com 3d6/1d6.",
        "nivel_max": 10
    },
    "risus": {
        "nome": "Risus: The Anything RPG",
        "descricao": "Clichês viram dados, piadas viram golpes críticos — qualquer gênero, com humor.",
        "categoria": "Cômico Universal",
        "dados": ["d6"],
        "atributos": ["Clichês com níveis em dados"],
        "classes": ["Sem classes; tudo em clichês"],
        "mecanicas": "Pool de d6 por clichê; soma vs oponente; leve e caótico.",
        "nivel_max": "N/A"
    },
    "numenera": {
        "nome": "Numenera (Cypher System)",
        "descricao": "Um bilhão de eras adiante: magia que é tecnologia, segredos que são relíquias de deuses esquecidos.",
        "categoria": "Sci-Fantasy",
        "dados": ["d20"],
        "atributos": ["Might","Speed","Intellect (pools)"],
        "classes": ["Glaive","Jack","Nano"],
        "mecanicas": "Dificuldades 1–10; esforço consome pools; ciphers mudam o jogo.",
        "nivel_max": "Tier 1–6"
    },
    "l5r": {
        "nome": "Legend of the Five Rings (L5R)",
        "descricao": "Honra, dever e tragédia em Rokugan: samurais divididos entre o coração e o imperador.",
        "categoria": "Samurai Fantasy",
        "dados": ["d6","d10"],
        "atributos": ["Earth","Water","Fire","Air","Void"],
        "classes": ["Bushi","Courtier","Shugenja","Monk","Ninja"],
        "mecanicas": "Roll & Keep / dados de anel; conflitos sociais e duelos.",
        "nivel_max": "N/A"
    },
    "exalted": {
        "nome": "Exalted 3ª Edição",
        "descricao": "Soles ardentes e destinos tecidos: heróis sobre-humanos reescrevem a mitologia com seus feitos.",
        "categoria": "Épico Mitológico",
        "dados": ["d10"],
        "atributos": ["Força","Destreza","Vigor","Carisma","Manipulação","Aparência","Percepção","Inteligência","Raciocínio"],
        "classes": ["Solar","Lunar","Sidereal","Abyssal","Infernal","Dragon-Blooded"],
        "mecanicas": "Pool de d10 (7+ sucesso); Charms; Intimacies e motivações.",
        "nivel_max": "N/A"
    },
    "ars_magica": {
        "nome": "Ars Magica 5ª Edição",
        "descricao": "Colégios de magos e eras medievais: estudo, laboratório e poder hermético moldam a Europa Mítica.",
        "categoria": "Magia Hermética",
        "dados": ["d10"],
        "atributos": ["Strength","Stamina","Dexterity","Quickness","Intelligence","Perception","Presence","Communication"],
        "classes": ["Magus","Companion","Grog"],
        "mecanicas": "d10 + Traits vs Ease Factor; Técnicas + Formas; jogo em troupe.",
        "nivel_max": "N/A"
    },
    "pendragon": {
        "nome": "Pendragon (King Arthur)",
        "descricao": "Cavaleiros e paixões: gerações de linhagens buscam glória sob o peso do destino arturiano.",
        "categoria": "Cavaleiros Arturianos",
        "dados": ["d6","d20"],
        "atributos": ["SIZ","DEX","STR","CON","APP"],
        "classes": ["Cavaleiros de diversas regiões e ordens"],
        "mecanicas": "d20 vs perícia/traço; paixões; campanhas geracionais.",
        "nivel_max": "N/A"
    },
    "ironkingdoms": {
        "nome": "Iron Kingdoms",
        "descricao": "Engrenagens e feitiços: guerra a vapor, pistolas fumegantes e golems de ferro no campo de batalha.",
        "categoria": "Steampunk Fantasy",
        "dados": ["d6"],
        "atributos": ["Physique","Agility","Intellect"],
        "classes": ["Carreiras variadas (Soldado, Pistoleiro, Mago, etc.)"],
        "mecanicas": "2d6 + skill vs alvo; Warjacks; magia arcana.",
        "nivel_max": "N/A"
    },
    "victoriana": {
        "nome": "Victoriana 3ª Edição",
        "descricao": "Fumaça, magia e etiqueta: a Londres vitoriana onde o véu social esconde o impossível.",
        "categoria": "Vitoriano Fantasy",
        "dados": ["d6"],
        "atributos": ["Body","Dexterity","Strength","Charisma","Intelligence","Willpower"],
        "classes": ["Profissões e linhagens da era vitoriana"],
        "mecanicas": "Pool de d6 vs alvo; intriga social e ocultismo industrial.",
        "nivel_max": "N/A"
    }
}

# ===== ALIASES =====
ALIASES = {
    "dnd": "dnd5e",
    "d&d": "dnd5e",
    "pf": "pathfinder",
    "pf2e": "pathfinder",
    "pf1": "pathfinder1e",
    "starwars": "starwars_ffg",
    "star wars": "starwars_ffg",
    "wfrp": "wfrp4e"
}

# ===== FUNÇÕES AUXILIARES =====
def resolver_alias(alias: str):
    """Resolve um alias para a chave do sistema, mantendo busca case-insensitive."""
    if not isinstance(alias, str):
        return alias
    key = alias.strip().lower()
    return ALIASES.get(key, key)

def buscar_sistema(sistema_key: str):
    """Retorna o dicionário de um sistema pelo código ou alias.
    Se não encontrado, retorna D&D 5e como padrão.
    """
    key = resolver_alias(sistema_key)
    return SISTEMAS_DISPONIVEIS.get(key, SISTEMAS_DISPONIVEIS["dnd5e"])

def listar_por_categoria():
    """Agrupa sistemas por categoria, retornando dict[Categoria] -> [(codigo, nome)]."""
    categorias = {}
    for codigo, info in SISTEMAS_DISPONIVEIS.items():
        cat = info.get("categoria", "Outros")
        categorias.setdefault(cat, []).append((codigo, info.get("nome", codigo)))
    return categorias