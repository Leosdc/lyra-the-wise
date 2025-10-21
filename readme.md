# 🎲 RPG Master Bot

Bot completo para Discord focado em RPG de mesa, com suporte a 50+ sistemas, IA integrada e sessões privadas.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> ⚠️ **Status:** Em desenvolvimento ativo — o bot ainda contém bugs e pode apresentar instabilidades.

## ✨ Recursos Principais

- 🤖 **IA Integrada** - Geração de fichas, NPCs, monstros e narrativas com Groq (Llama 3.3 70B)
- 🎮 **50+ Sistemas** - D&D, Pathfinder, Call of Cthulhu, Shadowrun, Vampire, e muito mais
- 🔐 **Sessões Privadas** - Canais isolados com gerenciamento de fichas e botões interativos
- 👹 **Banco de Dados** - Monstros pré-cadastrados de múltiplos sistemas
- 🎲 **Sistema de Dados** - Suporte a rolagens complexas (4d6k3, vantagem, etc)
- 💾 **Persistência** - Auto-save e backup de dados
- 🔄 **Conversão** - Converta fichas entre diferentes sistemas
- 🧠 **Contexto de Sistema** - Agora, quando o sistema é trocado (`!sistema`), os comandos de IA como `!mestre`, `!npc`, `!plot`, etc, passam a usar automaticamente o sistema definido.

## 📋 Comandos Disponíveis

As funções estão organizadas em quatro páginas principais dentro do Discord:

### 📄 Página 1/4 — Configuração e Fichas
⚙️ **Configuração**
```
!sistema - Ver/mudar sistema atual
!sistema dnd5e - Mudar para D&D 5e
!sistemas - Lista todos os 50+ sistemas
!buscarsistema <nome> - Busca sistemas
!infosistema <código> - Detalhes do sistema
!limpar - Limpa histórico de conversa
```

🎲 **Dados & Iniciativa**
```
!rolar 1d20 ou !r 1d20 - Rola dados
!rolar 2d6+3 - Rola com modificador
!rolar 4d6k3 - Mantém 3 maiores
!iniciativa - Rola iniciativa para o grupo
```

👤 **Fichas & Personagens**
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

### 📄 Página 2/4 — Combate, Geração e Campanha
⚔️ **Combate & Encontros**
```
!monstro <nome> - Busca stats de monstros
!encontro <nível> <dificuldade> - Gera encontro balanceado
!armadilha <dificuldade> - Cria armadilha
!cena <descrição> - Descreve cena dramaticamente
```

✨ **Geração de Conteúdo**
```
!item <tipo> - Gera item mágico/especial
!tesouro <nível> - Gera tesouro balanceado
!puzzle <tema> - Cria enigma/quebra-cabeça
!vilao <tipo> - Gera vilão completo
!nome <tipo> - Lista 10 nomes criativos
!motivacao - Sorteia motivação para NPC
```

📖 **História & Campanha**
```
!plot <tema> - Gera ideias de missão/aventura
!sessao <tema> - Planeja sessão completa 📋
!regra <dúvida> - Consulta regras do sistema
```

### 📄 Página 3/4 — Assistente e Utilidades
🎭 **Assistente do Mestre**
```
!mestre <pergunta> - Pergunta qualquer coisa
```
> Usa o sistema definido pelo comando `!sistema` para adaptar respostas de IA automaticamente.

📚 **Sistemas Suportados**
```
!sistemas - Ver todos os 50+ sistemas
!buscarsistema <nome> - Buscar sistema
!infosistema [código] - Detalhes do sistema
```

🧠 **Administração e Utilidades**
```
!stats - Mostra estatísticas do bot
!reload <módulo> - Recarrega partes do bot (admin)
!backup - Cria backup manual dos dados
!documentacao - Exibe documentação completa
!ajuda - Mostra comandos básicos
!suporte - Link de suporte ou contato
```

### 📄 Página 4/4 — Sessões de RPG
🎬 **Sessões e Jogadores**
```
!iniciarsessao @Jogador1 @Jogador2 - Cria sessão privada
!sessoes - Lista sessões ativas
!infosessao - Mostra detalhes da sessão
!convidarsessao @Jogador - Adiciona jogador
!removerjogador @Jogador - Remove jogador
```

👤 **Fichas em Sessão**
```
!selecionarficha <nome> - Escolhe ficha
!mudarficha <nome> - Troca personagem
!verficha <nome> - Mostra ficha
!resumosessao - Gera resumo narrativo com IA
```

⚙️ **Controle e Botões**
```
!pausarsessao - Pausa/retoma sessão
!ajudasessao - Guia completo de sessões
```
🎬 **Botões no canal:**
- Iniciar Aventura — Introdução épica
- Ver Fichas — Mostra status dos jogadores
- Encerrar Sessão — Deleta canal com confirmação

---

## ⚙️ Instalação

### Pré-requisitos
- Python 3.10+
- Conta no Discord Developer Portal
- API Key do Groq (grátis)

### Passos
```bash
git clone https://github.com/Leosdc/rpg-master-bot
cd rpg-master-bot
pip install -r requirements.txt
```
Crie o arquivo `.env` com:
```env
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
├── comandos/
│   ├── fichas.py
│   ├── sessoes.py
│   ├── sistemas.py
│   ├── combate.py
│   ├── mestre.py
│   └── utilidades.py
├── data/
│   ├── fichas_personagens.json
│   ├── sistemas_rpg.json
│   └── sessoes_ativas.json
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🧠 Observações

- O bot ainda está em **desenvolvimento ativo**, e novos recursos estão sendo adicionados regularmente.
- Funções de IA agora **seguem o sistema definido** pelo usuário, garantindo consistência nas respostas.
- Algumas funções podem falhar em casos específicos; por favor, reporte problemas em [Issues](https://github.com/Leosdc/rpg-master-bot/issues).

---

## 📜 Licença
Licenciado sob a **MIT License**.

## 👨‍💻 Autor
**Leosdc_**
- Discord: Leosdc
- GitHub: [@leosdc](https://github.com/leosdc)

---

⭐ Se este projeto te ajudou, dá uma estrela!
Feito com ❤️ para a comunidade de RPG de mesa.
