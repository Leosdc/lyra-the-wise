# 📜 Changelog

## [2.3.0] - 2025-10-26
### ⚔️ Adicionado - Sistema de Ações Interativas
- Novos botões nas rolagens: `🎲 Rolar Dados`, `🚫 Não Fazer Nada`, `✏️ Outra Ação`
- Jogadores agora podem escolher entre agir, ignorar ou realizar outra ação
- IA continua a narrativa automaticamente com base na decisão tomada

### ⚔️ Adicionado - Botão de Iniciativa
- Botão **“⚔️ Rolar Iniciativa”** dentro de “Continuar História”
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
