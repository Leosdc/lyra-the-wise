# 📜 Changelog

## [2.5.2] - 2025-10-26
### 🛡️ Melhorado - Comandos de ajuda enviados por DM
- **help_painel.py - !rpghelp** → DM
- **documentacao.py - !documentacao** → DM
- **utilidades.py - !ajuda** → DM
- **utilidades.py - !suporte** → DM
- **utilidades.py - !sobre → DM**
- **sistemas_comandos.py - !sistemas** → DM
- **sistemas_comandos.py - !buscarsistema** → DM
- **sistemas_comandos.py - !infosistema** → DM

---

## [2.5.1] - 2025-10-26
### 🎙️ Adicionado - Sistema de Canais de Voz Integrado
- **Criação automática de canal de voz** ao iniciar sessão com `!iniciarsessao`
- **Movimentação automática** de jogadores para o canal de voz da sessão
- **Desmute automático** ao entrar no canal de voz
- **Avisos inteligentes** para jogadores que não estão em canais de voz
- **Retorno automático** para "⚜️Torre da Maga" ao encerrar sessão
- Canais de voz e texto são excluídos simultaneamente ao finalizar

### 🎯 Melhorado - Experiência de Sessão
- Feedback visual sobre quem foi movido para o canal de voz
- Notificações claras para jogadores que precisam entrar manualmente
- Mensagens de boas-vindas destacando o canal de voz criado
- Busca flexível do canal "Torre da Maga" (aceita variações do nome)

### 🔧 Arquitetura
- Função `_criar_canal_de_sessao` agora retorna tupla `(TextChannel, VoiceChannel)`
- Campo `voice_channel_id` adicionado à estrutura de sessões
- Lógica de movimentação com tratamento robusto de exceções
- Logs detalhados de movimentação de jogadores

### 🎮 Fluxo Completo
1. Mestre cria sessão → Canais texto + voz criados
2. Jogadores em voz → Movidos automaticamente + desmutados
3. Jogadores fora de voz → Recebem aviso para entrar manualmente
4. Fim da sessão → Todos retornam para Torre da Maga → Canais deletados

---

## [2.5.0] - 2025-10-26
### 🗂️ Adicionado - Estruturas de Fichas Expandidas
- **9 sistemas com estruturas completas de fichas**:
  - D&D 5e, Pathfinder 2e, Call of Cthulhu 7e
  - Vampire: The Masquerade V5, Shadowrun 5e/6e
  - FATE Core, Dungeon World, Blades in the Dark, Numenera
- Cada sistema possui **campos específicos e autênticos**
- Estruturas baseadas em fichas oficiais dos sistemas
- Sistema genérico como fallback para sistemas não mapeados

### 🎯 Melhorado - Comando `!ficha`
- Agora cria fichas **estruturadas por padrão** (não mais formato legado)
- Prompt dinâmico adaptado à estrutura de cada sistema
- Geração automática de exemplo JSON baseado nos campos do sistema
- Parser robusto com fallback inteligente por sistema
- Compatível com todos os 50+ sistemas suportados

### 🧠 IA Mais Inteligente
- Prompts específicos por sistema para melhor preenchimento
- Validação automática de campos obrigatórios
- Cálculos corretos de valores derivados (HP, CA, iniciativa, etc)
- História e background mais ricos e coerentes

### 🔧 Arquitetura
- Nova função `get_estrutura_ficha()` em `sistemas_rpg.py`
- Dicionário `ESTRUTURAS_FICHAS` centralizando todas as estruturas
- Sistema escalável - fácil adicionar novos sistemas no futuro
- Separação clara entre dados (sistemas_rpg.py) e lógica (fichas_estruturadas.py)

### 📋 Próximos Sistemas
Estruturas em desenvolvimento para:
- Warhammer Fantasy, GURPS, Savage Worlds
- Apocalypse World, Monster of the Week
- Star Wars (FFG e d20), Star Trek Adventures
- E mais 30+ sistemas restantes

---

## [2.4.0] - 2025-10-25
### 📋 Adicionado - Sistema de Fichas Estruturadas
- Fichas agora são **totalmente estruturadas e organizadas em páginas navegáveis**
- Cada sistema (D&D 5e, Pathfinder 2e, Cthulhu, Shadowrun, Vampire V5, etc.) possui **campos e recursos próprios**
- Inclusão de atributos específicos:
  - D&D: HP, MP, Dados de Vida, Espaços de Magia
  - Cthulhu: Sanidade Máxima/Atual, Magia, Movimento
  - Shadowrun: Essência, Magia, Ressonância
  - Vampire: Humanidade, Fome, Pontos de Sangue
- Visualização interativa com botões:
  - `◀️ Anterior`, `▶️ Próxima`, `❌ Fechar`
- Compatível com fichas antigas (legado) e novo formato 📋 estruturado

### 🧠 IA Aprimorada - Fichas Mais Completas
- `!criarficha` agora faz **8 perguntas detalhadas**
- Prompt reescrito para **forçar preenchimento de todos os campos**
- IA expande e enriquece as respostas do jogador
- Tokens aumentados de 2000 → **2500**
- Parser JSON robusto com fallback inteligente (nunca retorna vazio)

### 🧩 Novo - Comando `!converterficha`
- Permite converter fichas entre sistemas mantendo equilíbrio e contexto narrativo
- Detecta automaticamente formato (texto ou estruturado)
- Converte atributos e recursos para o novo sistema mantendo proporções

### 💾 Melhorado - Persistência e Encoding
- Salvamento forçado com **UTF-8 seguro**
- Correção automática de campos com encoding corrompido (ex: "raÃ§a" → "raça")
- Recuperação automática de fichas quebradas
- Logs detalhados no console para debugging

