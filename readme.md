# 🎲 Lyra, the Wise

Bot completo para Discord focado em RPG de mesa, com suporte a **50+ sistemas**, **IA integrada (Lyra, the Wise)** e **sessões privadas com narrativa contínua**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Groq API](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange.svg)
![Version](https://img.shields.io/badge/Version-v2.5.7-purple.svg)

---

## 🌟 Visão Geral

**Lyra the Wise** é um bot de Discord que transforma seu servidor em uma mesa de RPG completa, com:

- 🤖 **IA Narrativa** - Groq AI gera histórias dinâmicas e contextuais
- 🎲 **Rolagens Interativas** - Sistema de botões para rolagens colaborativas
- 🎭 **Narrativa Adaptativa** - Escolha entre estilo extenso ou conciso
- 🎙️ **Voz Automática** - Canais de voz criados e gerenciados automaticamente
- 📊 **Gestão Completa** - Fichas, iniciativa, histórico e muito mais
- 🔒 **Sessões Privadas** - Canais exclusivos para cada grupo
- 👹 **Geração de conteúdo** - Gera monstros, NPCs, itens, puzzles e muito mais

---

## 📋 **Comandos Principais**

### ⚙️ Configuração
```
!sistema - Ver/mudar sistema atual
!sistema dnd5e - Mudar para D&D 5e
!sistemas - Lista todos os 50+ sistemas
!buscarsistema <nome> - Busca sistemas
!infosistema <código> - Detalhes do sistema
!limpar - Limpa histórico de conversa
```

### 🎲 Dados & Iniciativa
```
!rolar 1d20 ou !r 1d20 - Rola dados
!rolar 2d6+3 - Rola com modificador
!rolar 4d6k3 - Mantém 3 maiores
```

### 👤 Fichas & Personagens
```
!ficha <nome> - Cria ficha automática com IA
!criarficha - Formulário interativo 📝
!verficha / !verficha <nome> - Ver fichas
!editarficha <nome> - Edita ficha ✏️
!deletarficha <nome> - Deleta ficha
!converterficha <sistema> <nome> - Converte ficha
!minhasfichas [sistema] - Lista detalhada
!exportarficha <nome> - Exporta como JSON
```

### ⚔️ Combate & Encontros
```
!monstro <nome> - Cria um monstro
!encontro <nível> <dificuldade> - Gera encontro balanceado
!armadilha <dificuldade> - Cria armadilha
!cena <descrição> - Descreve cena dramaticamente
```

### ✨ Geração de Conteúdo
```
!item <tipo> - Gera item mágico/especial
!tesouro <nível> - Gera tesouro balanceado
!puzzle <tema> - Cria enigma/quebra-cabeça
!vilao <tipo> - Gera vilão completo
!nome <tipo> - Lista 10 nomes criativos
!motivacao - Sorteia motivação para NPC
```

### 🎭 Assistente do Mestre
```
!mestre <pergunta> - Pergunta qualquer coisa
Use para: criar histórias, balancear encontros,
improvisar situações e tirar dúvidas de regras.
💡 Mantém memória da conversa por canal!

📚 Sistemas Suportados
50+ sistemas de RPG disponíveis:
!sistemas ou !listarsistemas - Ver todos
!buscarsistema <nome> - Buscar sistema
!infosistema [código] - Detalhes do sistema

Exemplos populares:
• D&D 5e, 3.5, Pathfinder 1e/2e, 13th Age
• Call of Cthulhu, World of Darkness
• Shadowrun, Cyberpunk, Star Wars
• GURPS, FATE, Savage Worlds
• Blades in the Dark, Dungeon World
```

### 📖 História & Campanha
```
!plot <tema> - Gera ideias de missão/aventura
!sessao <tema> - Planeja sessão completa 📋
!regra <dúvida> - Consulta regras do sistema
```

### 🧠 Administração e Utilidades
```
!stats - Mostra estatísticas do bot
!reload <módulo> - Recarrega partes do bot (admin)
!backup - Cria backup manual dos dados
!documentacao - Exibe documentação completa
!ajuda - Mostra comandos básicos
!suporte - Link de suporte ou contato
```

### 🎬 Sessões e Jogadores
```
!iniciarsessao @Jogador1 @Jogador2 - Cria sessão privada
!sessoes - Lista sessões ativas
!infosessao - Mostra detalhes da sessão
!convidarsessao @Jogador - Adiciona jogador
!removerjogador @Jogador - Remove jogador
```

### 👤 Fichas em Sessão
```
!selecionarficha <nome> - Escolhe ficha
!mudarficha <nome> - Troca personagem
!verficha <nome> - Mostra ficha
!resumosessao - Gera resumo narrativo com IA
```

### ⚙️ Controle e Botões
```
!pausarsessao - Pausa/retoma sessão
!ajudasessao - Guia completo de sessões
```

### 🎬 Botões no canal:
```
• Iniciar Aventura — Introdução épica
• Ver Fichas — Mostra status dos jogadores
• Encerrar Sessão — Deleta canal com confirmação
• Iniciativa — Inicia contagem de iniciativa
```

### 🫂 Ações individuais ou em grupo:
```
• Rolar dados — Rola dados conforme situação da história
• Não fazer nada — Não faz nada naquela ação
• !acao — Descreve uma ação do jogador
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

## 🧩 Estrutura do Projeto
```
lyra-the-wise/
├── main.py
├── config.py
├── commands/
├── admin.py
├── changelog.md
├── documentacao.py
├── fichas_estruturadas.py
├── geracao_conteudo.py
├── help_painel.py
├── monstros_database.py
├── readme.md
├── rpg_core.py
├── sessoes_rpg.py
├── sistemas_comandos.py
├── sistemas_rpg.py
├── utilidades.py
├── utils.py
│   ├── dados.py
│   ├── mestre_ia.py
│   ├── fichas_crud.py
│   ├── fichas_conversao.py
│   ├── fichas_edicao.py
│   ├── geracao_npc.py
│   ├── geracao_mundo.py
│   ├── geracao_combate.py
│   ├── geracao_itens.py
│   ├── sessoes_acao.py
│   └── sessoes_commands.py
├── core/
│   ├── data_manager.py
│   ├── groq_client.py
│   ├── text_utils.py
│   ├── ficha_helpers.py
│   ├── sistemas_helpers.py
│   ├── monstros_helpers.py
│   └── sessao_helpers.py
├── views/
│   ├── ficha_views.py
│   ├── sessao_control_views.py
│   ├── sessao_roll_views.py
│   ├── sessao_continue_views.py
│   └── __init__.py
├── data/
│   ├── sistemas_definicoes.py
│   ├── estruturas_fichas.py
│   ├── monstros_dnd.py
│   ├── monstros_horror.py
│   └── monstros_outros.py
├── requirements.txt
└── LICENSE.txt
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

## 🤝 Contribuições

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
- **Contribuidores** - Todos que ajudaram até aqui

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

---

## 📞 Suporte

- 💬 Discord: [Taverna](https://discord.gg/SdWnWJ6w)
- 🐛 Issues: [GitHub Issues](https://github.com/Leosdc/lyra-the-wise/issues)

---

**Feito com ❤️ para a comunidade de RPG**

*Transformando Discord em mesas de RPG épicas desde 2025*