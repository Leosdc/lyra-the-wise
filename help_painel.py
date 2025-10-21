# help_painel.py — versão completa com administração restaurada
import discord
from discord.ext import commands
from discord.ui import View, button

COMMANDS = ["rpghelp"]

def register(bot: commands.Bot):
    try:
        bot.remove_command("rpghelp")
    except Exception:
        pass

    @bot.command(name="rpghelp")
    async def rpghelp(ctx):
        pages = []

        # ---------------- Página 1 ----------------
        embed1 = discord.Embed(
            title="🎲 RPG Master Bot - Comandos (1/4)",
            description="Seu assistente completo de RPG de mesa!",
            color=discord.Color.teal(),
        )
        embed1.add_field(
            name="⚙️ Configuração",
            value="""\
!sistema - Ver/mudar sistema atual
!sistema dnd5e - Mudar para D&D 5e
!sistemas - Lista todos os 50+ sistemas
!buscarsistema <nome> - Busca sistemas
!infosistema <código> - Detalhes do sistema
!limpar - Limpa histórico de conversa""",
            inline=False,
        )
        embed1.add_field(
            name="🎲 Dados & Iniciativa",
            value="""\
!rolar 1d20 ou !r 1d20 - Rola dados
!rolar 2d6+3 - Rola com modificador
!rolar 4d6k3 - Mantém 3 maiores
!iniciativa - Rola iniciativa para o grupo""",
            inline=False,
        )
        embed1.add_field(
            name="👤 Fichas & Personagens",
            value="""\
!ficha <nome> - Cria ficha automática com IA
!criarficha - Formulário interativo 📝
!verficha / !verficha <nome> - Ver fichas
!editarficha <nome> - Edita ficha ✏️
!deletarficha <nome> - Deleta ficha
!converterficha <sistema> <nome> - Converte ficha
!minhasfichas [sistema] - Lista detalhada
!exportarficha <nome> - Exporta como JSON""",
            inline=False,
        )
        embed1.set_footer(text="📄 Página 1/4 • Use os botões abaixo para navegar")
        pages.append(embed1)

        # ---------------- Página 2 ----------------
        embed2 = discord.Embed(
            title="🎲 RPG Master Bot - Comandos (2/4)",
            description="Ferramentas de combate, geração e planejamento",
            color=discord.Color.orange(),
        )
        embed2.add_field(
            name="⚔️ Combate & Encontros",
            value="""\
!monstro <nome> - Busca stats de monstros
!encontro <nível> <dificuldade> - Gera encontro balanceado
!armadilha <dificuldade> - Cria armadilha
!cena <descrição> - Descreve cena dramaticamente""",
            inline=False,
        )
        embed2.add_field(
            name="✨ Geração de Conteúdo",
            value="""\
!item <tipo> - Gera item mágico/especial
!tesouro <nível> - Gera tesouro balanceado
!puzzle <tema> - Cria enigma/quebra-cabeça
!vilao <tipo> - Gera vilão completo
!nome <tipo> - Lista 10 nomes criativos
!motivacao - Sorteia motivação para NPC""",
            inline=False,
        )
        embed2.add_field(
            name="📖 História & Campanha",
            value="""\
!plot <tema> - Gera ideias de missão/aventura
!sessao <tema> - Planeja sessão completa 📋
!regra <dúvida> - Consulta regras do sistema""",
            inline=False,
        )
        embed2.set_footer(text="📄 Página 2/4")
        pages.append(embed2)

        # ---------------- Página 3 ----------------
        embed3 = discord.Embed(
            title="🎲 RPG Master Bot - Comandos (3/4)",
            description="Assistente e utilitários",
            color=discord.Color.blue(),
        )
        embed3.add_field(
            name="🎭 Assistente do Mestre",
            value="""\
!mestre <pergunta> - Pergunta qualquer coisa
Use para: criar histórias, balancear encontros,
improvisar situações e tirar dúvidas de regras.
💡 Mantém memória da conversa por canal!""",
            inline=False,
        )
        embed3.add_field(
            name="📚 Sistemas Suportados",
            value="""\
50+ sistemas de RPG disponíveis:
!sistemas ou !listarsistemas - Ver todos
!buscarsistema <nome> - Buscar sistema
!infosistema [código] - Detalhes do sistema

Exemplos populares:
• D&D 5e, 3.5, Pathfinder 1e/2e, 13th Age
• Call of Cthulhu, World of Darkness
• Shadowrun, Cyberpunk, Star Wars
• GURPS, FATE, Savage Worlds
• Blades in the Dark, Dungeon World""",
            inline=False,
        )
        embed3.add_field(
            name="🧠 Administração e Utilidades",
            value="""\
!stats - Mostra estatísticas do bot
!reload <módulo> - Recarrega partes do bot (admin)
!backup - Cria backup manual dos dados
!documentacao - Exibe documentação completa
!ajuda - Mostra comandos básicos
!suporte - Link de suporte ou contato""",
            inline=False,
        )
        embed3.set_footer(text="📄 Página 3/4")
        pages.append(embed3)

        # ---------------- Página 4 ----------------
        embed4 = discord.Embed(
            title="🎮 RPG Master Bot - Sessões de RPG (4/4)",
            description="Gerencie campanhas com canais privados e fichas integradas",
            color=discord.Color.dark_green(),
        )
        embed4.add_field(
            name="🎬 Sessões e Jogadores",
            value="""\
!iniciarsessao @Jogador1 @Jogador2 - Cria sessão privada
!sessoes - Lista sessões ativas
!infosessao - Mostra detalhes da sessão
!convidarsessao @Jogador - Adiciona jogador
!removerjogador @Jogador - Remove jogador""",
            inline=False,
        )
        embed4.add_field(
            name="👤 Fichas em Sessão",
            value="""\
!selecionarficha <nome> - Escolhe ficha
!mudarficha <nome> - Troca personagem
!verficha <nome> - Mostra ficha
!resumosessao - Gera resumo narrativo com IA""",
            inline=False,
        )
        embed4.add_field(
            name="⚙️ Controle e Botões",
            value="""\
!pausarsessao - Pausa/retoma sessão
!ajudasessao - Guia completo de sessões

🎬 **Botões no canal:**
• Iniciar Aventura — Introdução épica
• Ver Fichas — Mostra status dos jogadores
• Encerrar Sessão — Deleta canal com confirmação""",
            inline=False,
        )
        embed4.set_footer(text="📄 Página 4/4 • Sistema de Sessões com IA e botões interativos")
        pages.append(embed4)

        # ---------------- Navegação ----------------
        class HelpView(View):
            def __init__(self):
                super().__init__(timeout=180)
                self.page = 0

            async def update(self, interaction):
                await interaction.response.edit_message(embed=pages[self.page], view=self)

            @button(label="◀️ Anterior", style=discord.ButtonStyle.secondary)
            async def previous(self, interaction, _):
                self.page = (self.page - 1) % len(pages)
                await self.update(interaction)

            @button(label="▶️ Próximo", style=discord.ButtonStyle.secondary)
            async def next(self, interaction, _):
                self.page = (self.page + 1) % len(pages)
                await self.update(interaction)

            @button(label="❌ Fechar", style=discord.ButtonStyle.danger)
            async def close(self, interaction, _):
                await interaction.message.delete()

        await ctx.send(embed=pages[0], view=HelpView())
