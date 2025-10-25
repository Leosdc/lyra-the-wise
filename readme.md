# 🎲 Lyra, the Wise

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

## 🧩 Estrutura do Projeto
```
lyra-the-wise/
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

⭐ Se este projeto te ajudou, dê uma estrela, ou então, ☕ [compre um café](https://ko-fi.com/leosdc) para mim! 

Feito com ❤️ para a comunidade de RPG de mesa.
