# 🎲 Lyra the Wise - Sistema de Sessões de RPG

> **Sistema completo de sessões privadas de RPG com IA, rolagens interativas e narrativa adaptativa**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Groq API](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange.svg)
![Version](https://img.shields.io/badge/Version-v2.5.4-purple.svg)

---

## 🌟 Visão Geral

**Lyra the Wise** é um bot de Discord que transforma seu servidor em uma mesa de RPG completa, com:

- 🤖 **IA Narrativa** - Groq AI gera histórias dinâmicas e contextuais
- 🎲 **Rolagens Interativas** - Sistema de botões para rolagens colaborativas
- 🎭 **Narrativa Adaptativa** - Escolha entre estilo extenso ou conciso
- 🎙️ **Voz Automática** - Canais de voz criados e gerenciados automaticamente
- 📊 **Gestão Completa** - Fichas, iniciativa, histórico e muito mais
- 🔒 **Sessões Privadas** - Canais exclusivos para cada grupo

---

## ✨ Features Principais

### 🎲 Sistema de Rolagens Interativo

Quando a IA solicita rolagens, aparecem **3 botões**:

```
┌─────────────────────────────────────────┐
│  🎲 Rolar Dados  │  🚫 Não Fazer Nada  |
└─────────────────────────────────────────┘
```

- **🎲 Rolar Dados**: Executa o teste solicitado
- **🚫 Não Fazer Nada**: Cancela ação, IA continua narrativa naturalmente
- **✏️ Outra Ação**: Permite descrever ação alternativa com `!acao`

O sistema **aguarda TODOS** os jogadores rolarem antes de continuar!

### 🎭 Estilos Narrativos

Escolha como Lyra conta a história:

#### 📖 Narrativa Extensa
```
✓ 3-5 parágrafos detalhados
✓ Descrições ricas dos 5 sentidos
✓ Atmosfera cinematográfica
✓ Profundidade emocional
✓ Ideal para: Roleplay, exploração, investigação
```

#### 📝 Narrativa Concisa
```
✓ 1-2 parágrafos curtos (4-5 frases)
✓ Foco em ação e essencial
✓ Narrativa ágil e dinâmica
✓ Respostas mais rápidas
✓ Ideal para: Combate, dungeons, sessões rápidas
```

### 🎮 Sessões de RPG
```
!iniciarsessao @jog1 @jog2
!selecionarficha <nome>
!sessoes
!infosessao
!cenanarrada <descrição>
!acao <descrição>
```

### ✨ Geração de Conteúdo
```
!npc <descrição>
!vilao <tipo>
!item <tipo>
!tesouro <nível>
!puzzle <tema>
!monstro <nome>
!cena <descrição>
```

### 📖 História & Campanha
```
!mestre <pergunta>
!plot <tema>
!sessao <tema>
!regra <dúvida>
```

---

## 🚀 Instalação

### Pré-requisitos

```bash
Python 3.11+
discord.py 2.3+
Groq API Key
```

### Setup

1. **Clone o repositório**
```bash
git clone https://github.com/Leosdc/lyra-the-wise.git
cd lyra-the-wise
```

2. **Instale dependências**
```bash
pip install -r requirements.txt
```

3. **Configure variáveis de ambiente**
```bash
DISCORD_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_chave_aqui
```

4. **Execute o bot**
```bash
python main.py
```

---

## 🎮 Guia Rápido

### 1️⃣ Criando uma Sessão

```bash
!iniciarsessao @Jogador1 @Jogador2 @Jogador3
```

**O que acontece:**
- ✅ Canal de texto privado criado
- ✅ Canal de voz privado criado
- ✅ Todos movidos automaticamente
- ✅ Botões de controle aparecem
- ✅ Fichas de cada jogador listadas

### 2️⃣ Selecionando Fichas

```bash
!selecionarficha Elara Corações de Cristal
```

**Sistema notifica:**
```
✅ Ficha Elara Corações de Cristal selecionada!
⏳ Aguardando 2 jogadores selecionarem ficha...
```

Quando todos selecionarem:
```
🎉 Todos os jogadores selecionaram suas fichas! O mestre pode iniciar a aventura.
```

### 3️⃣ Iniciando a Aventura

**Mestre clica:** `🎬 Iniciar Aventura`

**Escolhe estilo:**
- 📖 Narrativa Extensa
- 📝 Narrativa Concisa

**IA gera introdução épica!**

### 4️⃣ Durante a Sessão

**Jogadores descrevem ações:**
```bash
!acao examino a porta procurando armadilhas
```

**Mestre narra cenas:**
```bash
!cenanarrada um dragão pousa no topo da torre
```

**IA detecta quando precisa rolagens:**
```
🎲 Rolagem Necessária!
Tipo: 1d20+Percepção
Jogadores: @Elara, @Thorin
```

### 5️⃣ Combate

**Mestre clica:** `⚔️ Rolar Iniciativa`

```
⚔️ Iniciativa Rolada!
🥇 Elara → 22
🥈 Thorin → 18
🥉 Goblin → 12
```

Jogadores agem na ordem com `!acao`

### 6️⃣ Encerrando

**Mestre clica:** `🚪 Encerrar Sessão`

- ✅ Jogadores movidos para Torre da Maga
- ✅ Canais de voz e texto apagados
- ✅ Dados salvos

---

## 🎲 Sistema de Rolagens

### Como Funciona

1. **IA Detecta Necessidade**
   - Jogador usa `!acao ataco o goblin`
   - IA analisa e detecta necessidade de rolagem
   - Solicita com tag especial: `[ROLL: 1d20+3, Elara]`

2. **Sistema Exibe Botões**
   ```
   🎲 Rolagem Necessária!
   Tipo: 1d20+3
   Jogadores: @Elara
   
   [🎲 Rolar Dados] [🚫 Não Fazer Nada] [✏️ Outra Ação]
   ```

3. **Jogadores Escolhem**
   - **Rolar**: Executa teste
   - **Não Fazer**: IA narra sem teste
   - **Outra Ação**: Usa `!acao` novamente

4. **Sistema Aguarda Todos**
   ```
   ✅ Elara rolou: 1d20+3 = 18
   ⏳ Aguardando 1 jogador rolar...
   ```

5. **Resumo e Continuação**
   ```
   📊 Todas as Rolagens Concluídas!
   • Elara: 18
   • Thorin: 12
   
   ✨ A história continua...
   ```

6. **IA Narra Resultado**
   - Considera todos os valores
   - Narra consequências
   - Continua história

### Tipos de Rolagem Suportados

```
1d20        # D20 básico
1d20+5      # Com modificador
2d6         # Múltiplos dados
1d100       # Percentil
3d6+2       # Combinações
```

### Alvos de Rolagem

```
[ROLL: 1d20, todos]           # Todos jogadores
[ROLL: 1d20, Elara]           # Personagem específico
[ROLL: 1d20, Elara, Thorin]   # Múltiplos personagens
```

---

## 🎭 Estilos Narrativos

#### 📖 Narrativa Extensa

```
A porta de carvalho range suavemente sob seus dedos enquanto 
você a empurra. O cheiro de mofo e velas apagadas invade suas 
narinas, misturado com algo metálico - sangue, talvez. Suas 
botas afundam no tapete empoeirado, cada passo levantando 
pequenas nuvens que dançam na luz fraca da sua tocha.

As sombras se contorcem nas paredes de pedra, projetadas por 
relevos que retratam batalhas esquecidas. Você pode quase ouvir 
os gritos dos guerreiros, sentir o peso das espadas que nunca 
mais serão empunhadas. No centro da sala, uma mesa circular 
aguarda, coberta por um mapa amarelado cujas bordas se desfazem 
ao toque.

Ao se aproximar, você nota marcas recentes na poeira - pegadas. 
Alguém esteve aqui, e não faz muito tempo...
```

#### 📝 Narrativa Concisa

```
Você empurra a porta. O cômodo está escuro, cheira a mofo e 
sangue velho. No centro, uma mesa com mapa antigo. Pegadas 
recentes na poeira - alguém passou aqui há pouco.
```

### Quando Usar Cada Uma?

**Use Extensa quando:**
- ✅ Sessão focada em roleplay
- ✅ Explorando locais importantes
- ✅ Desenvolvendo NPCs
- ✅ Investigação e mistério
- ✅ Momentos dramáticos

**Use Concisa quando:**
- ✅ Combate intenso
- ✅ Dungeon crawling
- ✅ Sessões curtas (2-3h)
- ✅ Grupo grande (5+ jogadores)
- ✅ Foco em mecânicas

---

## 💡 Exemplos de Uso

### Exemplo Completo: Sessão de D&D 5e

```bash
# 1. MESTRE CRIA SESSÃO
!iniciarsessao @Alice @Bob @Carol

# ✅ Canais criados
# ✅ Todos movidos para voz
# ✅ Fichas listadas

# 2. JOGADORES SELECIONAM FICHAS
[Alice] !selecionarficha Elara Corações de Cristal
[Bob] !selecionarficha Thorin Martelo de Ferro
[Carol] !selecionarficha Kael Sombra Noturna

# 🎉 Todos os jogadores selecionaram suas fichas!

# 3. MESTRE INICIA AVENTURA
[Mestre clica: 🎬 Iniciar Aventura]
[Escolhe: 📖 Narrativa Extensa]

# IA GERA INTRODUÇÃO:
"""
A taverna do Dragão Vermelho está lotada esta noite. O cheiro 
de cerveja maltada mistura-se com fumaça de tabaco enquanto 
aventureiros de todos os cantos do reino trocam histórias de 
suas façanhas...
"""

# 4. JOGADORES AGEM
[Alice] !acao me aproximo do taverneiro e pergunto sobre rumores

# IA RESPONDE:
"""
O taverneiro, um anão de barba grisalha, limpa um copo enquanto 
te analisa com olhos experientes. "Rumores?" ele resmunga. 
"Tenho algo melhor que rumores, jovem. Tenho um trabalho."

Ele se inclina, baixando a voz. "Há uma caravana que precisa 
de escolta até Forte Névoa. Pagam bem, mas o caminho... 
digamos que não é dos mais seguros."

[ROLL: 1d20+Percepção, Elara]
"""

# BOTÕES APARECEM:
# [🎲 Rolar Dados] [🚫 Não Fazer Nada] [✏️ Outra Ação]

[Alice clica: 🎲 Rolar Dados]

# SISTEMA ROLA:
"""
🎲 Elara rolou: 1d20+3 = 18

📊 Todas as Rolagens Concluídas!
• Elara: 18
"""

# IA CONTINUA:
"""
Com sua percepção aguçada, você nota que o taverneiro está 
nervoso. Suas mãos tremem ligeiramente e seus olhos desviam 
para a janela a cada poucos segundos, como se esperasse algo...
"""

# 5. COMBATE ACONTECE
[Mestre] !cenanarrada goblins invadem a taverna

# IA EXPANDE:
"""
O vidro da janela se estilhaça em mil pedaços! Três goblins 
saltam para dentro, brandindo adagas enferrujadas e gritando 
em sua língua gutural. O taverneiro grita e mergulha atrás 
do balcão...
"""

[Mestre clica: ⚔️ Rolar Iniciativa]

# SISTEMA ROLA:
"""
⚔️ Iniciativa Rolada!
🥇 Elara → 22
🥈 Thorin → 18
🥉 Kael → 15
4. Goblin 1 → 12
5. Goblin 2 → 8
6. Goblin 3 → 5
"""

# JOGADORES AGEM NA ORDEM
[Alice] !acao disparo uma flecha no goblin mais próximo
[Bob] !acao avanço com meu martelo de guerra
[Carol] !acao lanço Raio de Gelo

# ... combate continua ...

# 6. FINAL DA SESSÃO
[Mestre clica: 🚪 Encerrar Sessão]

# ✅ Jogadores movidos para Torre da Maga
# ✅ Canais apagados
# ✅ Sessão salva
```

### Exemplo: Sessão Concisa (Dungeon Crawl)

```bash
# MESTRE ESCOLHE NARRATIVA CONCISA

[Mestre] !cenanarrada vocês entram na sala

# IA (CONCISA):
"""
Sala circular, 20 pés de diâmetro. Três portas - norte, 
leste, oeste. Cheiro de mofo. Pegadas recentes na poeira.
"""

[Alice] !acao examino as pegadas

# IA (CONCISA):
"""
Pegadas de humanoides, tamanho médio, 4-6 indivíduos. 
Levam à porta norte. Recentes - últimas horas.
"""

# RÁPIDO E DIRETO!
```

---

## 🧩 Estrutura do Projeto
```
lyra-the-wise/
├── main.py                   # Ponto de entrada
├── config.py                 # Configurações globais
├── utils.py                  # Funções auxiliares
├── sistemas_rpg.py           # Banco de dados de sistemas + estrutura de fichas
├── fichas_estruturadas.py    # Sistema de fichas estruturadas
├── sessoes_rpg.py            # Sistema de sessões
├── rpg_core.py               # Comandos principais
├── geracao_conteudo.py       # Geração de NPCs, monstros, etc
├── monstros_database.py      # Banco de monstros
├── help_painel.py            # Sistema de ajuda interativo
├── documentacao.py           # Documentação completa
├── utilidades.py             # Comandos administrativos
├── admin.py                  # Ferramentas de debug
├── bot_data/                 # Dados persistentes
│   ├── fichas_personagens.json
│   ├── sistemas_usuarios.json
│   └── sessoes_ativas.json
├── commands/
│   ├── sessoes_acao.py
│   └── sessoes_commands.py
│   └── __init__.py
├── core/
│   ├── sessao_helpers.py
│   └── __init__.py
├── views/
│   ├── sessao_views.py
│   └── __init__.py
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências Python
├── LICENSE                   # Licença MIT
├── README.md                 # Este arquivo
└── changelog.md              # Histórico de mudanças
```

---

## ❓ FAQ

### Perguntas Gerais

**P: Quantos jogadores por sessão?**  
R: Recomendado 3-6 jogadores. Tecnicamente suporta até 20, mas fica lento.

**P: Posso ter múltiplas sessões simultâneas?**  
R: Sim! Cada sessão é independente com seus próprios canais.

**P: As sessões são salvas?**  
R: Sim, automaticamente a cada 5 minutos e ao encerrar.

**P: Posso retomar uma sessão pausada?**  
R: Sim, use `!pausarsessao` novamente para retomar.

### Problemas Comuns

**P: "Erro ao processar rolagem"**  
R: A IA está usando formato inválido. Isso foi corrigido na v2.5.4.

**P: Botões não aparecem**  
R: Verifique se o bot tem permissão de "Usar Botões" no canal.

**P: "Sessão não encontrada"**  
R: Use o comando dentro do canal da sessão, não no canal geral.

**P: Fichas não aparecem ao selecionar**  
R: Verifique se a ficha tem nome, sistema E conteúdo preenchidos.

### Sistemas de RPG

**P: Quais sistemas são suportados?**  
R: D&D 5e, Call of Cthulhu, Vampire, Shadowrun, FATE, PBtA, Ordem Paranormal, Tormenta20, 3D&T, Old Dragon e mais.

**P: Como mudar o sistema da sessão?**  
R: O sistema é definido pelo mestre com `!sistema <código>` ANTES de criar a sessão.

**P: Posso criar meu próprio sistema?**  
R: Sim! Edite `sistemas_rpg.py` e adicione as regras.

### IA e Narrativa

**P: A IA pode quebrar o jogo?**  
R: Ela segue as regras do sistema configurado. Mestres podem corrigir com `!cenanarrada`.

**P: Posso mudar o estilo durante a sessão?**  
R: Não diretamente. Você precisa criar nova sessão. Use `!pausarsessao` e recrie.

**P: A IA lembra de eventos anteriores?**  
R: Sim, mantém 20 últimas interações no contexto.

---

## 🤝 Contribuindo

### Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch** (`git checkout -b feature/MinhaFeature`)
3. **Commit suas mudanças** (`git commit -m 'Add MinhaFeature'`)
4. **Push para a branch** (`git push origin feature/MinhaFeature`)
5. **Abra um Pull Request**

### Diretrizes

- ✅ Mantenha a modularização
- ✅ Adicione docstrings
- ✅ Teste todas as features
- ✅ Atualize CHANGELOG.md
- ✅ Siga PEP 8

### Áreas para Contribuir

- 🐛 Reportar bugs
- 💡 Sugerir features
- 📖 Melhorar documentação
- 🌍 Traduzir para outros idiomas
- 🎨 Melhorar UI/UX
- 🧪 Adicionar testes

---

## 🙏 Agradecimentos

- **Discord.py** - Framework incrível
- **Groq** - IA rápida e poderosa
- **Comunidade RPG** - Feedback e ideias
- **Contribuidores** - Todos que ajudaram

---

## 📞 Suporte

- 📧 Email: [Gmail](leonardo.dc.work@gmail.com)
- 💬 Discord: [Taverna](https://discord.gg/SdWnWJ6w)
- 🐛 Issues: [GitHub Issues](https://github.com/Leosdc/lyra-the-wise/issues)

---

## 🔮 **Roadmap Futuro**

### 🎯 **Próximas Estruturas de Fichas**
- [ ] Warhammer Fantasy 1e/4e
- [ ] GURPS 4ª Edição
- [ ] Savage Worlds
- [ ] Apocalypse World, Monster of the Week
- [ ] Star Wars (FFG e d20), Star Trek Adventures
- [ ] E mais 30+ sistemas restantes

### 🆕 **Novas Features - Gameplay**
- [ ] Sistema de progressão automática (level up)
  - XP tracking automático
  - Sugestões de escolhas por classe
  - Atualização de fichas via IA

- [ ] Sistema de Economia e Comércio
  - Loja procedural (itens por nível)
  - Preços dinâmicos por região
  - Sistema de crafting básico

- [ ] Sistema de Tempo e Calendário
  - Tracking de passagem do tempo
  - Calendários de sistemas diferentes
  - Eventos sazonais e datas importantes

- [ ] Sistema de Macros Personalizados
  - Comandos customizados por usuário
  - Templates de ações recorrentes
  - Atalhos para combos complexos

### 🎲 **Geração Procedural de Conteúdo**
- [ ] Gerador de Aventuras Completas
  - Plot com 3 atos estruturados
  - Encontros balanceados
  - Recompensas apropriadas
  - NPCs recorrentes

- [ ] Gerador de Masmorras
  - Layout procedural (salas conectadas)
  - Armadilhas e puzzles contextuais
  - Tesouros distribuídos
  - Boss final apropriado

- [ ] Gerador de Locais
  - Tavernas com NPCs únicos
  - Cidades com distritos
  - Vilas e assentamentos
  - Clima e atmosfera

- [ ] Sistema de Tabelas Aleatórias
  - Loot tables por CR/nível
  - Encontros randômicos
  - Eventos climáticos
  - Complicações narrativas

### 🎨 **Interface Visual Avançada**
- [ ] Mapas e Tokens Interativos
  - Upload de mapas customizados
  - Tokens de personagens
  - Fog of War básico

- [ ] Tracker de Iniciativa Visual
  - Ordem visual clara (🥇🥈🥉)
  - HP e condições visíveis
  - Contadores de turno/rodada

- [ ] Dashboard de Estatísticas
  - Progressão da campanha
  - Estatísticas de combate
  - Gráficos de XP e loot
  - Histórico de sessões

### 🔗 **Integrações Externas**
- [ ] VTTs (Virtual Tabletops)
  - Roll20 (sync de fichas)
  - Foundry VTT (export de dados)
  - Owlbear Rodeo (tokens)

- [ ] Gerenciadores de Fichas
  - D&D Beyond (import/export)
  - Pathbuilder 2e (sync)
  - Orcbrew (fichas antigas)

- [ ] Ferramentas de IA
  - Midjourney/DALL-E (retratos de NPCs)
  - Stable Diffusion (mapas visuais)
  - Outras APIs de geração

### 📊 **Expansão de Banco de Dados**
- [ ] Expandir Banco de Monstros
  - 100+ monstros por sistema principal
  - Variantes e templates
  - Monstros customizados salvos

- [ ] Biblioteca de NPCs
  - NPCs recorrentes salvos
  - Relacionamentos entre NPCs
  - Histórico de interações

- [ ] Arquivo de Itens Mágicos
  - Catálogo por sistema
  - Itens customizados
  - Histórico de loot das sessões

### 💾 **Persistência Avançada**
- [ ] Sistema de Salvamento Expandido
  - Salvar encontros gerados
  - Salvar NPCs criados
  - Salvar puzzles/armadilhas
  - Salvar locais visitados
  - Vincular tudo às sessões ativas

- [ ] Exportação Completa
  - Export de campanhas inteiras
  - Formato JSON/XML universal
  - Import de dados externos

### 💾 **Melhoria de Funções e Database Aprimorado para `!sessoes`**
- [ ] !monstro <nome>
- [ ] !encontro <nível> <dificuldade>
- [ ] !armadilha <dificuldade>
- [ ] !cena <descrição>
- [ ] !item <tipo>
- [ ] !tesouro <nível>
- [ ] !puzzle <tema>
- [ ] !vilao <tipo>
- [ ] !nome <tipo>
- [ ] !motivacao

---

### 🎯 Priorização coletada por feedbacks
- [ ] Curto Prazo (1-2 meses)
  - Expandir banco de monstros (impacto imediato)
  - Sistema de tabelas aleatórias (fácil implementar)
  - Gerador de aventuras completas (alto valor)

- [ ] Médio Prazo (3-6 meses)
  - Tracker de iniciativa visual (melhora UX)
  - Sistema de progressão automática (QoL importante)
  - Persistência de conteúdo gerado (salvar monstros/NPCs/itens)

- [ ] Longo Prazo (6-12 meses)
  - Interface visual avançada (complexo)
  - Integrações com VTTs (requer APIs externas)
  - Sistema completo de geração procedural (masmorras, locais, etc)

---

**Feito com ❤️ pela comunidade RPG**

*Transformando Discord em mesas de RPG épicas desde 2025*