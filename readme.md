# 🎲 RPG Master Bot

Bot completo para **Discord** focado em **RPG de mesa**, com suporte a **50+ sistemas**, **IA narrativa com Groq**, fichas, sessões e rolagens avançadas.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Recursos Principais

- 🤖 **IA Integrada (Groq - Llama 3.3 70B)**  
  Mestre virtual “**Lyra the Wise**” com estilo narrativo dinâmico — adapta tom, ambientação e regras conforme o sistema ativo (`!sistema`).

- 🎮 **50+ Sistemas Suportados**  
  D&D, Pathfinder, Call of Cthulhu, Shadowrun, Vampire, FATE, Iron Kingdoms, GURPS e muito mais.

- 🧙‍♀️ **Mestre Inteligente**  
  Comandos `!mestre`, `!plot`, `!regra` e outros ajustam o comportamento da IA ao sistema selecionado (fantasia, horror, sci-fi, etc).

- 🔐 **Sessões Privadas**  
  Canais exclusivos com gerenciamento de fichas e botões interativos.

- 👹 **Banco de Dados**  
  Monstros, NPCs e vilões pré-cadastrados com geração inteligente.

- 🎲 **Sistema de Rolagens Avançado**  
  Suporte a expressões como `4d6k3`, bônus e desvantagem.

- 💾 **Persistência Automática**  
  Auto-save periódico dos dados (fichas, sistemas e sessões).

---

## 📋 Comandos Principais

### 🔧 Configuração
- `!sistema <nome>` → muda o sistema ativo (ex: `!sistema cthulhu`)
- `!limpar` → limpa o histórico de conversa no canal

### 🎭 Mestre (IA)
- `!mestre <mensagem>` → conversa com o Mestre no estilo do sistema atual  
- `!plot <tema>` → gera uma aventura adaptada  
- `!regra <dúvida>` → explica regras conforme o sistema ativo  

### 🎲 Rolagens
- `!rolar 2d6+3` → rola dados com modificadores  
- `!iniciativa` → rola iniciativa para todos no canal de voz  

### 👤 Fichas
- `!ficha <nome>` → cria ficha de personagem  
- `!verficha <nome>` → exibe ficha  

> 💡 Use `!rpghelp` no Discord para ver a lista completa.

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.10+
- Conta no [Discord Developer Portal](https://discord.com/developers/applications)
- [Groq API Key](https://console.groq.com/) (grátis)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/Leosdc/rpg-master-bot.git
cd rpg-master-bot

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
echo DISCORD_BOT_TOKEN=seu_token_aqui > .env
echo GROQ_API_KEY=sua_chave_groq_aqui >> .env

# 4. Execute o bot
python main.py
```

---

## 📁 Estrutura do Projeto

```
rpg-master-bot/
├── main.py                 # Arquivo principal
├── config.py               # Configurações globais
├── utils.py                # Funções e prompts narrativos
├── rpg_core.py             # Núcleo principal (dados, IA, mestre)
├── sistemas_rpg.py         # Banco de sistemas
├── sistemas_comandos.py    # Comandos de seleção de sistema
├── fichas.py               # Sistema de fichas
├── sessoes_rpg.py          # Sessões privadas
├── geracao_conteudo.py     # Geração de NPCs, monstros e itens
├── monstros_database.py    # Base de monstros
├── help_painel.py          # Painel de ajuda interativo
├── documentacao.py         # Documentação embutida
├── utilidades.py           # Funções diversas
├── admin.py                # Comandos administrativos
└── bot_data/               # Dados persistentes
    ├── fichas_personagens.json
    ├── sistemas_rpg.json
    └── sessoes_ativas.json
```

---

## 🧠 Exemplo de Uso

### 🎮 Alternar Sistema e Jogar
```bash
!sistema cthulhu
!mestre descreva a atmosfera de uma mansão abandonada
```

### ⚙️ Criar Personagem
```bash
!sistema dnd5e
!ficha Aragorn
!verficha Aragorn
```

### ⚔️ Rolagens
```bash
!rolar 1d20+5
!iniciativa
```

### 👹 Geração
```bash
!npc mercador suspeito
!vilao necromante
!item espada flamejante
```

---

## 🧩 Sistemas Suportados

| Gênero | Exemplos |
|--------|-----------|
| **Fantasia** | D&D 5e • Pathfinder • 13th Age • Iron Kingdoms |
| **Horror** | Call of Cthulhu • Vampire: The Masquerade • Mage • Kult |
| **Ficção Científica** | Shadowrun • Cyberpunk RED • Starfinder • Eclipse Phase |
| **Genéricos** | GURPS • FATE • Savage Worlds • Cortex Prime |
| **Outros** | Apocalypse World • Blades in the Dark • 7th Sea • Exalted |

> 🧠 A Lyra adapta o estilo narrativo automaticamente para qualquer sistema reconhecido — e até para novos, não listados!

---

## 🤝 Contribuindo

1. Fork o projeto  
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)  
3. Commit suas mudanças (`git commit -m 'feat: nova funcionalidade'`)  
4. Push (`git push origin feature/NovaFuncionalidade`)  
5. Abra um Pull Request  

### 🧟 Adicionando novos sistemas
Edite `sistemas_rpg.py` e adicione no dicionário `SISTEMAS_DISPONIVEIS`.  
A Lyra reconhecerá automaticamente o novo sistema com estilo narrativo próprio.

---

## 📝 To-Do

- [ ] Tracker de HP e recursos  
- [ ] Macros de combate personalizadas  
- [ ] Geração procedural de mapas  
- [ ] Integração com Roll20 / Foundry  
- [ ] Dashboard web de administração  

---

## 🐛 Bugs Conhecidos
Nenhum crítico no momento.  
Reportes: [Issues](https://github.com/Leosdc/rpg-master-bot/issues)

---

## 📜 Licença
Este projeto está sob a licença **MIT**.  
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Leosdc_**  
- Discord: `leosdc`  
- GitHub: [@Leosdc](https://github.com/Leosdc)

---

## 🙏 Agradecimentos
- [Discord.py](https://github.com/Rapptz/discord.py)  
- [Groq](https://groq.com/)  
- Comunidade de RPG do Brasil 🇧🇷  

---

⭐ Se este projeto te ajudou, considere **dar uma estrela** no repositório!  
*Feito com ❤️ e dados críticos pela comunidade de RPG de mesa.*
