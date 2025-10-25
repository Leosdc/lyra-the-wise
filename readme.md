# 🎲 Lyra, the Wise

Bot completo para Discord focado em RPG de mesa, com suporte a **50+ sistemas**, **IA integrada (Lyra, the Wise)** e **sessões privadas com narrativa contínua**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-2.2.0-purple.svg)

⚠️ **Status:** Em desenvolvimento ativo — o bot ainda contém bugs e pode apresentar instabilidades.

---

## ✨ Recursos Principais

- 🤖 **IA Integrada (Lyra, the Wise)** — Gera fichas, NPCs, monstros e narrativas com **Groq (Llama 3.3 70B)**
- 🎮 **50+ Sistemas** — D&D, Pathfinder, Call of Cthulhu, Shadowrun, Vampire e mais
- 🔐 **Sessões Privadas** — Canais isolados com gerenciamento de fichas e botões interativos
- 📖 **Sistema de Estilo Narrativo** — Escolha entre **Narrativa Extensa** ou **Concisa**
- 🎭 **Narrativa Contínua** — Sistema `!acao` e `!cenanarrada` com IA contextual
- 🎯 **Sistema por Usuário** — Cada jogador define o próprio sistema
- 👹 **Banco de Monstros** — Dados prontos de múltiplos sistemas
- 🎲 **Sistema de Dados** — Suporte a rolagens complexas (4d6k3, vantagem, etc)
- 💾 **Persistência** — Auto-save e backup automáticos
- 🔄 **Conversão de Fichas** — Migre fichas entre sistemas diferentes

---

## 🎨 **NOVO: Sistema de Estilo Narrativo**

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

**Como funciona:**
1. Mestre cria sessão com `!iniciarsessao`
2. Jogadores selecionam fichas
3. Mestre clica em **"🎬 Iniciar Aventura"**
4. **NOVO:** Aparece escolha de estilo (Extensa ou Concisa)
5. Lyra inicia a história no estilo escolhido
6. **Todos** os comandos (`!acao`, `!cenanarrada`) seguem o mesmo estilo
7. Estilo é salvo na sessão e mostrado nos footers

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
   - Jogadores: `!criarficha` (criam personagens)

2. **Criação da Sessão:**
   - Mestre: `!iniciarsessao @Jogador1 @Jogador2`
   - Bot cria canal privado automaticamente

3. **Seleção de Fichas:**
   - Cada jogador: `!selecionarficha NomePersonagem`
   - Bot lista fichas disponíveis automaticamente

4. **Início da Aventura:**
   - Mestre clica no botão **"🎬 Iniciar Aventura"**
   - **NOVO:** Escolhe estilo (Extensa ou Concisa)
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
├── sistemas_rpg.py           # Banco de dados de sistemas
├── fichas.py                 # Sistema de fichas
├── sessoes_rpg.py            # Sistema de sessões (com estilo narrativo)
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
├── .env                      # Variáveis de ambiente (não versionado)
├── requirements.txt          # Dependências Python
├── LICENSE                   # Licença MIT
├── README.md                 # Este arquivo
└── changelog.md              # Histórico de mudanças
```

---

## 📜 **Licença**

Este projeto está licenciado sob a **MIT License**:

```
MIT License

Copyright (c) 2025 Leonardo (Leosdc_)

É concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia
deste software e arquivos de documentação associados (o "Software"), para lidar
no Software sem restrições, incluindo, sem limitação, os direitos de usar,
copiar, modificar, fundir, publicar, distribuir, sublicenciar e/ou vender
cópias do Software, e permitir que as pessoas a quem o Software é fornecido
o façam, sujeito às seguintes condições:

O aviso de copyright acima e este aviso de permissão devem ser incluídos em
todas as cópias ou partes substanciais do Software.

O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU
IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO,
ADEQUAÇÃO A UM PROPÓSITO ESPECÍFICO E NÃO VIOLAÇÃO. EM NENHUM CASO OS AUTORES
OU DETENTORES DE DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO,
DANOS OU OUTRA RESPONSABILIDADE, SEJA EM AÇÃO DE CONTRATO, DELITO OU DE OUTRA
FORMA, DECORRENTE DE, FORA DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS
NEGOCIAÇÕES NO SOFTWARE.
```

Ver arquivo [License](https://github.com/Leosdc/lyra-the-wise/blob/main/License.txt) para o texto completo.

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

---

## 👨‍💻 Autor

**Leonardo (Leosdc_)**  
- Discord: `Leosdc_`  
- GitHub: [@Leosdc](https://github.com/Leosdc)

---

## 🙏 **Agradecimentos**

- **Groq** — pela API de IA incrível
- **Discord.py** — pela biblioteca robusta
- **Comunidade de RPG** — pela inspiração e feedback

---

## ☕ **Apoie o Projeto**

Se este bot te ajudou ou você simplesmente quer apoiar o desenvolvimento:

⭐ **Dê uma estrela no GitHub!**  
☕ **[Compre um café para mim](https://ko-fi.com/leosdc)**

---

**Feito com ❤️ para a comunidade de RPG de mesa** 🎲
