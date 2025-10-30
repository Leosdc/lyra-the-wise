# documentacao.py — versão final com prevenção de duplicata
import discord
from discord.ext import commands

DOCUMENTACAO_COMPLETA = """📘 Lyra The Wise - Documentação Completa
🎲 Visão Geral
Bot completo para gerenciamento de mesas de RPG no Discord, com suporte a 50+ sistemas, IA integrada, geração de conteúdo e sessões privadas.

📋 Lista Completa de Comandos (50 comandos)

⚙️ Configuração e Sistemas (5 comandos)
•	!sistema [código] - Ver ou mudar sistema de RPG do canal
•	!sistemas - Lista todos os 50+ sistemas disponíveis
•	!buscarsistema <termo> - Busca sistemas por nome
•	!infosistema <código> - Detalhes completos de um sistema
•	!limpar - Limpa histórico de conversa do canal

🎲 Dados e Rolagens (2 comandos)
•	!rolar <expressão> ou !r <expressão> - Rola dados (2d6+3, 4d6k3, etc)
•	!iniciativa - Rola iniciativa para grupo no canal de voz

👤 Fichas de Personagem (7 comandos)
•	!ficha <nome> - Cria ficha automática com IA
•	!minhasfichas [sistema] - Lista suas fichas
•	!verficha <nome> - Visualiza ficha específica
•	!editarficha <nome> - Edita ficha (se implementado)
•	!deletarficha <nome> - Deleta ficha permanentemente
•	!converterficha <sistema> <nome> - Converte ficha entre sistemas
•	!exportarficha <nome> - Exporta ficha como JSON

🎮 Sessões de RPG (9 comandos)
•	!iniciarsessao @jogador1 @jogador2 - Cria sessão privada
•	!sessoes - Lista sessões ativas do servidor
•	!infosessao - Detalhes da sessão atual
•	!convidarsessao @jogador - Adiciona jogador à sessão
•	!removerjogador @jogador - Remove jogador da sessão
•	!selecionarficha <nome> - Escolhe ficha para sessão
•	!mudarficha <nome> - Troca de personagem (requer aprovação)
•	!pausarsessao - Pausa/retoma sessão
•	!resumosessao - Gera resumo narrativo com IA
•	!ajudasessao - Guia completo de sessões

👹 Monstros e NPCs (3 comandos)
•	!monstro [nome] - Busca no banco ou gera monstro com IA
•	!monstros - Lista monstros disponíveis para o sistema
•	!npc [descrição] - Gera NPC completo

⚔️ Combate e Encontros (2 comandos)
•	!encontro [nível] [dificuldade] - Gera encontro balanceado
•	!armadilha [dificuldade] - Cria armadilha criativa

✨ Geração de Conteúdo (6 comandos)
•	!item [tipo] - Gera item mágico/especial
•	!tesouro [nível] - Gera tesouro balanceado
•	!puzzle [tema] - Cria enigma/quebra-cabeça
•	!vilao [tipo] - Gera vilão completo
•	!cena <descrição> - Descreve cena dramaticamente
•	!nome <tipo> - Lista 10 nomes criativos

🎭 Assistente do Mestre (3 comandos)
•	!mestre <pergunta> - Assistente de IA contextual
•	!plot <tema> - Gera ideia de missão/aventura
•	!regra <dúvida> - Consulta regras do sistema
•	!motivacao - Sorteia motivação aleatória para NPC

📚 Ajuda e Documentação (5 comandos)
•	!rpghelp - Painel completo com navegação (4 páginas)
•	!documentacao - Documentação detalhada do bot
•	!ajuda - Comandos básicos e início rápido
•	!suporte - Informações de contato e suporte
•	!sobre - Informações sobre o bot

🔧 Administração (5 comandos)
•	!stats - Estatísticas do bot (CPU, memória, uptime)
•	!backup - Cria backup manual 🔒 (apenas dono)
•	!reload <módulo> - Recarrega módulo 🔒 (apenas dono)
•	!troubleshoot - Diagnóstico de comandos 🔒 (apenas dono)

🧪 Debug e Testes (2 comandos)
•	!ping - Testa latência do bot
•	!testegroq - Testa conexão com API Groq

🚀 Guia de Uso Rápido

Configuração Inicial

✨ Ver sistema atual
!sistema

✨ Mudar para D&D 5e
!sistema dnd5e

✨ Ver todos os sistemas
!sistemas

✨ Buscar sistema específico
!buscarsistema pathfinder

Criar Personagem

✨ Criar ficha automática com IA
!ficha Aragorn

✨ Ver suas fichas
!minhasfichas

✨ Ver ficha específica
!verficha Aragorn

✨ Converter para outro sistema
!converterficha pathfinder Aragorn

✨ Exportar como JSON
!exportarficha Aragorn

Iniciar Sessão

✨ Criar sessão privada
!iniciarsessao @Alice @Bob @Carol

✨ [No canal privado] Cada jogador escolhe ficha
!selecionarficha Elara

✨ [Mestre] Clica no botão "🎬 Iniciar Aventura"
✨ Bot gera introdução épica com IA

✨ Durante o jogo
!rolar 1d20+5
!mestre como resolver esta situação?

✨ Fim da sessão
!resumosessao

✨ [Mestre] Clica em "🚪 Encerrar Sessão"
Gerar Conteúdo

✨ Monstro do banco de dados
!monstro goblin

✨ Monstro novo com IA
!monstro

✨ NPC
!npc mercador corrupto

✨ Encontro
!encontro 5 medio

✨ Item mágico
!item espada

✨ Vilão
!vilao necromante

✨ Puzzle
!puzzle portas misteriosas

🎯 Casos de Uso Detalhados

📖 Caso 1: Preparar uma Sessão
Objetivo: Mestre quer preparar sessão de D&D 5e para grupo nível 5

1. Configurar sistema
!sistema dnd5e

2. Gerar vilão principal
!vilao mago maligno

3. Criar encontros
!encontro 5 medio
!encontro 5 dificil

4. Gerar NPCs
!npc taberneiro simpático
!npc guarda corrupto

5. Criar puzzles
!puzzle estátuas antigas

6. Gerar tesouro
!tesouro 5

7. Adicionar monstros
!monstro orc
!monstro dragão jovem

🎮 Caso 2: Rodar uma Sessão Completa
1. Criar sessão
!iniciarsessao @Jogador1 @Jogador2 @Jogador3

[Canal privado é criado]

2. Jogadores selecionam fichas
[Jogador1] !selecionarficha Thorin
[Jogador2] !selecionarficha Elara
[Jogador3] !selecionarficha Luna

3. Mestre inicia aventura (botão)
Bot gera introdução épica

4. Durante o jogo
[Mestre] !cena floresta sombria à noite
[Jogador1] !rolar 1d20+3
[Mestre] !monstro lobos direcionais
[Jogador2] !rolar 2d6+5

5. Consultar IA
[Mestre] !mestre como balancear este encontro?
[Jogador1] !regra ataque de oportunidade

6. Gerar conteúdo improvisado
[Mestre] !npc
[Mestre] !item
[Mestre] !armadilha media

7. Fim da sessão
[Mestre] !resumosessao
Bot gera resumo narrativo

[Mestre] Clica "🚪 Encerrar Sessão"
🔄 Caso 3: Converter Campanha Entre Sistemas
Campanha em D&D 5e, quer mudar para Pathfinder

1. Ver fichas atuais
!minhasfichas

2. Converter cada ficha
!converterficha pathfinder Thorin
!converterficha pathfinder Elara
!converterficha pathfinder Luna

3. Mudar sistema do canal
!sistema pathfinder

4. Continuar normalmente
!iniciarsessao @Jogador1 @Jogador2

🎲 Sistemas Suportados (50+)
D&D e Derivados
•	D&D 5e (dnd5e)
•	D&D 3.5 (dnd35)
•	Pathfinder 1e (pathfinder1e)
•	Pathfinder 2e (pathfinder)
•	13th Age (13thage)
•	Microlite20 (microlite20)
•	Tiny Dungeon (tiny_dungeon)

Horror e Investigação
•	Call of Cthulhu 7e (cthulhu)
•	World/Chronicles of Darkness (cofd)
•	Vampire: The Masquerade (vampire)
•	Werewolf: The Apocalypse (werewolf)
•	Mage: The Ascension (mage)

Ficção Científica
•	Shadowrun 5e/6e (shadowrun)
•	Cyberpunk 2020 (cyberpunk2020)
•	Cyberpunk RED (cyberpunkred)
•	Eclipse Phase 2e (eclipse)
•	Star Trek Adventures (startrek)
•	Star Wars d20 (starwars_d20)
•	Star Wars FFG (starwars_ffg)

Warhammer
•	Warhammer Fantasy 1e (wfrp1e)
•	Warhammer Fantasy 4e (wfrp4e)

Genéricos/Universais
•	GURPS 4e (gurps)
•	FATE Core (fate_core)
•	FATE Accelerated (fate_accelerated)
•	Savage Worlds (savage)
•	Cortex Prime (cortex)
•	Risus (risus)

Powered by the Apocalypse
•	Apocalypse World (apocalypse)
•	Dungeon World (dungeon_world)
•	Monster of the Week (monster_week)

Forged in the Dark
•	Blades in the Dark (blades)

Outros Populares
•	7th Sea 2e (7thsea)
•	Shadow of the Demon Lord (shadowdemon)
•	Mutants & Masterminds 3e (mutants)
•	Champions / Hero System (champions)
•	Marvel FASERIP (faserip)
•	Deadlands (deadlands)
•	Fiasco (fiasco)
•	Numenera / Cypher (numenera)
•	Legend of the Five Rings (l5r)
•	Exalted 3e (exalted)
•	Ars Magica 5e (ars_magica)
•	Pendragon (pendragon)
•	Iron Kingdoms (ironkingdoms)
•	Victoriana 3e (victoriana)
Total: 50+ sistemas

🎨 Recursos Especiais

🤖 IA Integrada (Groq + Llama 3.3)
•	Geração de fichas completas
•	Criação de NPCs e monstros
•	Descrições narrativas e cenas
•	Introduções de sessão
•	Resumos automáticos
•	Assistente contextual do mestre

💾 Persistência de Dados
•	Auto-save a cada 5 minutos
•	Backup manual via comando
•	Estrutura JSON organizada
•	Exportação de fichas

🔐 Sessões Privadas
•	Canais isolados por sessão
•	Controle de permissões automático
•	Botões interativos
•	Sistema de fichas integrado

📊 Banco de Dados de Monstros
•	D&D 5e: Goblin, Orc, Dragão Vermelho, Beholder, Lich
•	Call of Cthulhu: Profundo, Shoggoth, Byakhee, Ghoul
•	Pathfinder: Minotauro, Dragão de Bronze
•	Vampire: Lobisomem Garou, Tzimisce
•	Shadowrun: Drake, Espírito Inseto

🎯 Conversão Entre Sistemas
•	Converte fichas mantendo conceito e poder
•	IA adapta mecânicas automaticamente
•	Suporta conversão entre qualquer par de sistemas

🛠️ Comandos Administrativos

Diagnóstico completo
!troubleshoot

Recarregar módulo sem reiniciar
!reload fichas

Backup manual
!backup

💡 Dicas e Truques

✨ Melhor Uso da IA
•	Seja específico nas descrições
•	Use !mestre para dúvidas contextuais
•	!cena para descrições imersivas
•	!resumosessao para recapitular

🎲 Rolagem de Dados Avançada
!rolar 1d20+5          # Rolagem simples
!rolar 2d6+3           # Múltiplos dados
!rolar 4d6k3           # Mantém 3 maiores
!rolar 1d100           # Percentual
!rolar 8d6             # Pool grande

🎮 Organização de Sessão
1.	Configure sistema ANTES de criar sessão
2.	Peça para jogadores criarem fichas com antecedência
3.	Use !infosessao para verificar quem falta
4.	!resumosessao no início da próxima sessão

📝 Gestão de Fichas
•	Use nomes únicos e memoráveis
•	!minhasfichas para revisão rápida
•	!exportarficha para backup externo
•	Converta fichas quando experimentar sistemas novos

❓ FAQ
P: Quantos comandos posso usar por minuto? R: Sem limite! Mas a API do Groq tem rate limit.
P: As fichas são salvas permanentemente? R: Sim, com auto-save a cada 5 minutos + backup manual.
P: Posso ter múltiplas sessões simultâneas? R: Sim! Cada sessão tem seu próprio canal privado.
P: Como adicionar mais monstros ao banco? R: Edite monstros_database.py ou peça ao desenvolvedor.
P: O bot funciona offline? R: Não, precisa de conexão para Discord e Groq API.
P: Posso usar em múltiplos servidores? R: Sim! Cada servidor tem seus próprios dados.

📞 Suporte
•	Desenvolvedor: Leosdc_
•	Comando: !suporte
•	GitHub: https://github.com/Leosdc/lyra-the-wise

📄 Licença
Bot desenvolvido para comunidades de RPG. Versão 2.5.6 - 2025

Tecnologias:
•	Python 3.10+
•	Discord.py 2.0+
•	Groq API (Llama 3.3 70B)
"""

def register(bot: commands.Bot):
    # Remove versões antigas do comando se já existirem
    if "documentacao" in bot.all_commands:
        bot.remove_command("documentacao")

    @bot.command(name="documentacao")
    async def documentacao(ctx):
        """Exibe a documentação completa do bot."""
        texto = DOCUMENTACAO_COMPLETA
        # Deleta o comando do usuário

        is_dm = isinstance(ctx.channel, discord.DMChannel)

        try:
            await ctx.message.delete()
        except:
            pass
        
        # Envia por DM
        try:
            if len(texto) <= 2000:
                await ctx.author.send(texto)
            else:
                partes = [texto[i:i+2000] for i in range(0, len(texto), 2000)]
                for parte in partes:
                    await ctx.author.send(parte)
            if not is_dm:
                await ctx.send(f"📨 {ctx.author.mention}, documentação enviada no privado!", delete_after=10)
        
        except discord.Forbidden:
            await ctx.send(
                f"❌ {ctx.author.mention}, não consigo te enviar DM! "
                f"Habilite mensagens diretas nas configurações.",
                delete_after=15
            )