### ⚙️ Compatibilidade Total
- Todos os comandos existentes continuam funcionais:
- `!criarficha`, `!verficha`, `!editarficha`, `!minhasfichas`, `!exportarficha`, `!converterficha`
- Fichas antigas (legado) continuam sendo lidas e listadas normalmente
- Indicador visual 📋 (estruturada) ou 📄 (legado)

### 🧠 Experiência do Usuário
- Feedback de criação mostrando **percentual de completude**
- Dicas contextuais sugerindo `!editarficha` se <70%
- Exibição mais limpa e legível, página por página

---

## [2.3.0] - 2025-10-26
### ⚔️ Adicionado - Sistema de Ações Interativas
- Novos botões nas rolagens: `🎲 Rolar Dados`, `🚫 Não Fazer Nada`, `✏️ Outra Ação`
- Jogadores agora podem escolher entre agir, ignorar ou realizar outra ação
- IA continua a narrativa automaticamente com base na decisão tomada

### ⚔️ Adicionado - Botão de Iniciativa
- Botão **"⚔️ Rolar Iniciativa"** dentro de "Continuar História"
- Exclusivo para o mestre
- Define automaticamente a ordem de ação dos jogadores (🥇🥈🥉)
- Resultado registrado no histórico da IA

### ✍️ Melhorado - Estilo Narrativo Conciso
- Redução de tokens para 350–400
- Agora limitado a **1 parágrafo curto (máx. 4–5 frases)**
- Linguagem objetiva e direta, ideal para combate e ritmo rápido

### 📘 Atualizado - Comando `!ajudasessao`
- Novo guia completo cobrindo todos os botões e fluxos de sessão
- Explicações detalhadas dos estilos narrativos
- Exemplo completo de partida com todas as features

### 🧠 Qualidade de Vida
- Feedback visual aprimorado nos botões
- Consistência de tom entre estilos Extenso e Conciso
- Salvamento automático mantido a cada 5 minutos

---

## [2.2.0] - 2025-10-26
### 🎨 Adicionado - Sistema de Estilo Narrativo
- **Escolha de Estilo ao Iniciar Aventura**: Mestre escolhe entre Narrativa Extensa ou Concisa
- **📖 Narrativa Extensa**: 
  - 3-5 parágrafos completos e detalhados
  - Descrições ricas dos 5 sentidos
  - Atmosfera cinematográfica e imersiva
  - 1200-1500 tokens por resposta
  - Ideal para sessões focadas em roleplay
- **📝 Narrativa Concisa**:
  - 1-2 parágrafos curtos e objetivos
  - Foco em ação e informação essencial
  - Ritmo ágil e dinâmico
  - 500-600 tokens por resposta
  - Ideal para combate e progressão rápida
- Estilo aplicado automaticamente em `!acao` e `!cenanarrada`
- Footer visual mostrando estilo ativo (EXTENSO/CONCISO)
- Sistema de rolagens interativas respeitando o estilo escolhido

### 🎲 Melhorado - Sistema de Rolagens
- Rolagens automáticas agora respeitam o estilo narrativo
- Narrativa pós-rolagem adapta tamanho conforme configuração
- Melhor integração entre dados e história contínua

### 🎭 Interno
- Refatoração da classe `NarrativeStyleView`
- Parâmetros dinâmicos de tokens baseados em estilo
- Consistência de tom narrativo em toda a sessão

---

## [2.1.0] - 2025-10-23
### 🎭 Adicionado - Sistema de Narrativa Contínua
- `!acao`: Jogadores descrevem ações, IA narra consequências com contexto contínuo.
- `!cenanarrada`: Mestre narra cenas expandidas cinematograficamente pela IA.
- `!rolar dados`: Mestre solicita que os dados sejam lançados por todos os participantes, tornando a aventura ainda mais emocionante.
- Histórico de 20 interações por sessão para manter coerência narrativa.
- Botão **"Continuar História"** para fluidez da aventura.

### 👤 Adicionado - Sistema por Usuário
- Cada usuário possui seu próprio sistema configurado via `!sistema`.
- Comandos de IA (`!mestre`, `!ficha`, `!npc`, etc.) usam o sistema do jogador.
- Sessões utilizam o sistema do mestre como referência.

### 📝 Adicionado - Melhorias em Fichas
- `!criarficha`: Formulário interativo com 5 perguntas guiadas.
- `!editarficha`: Editor interativo com 4 opções de edição.
- Busca exata e salvamento forçado após cada operação.

### 🔧 Corrigido
- `!deletarficha`: agora busca exata, sem apagar fichas erradas.
- Persistência garantida via `salvar_fichas_agora()`.
- Recarregamento de dados antes de listar fichas.

### 🎨 Melhorado
- Lyra agora tem personalidade definida e tom narrativo imersivo.
- Respostas longas divididas automaticamente em partes.
- Aumento dos tokens máximos de geração.
- Feedback visual aprimorado (mensagens de "gerando...", cores e dicas).

### 📚 Atualizado
- `!rpghelp`, `!documentacao`, `!ajudasessao` revisados com exemplos do novo sistema narrativo.

### 🔧 Interno
- Refatoração de imports e estados centralizados em `config.py`.
- Debug logging aprimorado e validações mais robustas.

---

## [2.0.0] - 2025-10-21
### Adicionado
- Integração com **Groq (Llama 3.3 70B)** para geração de conteúdo com IA.
- Banco de dados com 15+ monstros pré-cadastrados.
- 50+ sistemas de RPG suportados.
- Sessões privadas com canais dedicados.
- Auto-save e comando `!backup`.
- 50 comandos funcionais organizados.

### Corrigido
- Bugs na criação e persistência de fichas.
- Problemas em chamadas à API Groq.

### Melhorado
- Interface reorganizada com help interativo.
- Documentação completa integrada.