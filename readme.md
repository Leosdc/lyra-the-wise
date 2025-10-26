# 🎲 Lyra, the Wise

Bot completo para Discord focado em RPG de mesa, com suporte a **50+ sistemas**, **IA integrada (Lyra, the Wise)** e **sessões privadas com narrativa contínua**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Groq API](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange.svg)
![Version](https://img.shields.io/badge/Version-v2.5.1-purple.svg)

## 🆕 Atualização — Versão 2.5.0 (2025-10-26)

### 🗂️ Estruturas de Fichas Expandidas
- **9 sistemas com estruturas completas de fichas**:
  - D&D 5e, Pathfinder 2e, Call of Cthulhu 7e
  - Vampire: The Masquerade V5, Shadowrun 5e/6e
  - FATE Core, Dungeon World, Blades in the Dark, Numenera
- Cada sistema possui **campos específicos e autênticos** baseados nas fichas oficiais
- Estruturas totalmente integradas ao sistema de criação com IA
- Sistema genérico como fallback para sistemas não mapeados (ainda suporta todos os 50+ sistemas)

### 🎯 Comando `!ficha` Totalmente Reformulado
- Agora cria fichas **estruturadas por padrão** (não mais formato legado)
- Prompt dinâmico adaptado à estrutura de cada sistema
- Geração automática de exemplo JSON baseado nos campos definidos
- Parser robusto com fallback inteligente por sistema
- **Experiência idêntica para qualquer sistema** - escalável e consistente

### 🧠 IA Mais Inteligente
- Prompts específicos por sistema para preenchimento correto
- Validação automática de campos obrigatórios
- Cálculos corretos de valores derivados (HP, CA, iniciativa, Sanidade, etc)
- História e background mais ricos e coerentes com o sistema

### 🔧 Arquitetura Escalável
- Nova função `get_estrutura_ficha()` em `sistemas_rpg.py`
- Dicionário `ESTRUTURAS_FICHAS` centralizando todas as estruturas
- **Fácil adicionar novos sistemas** - basta adicionar entrada no dicionário
- Separação clara entre dados (sistemas_rpg.py) e lógica (fichas_estruturadas.py)

### 📋 Exemplo de Estruturas
```python
# D&D 5e
Seções: Básico, Atributos, Recursos, Combate, Perícias, 
        Equipamento, Magia, História
Campos: 40+ campos específicos de D&D

# Call of Cthulhu
Seções: Básico, Características, Recursos, Combate, 
        Perícias, Equipamento, História
Campos: FOR, CON, TAM, DES, INT, POD, EDU, SOR, Sanidade, etc

# Vampire V5
Seções: Básico, Atributos, Habilidades, Recursos, 
        Disciplinas, Vantagens, História
Campos: Humanidade, Fome, Potência do Sangue, Convicções, etc
```

---

## 🎙️ **Sistema de Canais de Voz Integrado** (v2.5.1)

Lyra agora gerencia automaticamente canais de voz durante as sessões!

### Funcionalidades:
- ✅ **Criação Automática** - Canal de voz privado criado junto com o canal de texto
- ✅ **Movimentação Inteligente** - Jogadores são movidos automaticamente se já estiverem em voz
- ✅ **Desmute Automático** - Todos são desmutados ao entrar no canal da sessão
- ⚠️ **Avisos Contextuais** - Notificação clara para quem precisa entrar manualmente
- 🔄 **Retorno Seguro** - Ao encerrar, todos voltam para "⚜️Torre da Maga"
- 🗑️ **Limpeza Completa** - Canais de texto e voz excluídos simultaneamente

### Como Funciona:
1. Mestre usa `!iniciarsessao @jogador1 @jogador2`
2. Lyra cria canal de **texto** (`sessao-mestre`) e **voz** (`🎙️ sessao-mestre`)
3. Jogadores conectados em qualquer canal de voz são **movidos automaticamente**
4. Jogadores offline/desconectados recebem **aviso para entrar manualmente**
5. Ao clicar **"🚪 Encerrar Sessão"**, todos retornam para a Torre da Maga
6. Ambos os canais são deletados automaticamente

---

## ✨ Recursos Principais

- 🤖 **IA Integrada (Lyra, the Wise)** — Gera fichas, NPCs, monstros e narrativas com **Groq (Llama 3.3 70B)**
- 🎮 **50+ Sistemas** — D&D, Pathfinder, Call of Cthulhu, Shadowrun, Vampire e mais
- 🗂️ **9 Sistemas com Fichas Completas** — Estruturas autênticas baseadas em fichas oficiais
- 🔐 **Sessões Privadas** — Canais isolados com gerenciamento de fichas e botões interativos
- 📖 **Sistema de Estilo Narrativo** — Escolha entre **Narrativa Extensa** ou **Concisa**
- 🎭 **Narrativa Contínua** — Sistema `!acao` e `!cenanarrada` com IA contextual
- 🎯 **Sistema por Usuário** — Cada jogador define o próprio sistema
- 👹 **Banco de Monstros** — Dados prontos de múltiplos sistemas
- 🎲 **Sistema de Dados** — Suporte a rolagens complexas (4d6k3, vantagem, etc)
- 💾 **Persistência** — Auto-save e backup automáticos
- 🔄 **Conversão de Fichas** — Migre fichas entre sistemas diferentes

---

## 🎨 **Sistema de Estilo Narrativo**

Ao iniciar uma aventura, o mestre pode escolher como Lyra contará a história:

### 📖 **Narrativa Extensa**
- **3-5 parágrafos detalhados**
- **Descrições ricas e imersivas**
- Uso dos 5 sentidos e atmosfera profunda
- **Ideal para:** Roleplay, exploração, drama narrativo
- **Tokens:** 1200-1500 por resposta

### 📝 **Narrativa Concisa**
- **1-2 parágrafos objetivos**
- **Foco em ação e progressão**
- Direto ao ponto, sem perder qualidade
- **Ideal para:** Combate, ritmo acelerado, sessões rápidas
- **Tokens:** 500-600 por resposta

---

## 📋 **Sistemas com Estruturas Completas**

### 🎲 Sistemas Totalmente Mapeados (9 sistemas)
1. **D&D 5ª Edição** - 40+ campos específicos, 18 perícias, sistema de magia completo
2. **Pathfinder 2ª Edição** - Ancestralidade, Heritage, sistema de 3 ações
3. **Call of Cthulhu 7ª Edição** - 9 características, sistema de sanidade
4. **Vampire: The Masquerade V5** - Disciplinas, Humanidade, Fome
5. **Shadowrun 5e/6e** - Cyberware, Magia, Ressonância, Matriz
6. **FATE Core** - Aspectos, Façanhas, Pontos de Destino
7. **Dungeon World** - Movimentos, Vínculos, sistema PbtA
8. **Blades in the Dark** - Ações, Estresse, Trauma, Crew
9. **Numenera** - Pools (Might/Speed/Intellect), Cyphers, Esforço

### 🔮 Sistemas Suportados com Estrutura Genérica (41+ sistemas)
Todos os outros sistemas do bot possuem estrutura genérica funcional e serão expandidos no futuro:
- D&D 3.5, Pathfinder 1e, 13th Age
- Chronicles of Darkness, Werewolf, Mage
- Cyberpunk 2020/RED, Eclipse Phase, Star Trek, Star Wars
- Warhammer Fantasy (1e/4e), GURPS, FATE Accelerated, Savage Worlds
- Apocalypse World, Monster of the Week, 7th Sea, Shadow of the Demon Lord
- Mutants & Masterminds, Champions, Marvel FASERIP
- E mais 20+ sistemas

---

## 📋 **Comandos Principais**

### ⚙️ Configuração
```
!sistema - Ver seu sistema atual
!sistema <código> - Mudar sistema pessoal
!sistemas - Lista todos os sistemas
!buscarsistema <nome> - Buscar sistemas
!infosistema <código> - Detalhes do sistema
```

### 🎲 Dados & Iniciativa
```
!rolar 1d20
!rolar 2d6+3
!iniciativa
```

### 👤 Fichas & Personagens
```
!ficha <nome> - Criação rápida estruturada
!criarficha - Modo interativo com 8 perguntas
!verficha <nome> - Ver com navegação por páginas
!editarficha <nome> - Editor interativo
!converterficha <sistema> <nome> - Converte entre sistemas
!minhasfichas [sistema] - Lista suas fichas
!exportarficha <nome> - Exporta como JSON
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

## 🚀 **Instalação e Configuração**

### Pré-requisitos
- Python 3.10+
- Conta Discord Developer (bot token)
- Chave API do Groq

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/Leosdc/lyra-the-wise.git
cd lyra-the-wise
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_BOT_TOKEN=seu_token_discord_aqui
GROQ_API_KEY=sua_chave_groq_aqui
```

4. **Execute o bot:**
```bash
python main.py
```

5. **Convide o bot para seu servidor:**
- Acesse o Discord Developer Portal
- Copie o link de convite com permissões de:
  - Gerenciar Canais
  - Ler/Enviar Mensagens
  - Adicionar Reações
  - Usar Comandos

---

## 🎯 **Fluxo Completo de uma Sessão**

1. **Preparação:**
   - Mestre: `!sistema dnd5e` (configura sistema)
   - Jogadores: `!criarficha` ou `!ficha <nome>` (criam personagens)

2. **Criação da Sessão:**
   - Mestre: `!iniciarsessao @Jogador1 @Jogador2`
   - Bot cria canal privado automaticamente

3. **Seleção de Fichas:**
   - Cada jogador: `!selecionarficha NomePersonagem`
   - Bot lista fichas disponíveis automaticamente

4. **Início da Aventura:**
   - Mestre clica no botão **"🎬 Iniciar Aventura"**
   - Escolhe estilo (Extensa ou Concisa)
   - Lyra gera introdução épica personalizada

5. **Durante o Jogo:**
   - Jogadores: `!acao escalo a parede`
   - Mestre: `!cenanarrada dragão pousa na torre`
   - Bot gera narrativa no estilo escolhido
   - Sistema de rolagens interativas (quando solicitado)

6. **Encerramento:**
   - Mestre: `!resumosessao` (gera resumo com IA)
   - Mestre clica **"🚪 Encerrar Sessão"**

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
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências Python
├── LICENSE                   # Licença MIT
├── README.md                 # Este arquivo
└── changelog.md              # Histórico de mudanças
```

---

## 🔮 **Roadmap Futuro**

### Próximas Estruturas de Fichas
- [ ] Warhammer Fantasy 1e/4e
- [ ] GURPS 4ª Edição
- [ ] Savage Worlds
- [ ] Apocalypse World
- [ ] Monster of the Week
- [ ] Star Wars (FFG e d20)
- [ ] Star Trek Adventures
- [ ] E mais 30+ sistemas

### Novas Features
- [ ] Sistema de progressão automática (level up)
- [ ] Gerador de aventuras completas
- [ ] Mapas e tokens visuais
- [ ] Integração com Roll20/Foundry VTT
- [ ] Sistema de economia e comércio
- [ ] Calendários e tracking de tempo

---

## 🤝 **Contribuindo**

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

**Diretrizes:**
- Siga o estilo de código existente
- Adicione testes quando aplicável
- Atualize a documentação conforme necessário
- Seja descritivo nos commits

**Especialmente bem-vindos:**
- Novas estruturas de fichas para sistemas não mapeados
- Melhorias nos prompts de IA
- Traduções da documentação
- Correções de bugs

---

## 👨‍💻 Autor

**Leonardo (Leosdc_)**  
- Discord: `Leosdc_`  
- Canal do Discord: [Taverna](https://discord.gg/SdWnWJ6w)
- GitHub: [@Leosdc](https://github.com/Leosdc)

---

## 🙏 **Agradecimentos**

- **Groq** — pela API de IA incrível
- **Discord.py** — pela biblioteca robusta
- **Comunidade de RPG** — pela inspiração e feedback
- **Contribuidores** — por ajudarem a expandir as estruturas de fichas

---

## ☕ **Apoie o Projeto**

Se este bot te ajudou ou você simplesmente quer apoiar o desenvolvimento:

⭐ **Dê uma estrela no GitHub!**  
☕ **[Compre um café para mim](https://ko-fi.com/leosdc)**  
💬 **Entre no nosso Discord**: [Taverna](https://discord.gg/SdWnWJ6w)

---

**Feito com ❤️ para a comunidade de RPG de mesa** 🎲