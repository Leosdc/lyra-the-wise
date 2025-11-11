# documentacao.py — versão visual e bilíngue (PT/EN) com troca completa de idioma
import discord
from discord.ext import commands
from discord.ui import View, button

def register(bot: commands.Bot):
    try:
        bot.remove_command("documentacao")
    except Exception:
        pass

    @bot.command(name="documentacao")
    async def documentacao(ctx):
        """Exibe/Mostra a documentação completa da Lyra em páginas, com suporte PT/EN."""
        # -------------------- PÁGINAS EM PORTUGUÊS --------------------
        pt_pages = []

        embed1_pt = discord.Embed(
            title="📘 Lyra The Wise — Documentação (1/5)",
            description="Visão geral e configuração inicial",
            color=discord.Color.teal()
        )
        embed1_pt.add_field(
            name="🎲 Visão Geral",
            value=(
                "Bot completo para gerenciamento de mesas de RPG no Discord.\n"
                "Suporte a **40+ sistemas**, **IA narrativa**, **sessões privadas** "
                "e **combate tático** automatizado."
            ),
            inline=False
        )
        embed1_pt.add_field(
            name="⚙️ Configuração e Sistemas",
            value="""\
!sistema [código] — Ver/mudar sistema atual  
!sistemas — Lista os 40+ sistemas disponíveis  
!buscarsistema <termo> — Busca sistemas por nome  
!infosistema <código> — Mostra detalhes de um sistema  
!limpar — Limpa histórico de conversa do canal""",
            inline=False
        )
        embed1_pt.add_field(
            name="🎲 Dados e Rolagens",
            value="""\
!rolar <expressão> — Ex: 2d6+3, 4d6k3  
!r <expressão> — Atalho para rolagem  
!iniciativa — Rola iniciativa do grupo""",
            inline=False
        )
        embed1_pt.set_footer(text="📄 Página 1/5 — Configuração e Rolagens")
        pt_pages.append(embed1_pt)

        embed2_pt = discord.Embed(
            title="📘 Lyra The Wise — Documentação (2/5)",
            description="Fichas, Sessões e Combate",
            color=discord.Color.orange()
        )
        embed2_pt.add_field(
            name="👤 Fichas de Personagem",
            value="""\
!ficha <nome> — Cria ficha automática com IA  
!minhasfichas [sistema] — Lista fichas  
!verficha <nome> — Mostra ficha específica  
!editarficha <nome> — Edita ficha existente  
!converterficha <sistema> <nome> — Converte entre sistemas  
!exportarficha <nome> — Exporta como JSON""",
            inline=False
        )
        embed2_pt.add_field(
            name="🎮 Sessões de RPG",
            value="""\
!iniciarsessao @Jogadores — Cria sessão privada  
!sessoes — Lista sessões ativas  
!infosessao — Mostra detalhes  
!convidarsessao / !removerjogador — Gerencia membros  
!selecionarficha <nome> — Escolhe personagem  
!pausarsessao — Pausa/retoma  
!resumosessao — Gera resumo narrativo com IA""",
            inline=False
        )
        embed2_pt.add_field(
            name="⚔️ Combate e Encontros",
            value="""\
!iniciarcombate — Ativa modo tático  
!addinimigo <nome> <HP> <CA> — Adiciona inimigo  
!rolariniciativa — Define ordem de turnos  
!statuscombate — Mostra status (HP, CA, turno)  
!atacar / !curar — Ações em combate  
!encerrarcombate — Finaliza e salva HP""",
            inline=False
        )
        embed2_pt.set_footer(text="📄 Página 2/5 — Fichas, Sessões e Combate")
        pt_pages.append(embed2_pt)

        embed3_pt = discord.Embed(
            title="📘 Lyra The Wise — Documentação (3/5)",
            description="Geração de conteúdo e ferramentas do mestre",
            color=discord.Color.blurple()
        )
        embed3_pt.add_field(
            name="✨ Geração de Conteúdo",
            value="""\
!item <tipo> — Gera item mágico  
!tesouro <nível> — Gera tesouro balanceado  
!puzzle <tema> — Cria enigma ou quebra-cabeça  
!vilao <tipo> — Gera vilão completo  
!cena <descrição> — Descreve cena cinematográfica  
!nome <tipo> — Lista 10 nomes criativos""",
            inline=False
        )
        embed3_pt.add_field(
            name="🎭 Assistente do Mestre (IA)",
            value="""\
!mestre <pergunta> — Pergunte qualquer coisa  
!plot <tema> — Ideias de missão/aventura  
!regra <dúvida> — Consulta regras  
!motivacao — Sorteia motivações para NPCs  
💡 Mantém memória do canal e contexto narrativo.""",
            inline=False
        )
        embed3_pt.add_field(
            name="👹 Monstros e NPCs",
            value="""\
!monstro [nome] — Busca ou gera monstro  
!npc [descrição] — Cria NPC detalhado  
!encontro [nível] [dificuldade] — Cria encontro completo""",
            inline=False
        )
        embed3_pt.set_footer(text="📄 Página 3/5 — Criação e IA")
        pt_pages.append(embed3_pt)

        embed4_pt = discord.Embed(
            title="📘 Lyra The Wise — Documentação (4/5)",
            description="Administração, dicas e persistência",
            color=discord.Color.green()
        )
        embed4_pt.add_field(
            name="🔧 Administração",
            value="""\
!stats — Mostra estatísticas do bot  
!backup — Cria backup manual 🔒  
!reload <módulo> — Recarrega partes do bot 🔒  
!troubleshoot — Diagnóstico geral 🔒  
!ping — Testa latência""",
            inline=False
        )
        embed4_pt.add_field(
            name="💾 Persistência e Dados",
            value="""\
• Auto-save a cada 5 minutos  
• Backup manual  
• Estrutura JSON limpa  
• Fichas exportáveis e importáveis""",
            inline=False
        )
        embed4_pt.add_field(
            name="💡 Dicas Rápidas",
            value="""\
• Use !resumosessao ao fim de cada sessão  
• Crie fichas antes de iniciar aventuras  
• Utilize !mestre para improvisos e dúvidas  
• Explore !puzzle, !vilao e !npc para enriquecer o jogo!""",
            inline=False
        )
        embed4_pt.set_footer(text="📄 Página 4/5 — Administração e Dicas")
        pt_pages.append(embed4_pt)

        embed5_pt = discord.Embed(
            title="📘 Lyra The Wise — Documentação (5/5)",
            description="Sistemas suportados, suporte e créditos",
            color=discord.Color.purple()
        )
        embed5_pt.add_field(
            name="🎲 Principais Sistemas Suportados",
            value="""\
D&D 5e / 3.5 • Pathfinder 1e/2e • Call of Cthulhu  
Vampire / Werewolf / Mage • GURPS • FATE • Shadowrun  
Cyberpunk RED / 2020 • Star Wars d20 / FFG  
Savage Worlds • Blades in the Dark • Dungeon World  
E muitos outros! Total: **40+ sistemas**""",
            inline=False
        )
        embed5_pt.add_field(
            name="📞 Suporte e Contato",
            value="""\
• Desenvolvedor: **Leosdc_**  
• GitHub: [Lyra the Wise](https://github.com/Leosdc/lyra-the-wise)  
• Discord: [Taverna](https://discord.gg/SdWnWJ6w)  
• Comando: !suporte""",
            inline=False
        )
        embed5_pt.add_field(
            name="📄 Licença e Créditos",
            value="""\
Versão 2.6.0 — 2025  
Tecnologias: Python 3.10+, Discord.py 2.0+, Groq API (Llama 3.3 70B)  
🧙 Feito com ❤️ para a comunidade de RPG""",
            inline=False
        )
        embed5_pt.set_footer(text="📄 Página 5/5 — Créditos e Suporte")
        pt_pages.append(embed5_pt)

        # -------------------- PAGES IN ENGLISH (FULL) --------------------
        en_pages = []

        embed1_en = discord.Embed(
            title="📘 Lyra The Wise — Documentation (1/5)",
            description="Overview and initial setup",
            color=discord.Color.teal()
        )
        embed1_en.add_field(
            name="🎲 Overview",
            value=(
                "Full-featured bot to run tabletop RPG games on Discord.\n"
                "Supports **40+ systems**, **narrative AI**, **private sessions**, "
                "and **automated tactical combat**."
            ),
            inline=False
        )
        embed1_en.add_field(
            name="⚙️ Setup & Systems",
            value="""\
!sistema [code] — View/change current system  
!sistemas — List all 40+ available systems  
!buscarsistema <term> — Search systems by name  
!infosistema <code> — System details  
!limpar — Clear channel conversation history""",
            inline=False
        )
        embed1_en.add_field(
            name="🎲 Dice & Initiative",
            value="""\
!rolar <expr> — e.g., 2d6+3, 4d6k3  
!r <expr> — Roll shortcut  
!iniciativa — Roll party initiative""",
            inline=False
        )
        embed1_en.set_footer(text="📄 Page 1/5 — Setup & Rolls")
        en_pages.append(embed1_en)

        embed2_en = discord.Embed(
            title="📘 Lyra The Wise — Documentation (2/5)",
            description="Characters, sessions and combat",
            color=discord.Color.orange()
        )
        embed2_en.add_field(
            name="👤 Character Sheets",
            value="""\
!ficha <name> — Create an AI-generated sheet  
!minhasfichas [system] — List your sheets  
!verficha <name> — View a specific sheet  
!editarficha <name> — Edit an existing sheet  
!converterficha <system> <name> — Convert between systems  
!exportarficha <name> — Export as JSON""",
            inline=False
        )
        embed2_en.add_field(
            name="🎮 RPG Sessions",
            value="""\
!iniciarsessao @Players — Create a private session  
!sessoes — List active sessions  
!infosessao — Session details  
!convidarsessao / !removerjogador — Manage members  
!selecionarficha <name> — Choose character  
!pausarsessao — Pause/Resume  
!resumosessao — AI session recap""",
            inline=False
        )
        embed2_en.add_field(
            name="⚔️ Combat & Encounters",
            value="""\
!iniciarcombate — Enable tactical mode  
!addinimigo <name> <HP> <AC> — Add enemy  
!rolariniciativa — Set turn order  
!statuscombate — Status (HP, AC, turn)  
!atacar / !curar — Actions during combat  
!encerrarcombate — Finish and save HP""",
            inline=False
        )
        embed2_en.set_footer(text="📄 Page 2/5 — Sheets, Sessions & Combat")
        en_pages.append(embed2_en)

        embed3_en = discord.Embed(
            title="📘 Lyra The Wise — Documentation (3/5)",
            description="Content generation and GM tools",
            color=discord.Color.blurple()
        )
        embed3_en.add_field(
            name="✨ Content Generation",
            value="""\
!item <type> — Generate a magic item  
!tesouro <level> — Balanced treasure  
!puzzle <theme> — Create a riddle/puzzle  
!vilao <type> — Build a complete villain  
!cena <desc> — Cinematic scene description  
!nome <type> — 10 creative names""",
            inline=False
        )
        embed3_en.add_field(
            name="🎭 GM Assistant (AI)",
            value="""\
!mestre <question> — Ask anything  
!plot <theme> — Quest/adventure ideas  
!regra <doubt> — Rules lookup  
!motivacao — Random NPC motivations  
💡 Keeps channel memory and narrative context.""",
            inline=False
        )
        embed3_en.add_field(
            name="👹 Monsters & NPCs",
            value="""\
!monstro [name] — Look up or generate a monster  
!npc [desc] — Create a detailed NPC  
!encontro [level] [difficulty] — Full encounter""",
            inline=False
        )
        embed3_en.set_footer(text="📄 Page 3/5 — Creation & AI")
        en_pages.append(embed3_en)

        embed4_en = discord.Embed(
            title="📘 Lyra The Wise — Documentation (4/5)",
            description="Administration, tips and persistence",
            color=discord.Color.green()
        )
        embed4_en.add_field(
            name="🔧 Administration",
            value="""\
!stats — Bot statistics  
!backup — Manual backup 🔒  
!reload <module> — Reload parts of the bot 🔒  
!troubleshoot — Diagnostic tools 🔒  
!ping — Latency test""",
            inline=False
        )
        embed4_en.add_field(
            name="💾 Persistence & Data",
            value="""\
• Auto-save every 5 minutes  
• Manual backups  
• Clean JSON structure  
• Import/Export character sheets""",
            inline=False
        )
        embed4_en.add_field(
            name="💡 Quick Tips",
            value="""\
• Use !resumosessao at the end of each session  
• Create sheets before starting adventures  
• Use !mestre for improv and rules  
• Explore !puzzle, !vilao and !npc to enrich play!""",
            inline=False
        )
        embed4_en.set_footer(text="📄 Page 4/5 — Admin & Tips")
        en_pages.append(embed4_en)

        embed5_en = discord.Embed(
            title="📘 Lyra The Wise — Documentation (5/5)",
            description="Supported systems, support and credits",
            color=discord.Color.purple()
        )
        embed5_en.add_field(
            name="🎲 Main Supported Systems",
            value="""\
D&D 5e / 3.5 • Pathfinder 1e/2e • Call of Cthulhu  
Vampire / Werewolf / Mage • GURPS • FATE • Shadowrun  
Cyberpunk RED / 2020 • Star Wars d20 / FFG  
Savage Worlds • Blades in the Dark • Dungeon World  
And many more! Total: **40+ systems**""",
            inline=False
        )
        embed5_en.add_field(
            name="📞 Support & Contact",
            value="""\
• Developer: **Leosdc_**  
• GitHub: [Lyra the Wise](https://github.com/Leosdc/lyra-the-wise)  
• Discord: [Tavern](https://discord.gg/SdWnWJ6w)  
• Command: !suporte / !support (soon)""",
            inline=False
        )
        embed5_en.add_field(
            name="📄 License & Credits",
            value="""\
Version 2.6.0 — 2025  
Tech: Python 3.10+, Discord.py 2.0+, Groq API (Llama 3.3 70B)  
🧙 Made with ❤️ for the RPG community""",
            inline=False
        )
        embed5_en.set_footer(text="📄 Page 5/5 — Credits & Support")
        en_pages.append(embed5_en)

        # -------------------- VIEW COM TROCA DE IDIOMA --------------------
        class DocView(View):
            def __init__(self, start_lang: str = "pt"):
                super().__init__(timeout=None)
                self.page = 0
                self.lang = start_lang  # "pt" ou "en"
                self._sync_labels()

            def _sync_labels(self):
                """Atualiza rótulos dos botões conforme o idioma."""
                prev = "◀️ Anterior" if self.lang == "pt" else "◀️ Previous"
                nxt  = "▶️ Próximo"  if self.lang == "pt" else "▶️ Next"
                close = "❌ Fechar"  if self.lang == "pt" else "❌ Close"
                switch = "🌐 Mudar idioma" if self.lang == "pt" else "🌐 Change language"
                # children: [previous, next, switch_lang, close]
                self.children[0].label = prev
                self.children[1].label = nxt
                self.children[2].label = switch
                self.children[3].label = close

            async def update(self, interaction):
                pages = pt_pages if self.lang == "pt" else en_pages
                await interaction.response.edit_message(embed=pages[self.page], view=self)

            @button(label="◀️ Anterior", style=discord.ButtonStyle.secondary)
            async def previous(self, interaction, _):
                pages = pt_pages if self.lang == "pt" else en_pages
                self.page = (self.page - 1) % len(pages)
                await self.update(interaction)

            @button(label="▶️ Próximo", style=discord.ButtonStyle.secondary)
            async def next(self, interaction, _):
                pages = pt_pages if self.lang == "pt" else en_pages
                self.page = (self.page + 1) % len(pages)
                await self.update(interaction)

            @button(label="🌐 Mudar idioma", style=discord.ButtonStyle.primary)
            async def switch_lang(self, interaction, _):
                self.lang = "en" if self.lang == "pt" else "pt"
                self._sync_labels()
                await self.update(interaction)

            @button(label="❌ Fechar", style=discord.ButtonStyle.danger)
            async def close(self, interaction, _):
                await interaction.message.delete()

        # --------- detecção opcional do idioma do usuário ----------
        # Se quiser começar em inglês quando o Discord do usuário estiver em EN:
        start_lang = "en" if getattr(ctx.author, "locale", "pt").startswith("en") else "pt"

        # -------------------- ENVIO --------------------
        is_dm = isinstance(ctx.channel, discord.DMChannel)

        try:
            await ctx.message.delete()
        except Exception:
            pass

        try:
            first_embed = en_pages[0] if start_lang == "en" else pt_pages[0]
            await ctx.author.send(embed=first_embed, view=DocView(start_lang))
            if not is_dm:
                msg = "📨 Documentação enviada no privado!" if start_lang == "pt" else "📨 Documentation sent to your DMs!"
                await ctx.send(f"{ctx.author.mention} {msg}", delete_after=10)
        except discord.Forbidden:
            warn_pt = f"❌ {ctx.author.mention}, não consigo te enviar DM! Habilite mensagens diretas."
            warn_en = f"❌ {ctx.author.mention}, I can't DM you! Please enable direct messages."
            await ctx.send(warn_en if start_lang == "en" else warn_pt, delete_after=15)
