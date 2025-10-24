# 🎲 RPG Master Bot

Bot completo para Discord focado em RPG de mesa, com suporte a **50+ sistemas**, **IA integrada (Lyra, the Wise)** e **sessões privadas com narrativa contínua**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

⚠️ **Status:** Em desenvolvimento ativo — o bot ainda contém bugs e pode apresentar instabilidades.

---

## ✨ Recursos Principais

- 🤖 **IA Integrada (Lyra, the Wise)** — Gera fichas, NPCs, monstros e narrativas com **Groq (Llama 3.3 70B)**
- 🎮 **50+ Sistemas** — D&D, Pathfinder, Call of Cthulhu, Shadowrun, Vampire e mais
- 🔐 **Sessões Privadas** — Canais isolados com gerenciamento de fichas e botões interativos
- 📖 **Narrativa Contínua** — Sistema `!acao` e `!cenanarrada` com IA contextual
- 🎯 **Sistema por Usuário** — Cada jogador define o próprio sistema
- 👹 **Banco de Monstros** — Dados prontos de múltiplos sistemas
- 🎲 **Sistema de Dados** — Suporte a rolagens complexas (4d6k3, vantagem, etc)
- 💾 **Persistência** — Auto-save e backup automáticos
- 🔄 **Conversão de Fichas** — Migre fichas entre sistemas diferentes

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
!ficha <nome>
!criarficha
!verficha <nome>
!editarficha <nome>
!converterficha <sistema> <nome>
!minhasfichas [sistema]
!exportarficha <nome>
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

## 🎨 **Lyra, the Wise**
A anciã sábia integrada ao bot:

- 🌟 Personalidade calorosa e encorajadora  
- 📚 Conhecimento vasto sobre 50+ sistemas  
- 🎭 Narrativas ricas e imersivas  
- 💡 Conselhos práticos para mestres  
- 🇧🇷 Sempre responde em português do Brasil  

---

## ⚙️ Instalação

### Pré-requisitos
- Python 3.10+  
- Conta no [Discord Developer Portal](https://discord.com/developers/applications)  
- API Key do [Groq](https://console.groq.com)

### Passos
```bash
git clone https://github.com/Leosdc/rpg-master-bot
cd rpg-master-bot
pip install -r requirements.txt
```

Crie o arquivo `.env`:
```
DISCORD_BOT_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_chave_groq_aqui
```

Execute:
```bash
python main.py
```

---

## 🧩 Estrutura do Projeto
```
rpg-master-bot/
├── main.py
├── config.py
├── utils.py
├── sistemas_rpg.py
├── fichas.py
├── sessoes_rpg.py
├── rpg_core.py
├── geracao_conteudo.py
├── monstros_database.py
├── help_painel.py
├── documentacao.py
├── utilidades.py
├── admin.py
├── bot_data/
│   ├── fichas_personagens.json
│   ├── sistemas_usuarios.json
│   └── sessoes_ativas.json
└── README.md
```

---

## 👨‍💻 Autor
**Leosdc_**  
Discord: `Leosdc_`  
GitHub: [@Leosdc](https://github.com/Leosdc)

📜 Licença: **MIT License**  
⭐ Se este projeto te ajudou, dê uma estrela!  
Feito com ❤️ para a comunidade de RPG de mesa.
