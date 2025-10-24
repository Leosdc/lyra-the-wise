# 📜 Changelog

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
