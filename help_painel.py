# help_painel.py (ATUALIZADO v3.0)
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

        # ---------------- Página 1 - Configuração & Dados ----------------
        embed1 = discord.Embed(
            title="🎲 Lyra, the Wise - Comandos v3.0 (1/5)",
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
!rolar 4d6k3 - Mantém 3 maiores""",
            inline=False,
        )
        embed1.add_field(
            name="👤 Fichas & Personagens",
            value="""\
!ficha <nome> - Cria ficha automática com IA
!criarficha - Formulário interativo 📝
!verficha <nome> - Ver fichas
!editarficha <nome> - Edita ficha ✏️
!deletarficha <nome> - Deleta ficha
!converterficha <sistema> <nome> - Converte ficha
!minhasfichas [sistema] - Lista detalhada
!exportarficha <nome> - Exporta como JSON""",
            inline=False,
        )
        embed1.set_footer(text="📄 Página 1/5 • Use os botões abaixo para navegar")
        pages.append(embed1)

        # ---------------- Página 2 - Inventário & XP (NOVO v3.0) ----------------
        embed2 = discord.Embed(
            title="🎲 Lyra, the Wise - Comandos v3.0 (2/5)",
            description="Inventário, XP e progressão de personagens",
            color=discord.Color.gold(),
        )
        embed2.add_field(
            name="🎒 Sistema de Inventário",
            value="""\
!inventario [nome] - Ver inventário completo
!addinventario <item> [qtd] [tipo] - Adicionar item
!equiparitem <item> - Equipar arma/armadura
!usaritem <item> - Usar/consumir item
!jogarfora <item> - Descartar item
!vender <item> [preço] - Vender item

💡 Exemplo: !addinventario "Poção de Cura" 3 consumível""",
            inline=False,
        )
        embed2.add_field(
            name="📊 Sistema de XP e Progressão",
            value="""\
!xp [nome] - Ver XP e progressão
!darxp <@jogador> <quantidade> - Dar XP individual 🔒
!darxpgrupo <quantidade> - Dar XP para todos 🔒

✨ Level up automático quando atingir XP necessário
📈 Barra de progresso visual (🟩⬜)
🎯 XP Total acumulado rastreado""",
            inline=False,
        )
        embed2.set_footer(text="📄 Página 2/5 • 🔒 = Apenas Mestre")
        pages.append(embed2)

        # ---------------- Página 3 - Geração & IA ----------------
        embed3 = discord.Embed(
            title="🎲 Lyra, the Wise - Comandos v3.0 (3/5)",
            description="Ferramentas de geração e IA",
            color=discord.Color.orange(),
        )
        embed3.add_field(
            name="🎮 Geração de Encontros",
            value="""\
!monstro <nome> - Cria um monstro
!encontro <nível> <dificuldade> - Gera encontro balanceado
!armadilha <dificuldade> - Cria armadilha
!cena <descrição> - Descreve cena dramaticamente""",
            inline=False,
        )
        embed3.add_field(
            name="✨ Geração de Conteúdo",
            value="""\
!item <tipo> - Gera item mágico/especial
!tesouro <nível> - Gera tesouro balanceado
!puzzle <tema> - Cria enigma/quebra-cabeça
!vilao <tipo> - Gera vilão completo
!npc [descrição] - Cria NPC detalhado
!nome <tipo> - Lista 10 nomes criativos
!motivacao - Sorteia motivação para NPC""",
            inline=False,
        )
        embed3.add_field(
            name="🎭 Assistente do Mestre",
            value="""\
!mestre <pergunta> - Pergunta qualquer coisa
!plot <tema> - Gera ideias de missão/aventura
!regra <dúvida> - Consulta regras do sistema
!sessao <tema> - Planeja sessão completa 📋

💡 Mantém memória da conversa por canal!""",
            inline=False,
        )
        embed3.set_footer(text="📄 Página 3/5")
        pages.append(embed3)

        # ---------------- Página 4 - Sessões v3.0 (ATUALIZADO) ----------------
        embed4 = discord.Embed(
            title="🎮 Lyra, the Wise - Sessões v3.0 (4/5)",
            description="Sistema de sessões TOTALMENTE controlado pelo mestre",
            color=discord.Color.dark_green(),
        )
        embed4.add_field(
            name="🎬 Comandos de Sessão",
            value="""\
!iniciarsessao @jog1 @jog2 - Cria sessão privada
!selecionarficha <nome> - Escolhe sua ficha
!sessoes - Lista sessões ativas
!pausarsessao - Pausa/retoma
!resumosessao - Resumo com IA""",
            inline=False,
        )
        embed4.add_field(
            name="📖 Narrativa e Ações (v3.0)",
            value="""\
**[MESTRE]**
!narrativa <descrição> - Lyra narra a cena
!acoespendentes - Ver ações dos jogadores
!limparacoes - Limpar ações

**[JOGADORES]**
!acao <descrição> - Descrever ação do personagem

💡 Lyra apenas narra - mestre controla tudo!""",
            inline=False,
        )
        embed4.add_field(
            name="🎮 Botões de Controle do Mestre",
            value="""\
🎲 **Solicitar Rolagens** - Escolhe jogadores e dados
⚔️ **Iniciar Combate** - Ativa modo de combate
📊 **Status Geral** - Mostra HP/CA de todos
📖 **Ver Ações Pendentes** - Lista ações declaradas""",
            inline=False,
        )
        embed4.set_footer(text="📄 Página 4/5 • v3.0: Mestre tem controle total")
        pages.append(embed4)

        # ---------------- Página 5 - Combate & Admin ----------------
        embed5 = discord.Embed(
            title="🎮 Lyra, the Wise - Combate & Admin (5/5)",
            description="Sistema de combate tático e administração",
            color=discord.Color.red(),
        )
        embed5.add_field(
            name="⚔️ Sistema de Combate Tático",
            value="""\
!iniciarcombate - Ativa modo de combate 🔒
!addinimigo <nome> <HP> <CA> [bonus] - Adiciona inimigo 🔒
!rolariniciativa - Rola iniciativa para todos 🔒
!statuscombate - Mostra status (HP, CA, turno)
!atacar <alvo> <dano> - Ataca inimigo
!curar <alvo> <HP> - Cura aliado
!proximoturno - Avança turno 🔒
!encerrarcombate - Finaliza e salva HP 🔒""",
            inline=False,
        )
        embed5.add_field(
            name="🧠 Administração e Utilidades",
            value="""\
!stats - Mostra estatísticas do bot
!reload <módulo> - Recarrega partes do bot 🔒
!backup - Cria backup manual dos dados 🔒
!documentacao - Exibe documentação completa
!ajuda - Mostra comandos básicos
!suporte - Link de suporte ou contato
!sobre - Informações sobre o bot""",
            inline=False,
        )
        embed5.add_field(
            name="💡 Fluxo Completo v3.0",
            value="""\
1️⃣ `!iniciarsessao @jogadores`
2️⃣ Jogadores: `!selecionarficha <nome>`
3️⃣ Mestre: Clica **Iniciar Aventura**
4️⃣ Mestre: `!narrativa <situação>`
5️⃣ Jogadores: `!acao <o que fazem>`
6️⃣ Mestre: Usa botões de controle
7️⃣ Mestre: `!darxpgrupo 300`
8️⃣ Jogadores: `!inventario`, `!xp`""",
            inline=False,
        )
        embed5.set_footer(text="📄 Página 5/5 • v3.0 • 🔒 = Apenas Mestre")
        pages.append(embed5)

        # ---------------- Navegação ----------------
        is_dm = isinstance(ctx.channel, discord.DMChannel)

        class HelpView(View):
            def __init__(self):
                super().__init__(timeout=None)
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

        # Deleta o comando do usuário
        try:
            await ctx.message.delete()
        except:
            pass
        
        # Envia por DM
        try:
            await ctx.author.send(embed=pages[0], view=HelpView())

            if not is_dm:
                await ctx.send(f"📨 {ctx.author.mention}, confira seu privado!", delete_after=10)
        except discord.Forbidden:
            await ctx.send(
                f"❌ {ctx.author.mention}, não consigo te enviar DM! "
                f"Habilite mensagens diretas nas configurações de privacidade.",
                delete_after=15
            )