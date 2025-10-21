# 🎲 RPG Master Bot

Bot completo para Discord focado em RPG de mesa, com suporte a 50+ sistemas, IA integrada e sessões privadas.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Recursos Principais

- 🤖 **IA Integrada** - Geração de fichas, NPCs, monstros e narrativas com Groq (Llama 3.3 70B)
- 🎮 **50+ Sistemas** - D&D, Pathfinder, Call of Cthulhu, Shadowrun, Vampire, e muito mais
- 🔐 **Sessões Privadas** - Canais isolados com gerenciamento de fichas e botões interativos
- 👹 **Banco de Dados** - Monstros pré-cadastrados de múltiplos sistemas
- 🎲 **Sistema de Dados** - Suporte a rolagens complexas (4d6k3, vantagem, etc)
- 💾 **Persistência** - Auto-save e backup de dados
- 🔄 **Conversão** - Converta fichas entre diferentes sistemas

## 📋 Comandos Disponíveis

### Categorias
- ⚙️ **Configuração** (5 comandos) - Gerenciar sistemas de RPG
- 🎲 **Dados** (2 comandos) - Rolagens e iniciativa
- 👤 **Fichas** (7 comandos) - Criar e gerenciar personagens
- 🎮 **Sessões** (9 comandos) - Campanhas privadas
- 👹 **Monstros** (3 comandos) - Banco de dados + geração com IA
- ⚔️ **Combate** (2 comandos) - Encontros e armadilhas
- ✨ **Geração** (6 comandos) - Itens, puzzles, vilões
- 🎭 **Mestre IA** (4 comandos) - Assistente inteligente
- 📚 **Ajuda** (5 comandos) - Documentação
- 🔧 **Admin** (5 comandos) - Administração do bot

**Total: 50 comandos**

Use `!rpghelp` no Discord para ver todos os comandos organizados!

## 🚀 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- Conta no Discord Developer Portal
- API Key do Groq (grátis)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/rpg-master-bot.git
cd rpg-master-bot
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_BOT_TOKEN=seu_token_do_discord_aqui
GROQ_API_KEY=sua_chave_groq_aqui
```

4. **Execute o bot**
```bash
python main.py
```

## 🔑 Obtendo as Chaves

### Discord Bot Token
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma "New Application"
3. Vá em "Bot" → "Add Bot"
4. Copie o Token
5. Em "Privileged Gateway Intents", ative:
   - ✅ Message Content Intent
   - ✅ Server Members Intent

### Groq API Key
1. Acesse [Groq Console](https://console.groq.com/)
2. Crie uma conta (grátis)
3. Vá em "API Keys"
4. Crie uma nova chave
5. Copie e salve (não será mostrada novamente!)

## 📁 Estrutura do Projeto

```
rpg-master-bot/
├── main.py                    # Arquivo principal
├── config.py                  # Configurações globais
├── utils.py                   # Funções auxiliares
├── sistemas_rpg.py            # Banco de dados de sistemas
├── monstros_database.py       # Banco de dados de monstros
├── rpg_core.py                # Comandos principais
├── fichas.py                  # Sistema de fichas
├── sistemas_comandos.py       # Comandos de sistemas
├── geracao_conteudo.py        # Geração de NPCs, itens, etc
├── sessoes_rpg.py             # Sistema de sessões
├── help_painel.py             # Painel de ajuda
├── documentacao.py            # Documentação
├── utilidades.py              # Utilitários
├── admin.py                   # Comandos administrativos
├── requirements.txt           # Dependências
├── .env                       # Variáveis de ambiente (NÃO SUBIR)
├── .gitignore                 # Arquivos a ignorar
├── README.md                  # Este arquivo
└── bot_data/                  # Dados salvos (NÃO SUBIR)
    ├── fichas_personagens.json
    ├── sistemas_rpg.json
    └── sessoes_ativas.json
```

## 🎯 Exemplos de Uso

### Criar Personagem
```
!sistema dnd5e
!ficha Aragorn
!verficha Aragorn
```

### Iniciar Sessão
```
!iniciarsessao @Jogador1 @Jogador2
# [No canal privado]
!selecionarficha MeuPersonagem
# [Mestre clica em "Iniciar Aventura"]
```

### Gerar Conteúdo
```
!monstro goblin
!npc mercador suspeito
!vilao necromante
!item espada mágica
!encontro 5 medio
```

### Rolar Dados
```
!rolar 1d20+5
!rolar 4d6k3
!iniciativa
```

## 🎲 Sistemas Suportados

### D&D e Derivados
D&D 5e • D&D 3.5 • Pathfinder 1e/2e • 13th Age • Microlite20

### Horror
Call of Cthulhu • Vampire: The Masquerade • Werewolf • Mage

### Ficção Científica
Shadowrun • Cyberpunk 2020/RED • Eclipse Phase • Star Wars • Star Trek

### Genéricos
GURPS • FATE Core/Accelerated • Savage Worlds • Cortex Prime

### Outros
Warhammer Fantasy • Apocalypse World • Dungeon World • Blades in the Dark • 7th Sea • Mutants & Masterminds • Exalted • e mais!

**Total: 50+ sistemas**

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Adicionando Monstros
Edite `monstros_database.py` e adicione novos monstros seguindo o formato existente.

### Adicionando Sistemas
Edite `sistemas_rpg.py` e adicione o novo sistema no dicionário `SISTEMAS_DISPONIVEIS`.

## 📝 To-Do

- [ ] Sistema de iniciativa integrado nas sessões
- [ ] Tracker de HP/recursos
- [ ] Mais monstros no banco de dados
- [ ] Geração de mapas com ASCII art
- [ ] Sistema de macros personalizados
- [ ] Integração com Roll20/Foundry
- [ ] Dashboard web para gerenciar o bot

## 🐛 Bugs Conhecidos

Nenhum no momento! Reporte em [Issues](https://github.com/seu-usuario/rpg-master-bot/issues)

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Leosdc_**
- Discord: leosdc
- GitHub: [@leosdc](https://github.com/leosdc)

## 🙏 Agradecimentos

- [Discord.py](https://github.com/Rapptz/discord.py) - Framework do bot
- [Groq](https://groq.com/) - API de IA
- Comunidade RPG brasileira

---

⭐ Se este projeto te ajudou, considere dar uma estrela!

*Feito com ❤️ para a comunidade de RPG de mesa*
