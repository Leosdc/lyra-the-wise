# views/sessao_views.py
"""Views (botões interativos) para o sistema de sessões de RPG."""

import discord
from discord.ui import View, Button
import random
from typing import Dict, Any, Callable
from discord.ext import commands


class RollRequestView(discord.ui.View):
    """Botões para rolar dados quando solicitado pela IA."""

    def __init__(self, bot, sessoes_ativas, salvar_dados, channel_id, roll_type, players_needed):
        super().__init__(timeout=300)  # 5 minutos para rolar
        self.bot = bot
        self.sessoes_ativas = sessoes_ativas
        self.salvar_dados = salvar_dados
        self.channel_id = channel_id
        self.roll_type = roll_type
        self.players_needed = players_needed
        self.rolls_done = {}
        self.action_chosen = None

    @discord.ui.button(label="🎲 Rolar Dados", style=discord.ButtonStyle.success, custom_id="roll_dice", row=0)
    async def roll_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Jogador rola os dados solicitados."""
        if interaction.user.id not in self.players_needed:
            return await interaction.response.send_message(
                "⚠️ Esta rolagem não é para você!",
                ephemeral=True
            )
        
        if interaction.user.id in self.rolls_done:
            return await interaction.response.send_message(
                f"✅ Você já rolou: **{self.rolls_done[interaction.user.id]}**",
                ephemeral=True
            )
        
        from rpg_core import rolar_dados
        texto, total = rolar_dados(self.roll_type)
        
        if total is None:
            return await interaction.response.send_message(
                f"❌ Erro ao processar rolagem: {texto}",
                ephemeral=True
            )
        
        self.rolls_done[interaction.user.id] = total
        
        await interaction.response.send_message(
            f"🎲 **{interaction.user.display_name}** rolou:\n{texto}",
            ephemeral=False
        )
        
        if len(self.rolls_done) >= len(self.players_needed):
            sessao = self.sessoes_ativas.get(self.channel_id)
            if sessao:
                for item in self.children:
                    item.disabled = True
                await interaction.message.edit(view=self)
                
                resumo_rolls = "\n".join([
                    f"• {interaction.guild.get_member(uid).display_name if interaction.guild.get_member(uid) else f'Jogador {uid}'}: **{resultado}**"
                    for uid, resultado in self.rolls_done.items()
                ])
                
                await interaction.channel.send(
                    embed=discord.Embed(
                        title="📊 Todas as Rolagens Concluídas!",
                        description=f"**Resultados:**\n{resumo_rolls}\n\n✨ *A história continua...*",
                        color=discord.Color.gold()
                    )
                )
                
                await self._continue_story(interaction.channel, sessao)
        else:
            faltam = len(self.players_needed) - len(self.rolls_done)
            await interaction.channel.send(
                f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} rolar..."
            )

    @discord.ui.button(label="🚫 Não Fazer Nada", style=discord.ButtonStyle.secondary, custom_id="do_nothing", row=0)
    async def do_nothing_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Jogador escolhe não realizar a ação."""
        sessao = self.sessoes_ativas.get(self.channel_id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id not in self.players_needed:
            return await interaction.response.send_message(
                "⚠️ Esta escolha não é para você!",
                ephemeral=True
            )
        
        # Marca que este jogador escolheu não fazer nada
        if not hasattr(self, 'players_skipped'):
            self.players_skipped = []
        
        if interaction.user.id in self.players_skipped:
            return await interaction.response.send_message(
                "✅ Você já escolheu não fazer nada.",
                ephemeral=True
            )
        
        self.players_skipped.append(interaction.user.id)
        
        fichas_sel = sessao.get("fichas", {})
        chave_ficha = fichas_sel.get(str(interaction.user.id)) or fichas_sel.get(interaction.user.id)
        if chave_ficha:
            nome_personagem = chave_ficha.split('_', 1)[-1].replace('_', ' ').title()
        else:
            nome_personagem = interaction.user.display_name
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="⏸️ Ação Cancelada",
                description=f"**{nome_personagem}** decidiu não realizar a ação.",
                color=discord.Color.orange()
            )
        )
        
        # Verifica se todos responderam (rolaram OU pularam)
        total_respostas = len(self.rolls_done) + len(self.players_skipped)
        if total_respostas >= len(self.players_needed):
            # Todos responderam - desabilita botões e continua
            for item in self.children:
                item.disabled = True
            await interaction.message.edit(view=self)
            
            # Prepara resumo
            resumo_parts = []
            for uid in self.players_needed:
                membro = interaction.guild.get_member(uid)
                nome = membro.display_name if membro else f"Jogador {uid}"
                
                if uid in self.rolls_done:
                    resumo_parts.append(f"• **{nome}**: Rolou {self.rolls_done[uid]}")
                elif uid in self.players_skipped:
                    resumo_parts.append(f"• **{nome}**: Não fez nada")
            
            await interaction.channel.send(
                embed=discord.Embed(
                    title="📊 Todos Responderam!",
                    description="\n".join(resumo_parts) + "\n\n✨ *A história continua...*",
                    color=discord.Color.gold()
                )
            )
            
            await self._continue_story_with_choices(interaction.channel, sessao)
        else:
            faltam = len(self.players_needed) - total_respostas
            await interaction.channel.send(
                f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} responder..."
            )
        
        from utils import chamar_groq, get_system_prompt
        sistema = sessao.get("sistema", "dnd5e")
        historia = sessao.get("historia", [])
        
        historia.append({
            "role": "user",
            "content": f"{nome_personagem} decidiu não realizar a ação sugerida. Narre como a situação evolui naturalmente."
        })
        
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
        ] + historia_recente
        
        estilo = sessao.get("estilo_narrativo", "extenso")
        max_tokens = 1200 if estilo == "extenso" else 600

        resposta = await chamar_groq(mensagens, max_tokens=max_tokens)
        
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        self.salvar_dados()
        
        embed = discord.Embed(
            title="📖 A História Continua...",
            description=resposta[:4000],
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Estilo: {estilo.upper()}")
        
        view = ContinueStoryView(
            self.bot,
            self.sessoes_ativas,
            self.salvar_dados,
            chamar_groq,
            get_system_prompt
        )
        await interaction.channel.send(embed=embed, view=view)

    @discord.ui.button(label="✏️ Outra Ação", style=discord.ButtonStyle.primary, custom_id="other_action", row=0)
    async def other_action_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Jogador escolhe fazer outra ação."""
        sessao = self.sessoes_ativas.get(self.channel_id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id not in self.players_needed:
            return await interaction.response.send_message(
                "⚠️ Esta opção não é para você!",
                ephemeral=True
            )
        
        # Marca que este jogador escolheu outra ação
        if not hasattr(self, 'players_other_action'):
            self.players_other_action = []
        
        if interaction.user.id in self.players_other_action:
            return await interaction.response.send_message(
                "✅ Você já escolheu fazer outra ação. Use `!acao <descrição>`",
                ephemeral=True
            )
        
        self.players_other_action.append(interaction.user.id)
        
        fichas_sel = sessao.get("fichas", {})
        chave_ficha = fichas_sel.get(str(interaction.user.id)) or fichas_sel.get(interaction.user.id)
        if chave_ficha:
            nome_personagem = chave_ficha.split('_', 1)[-1].replace('_', ' ').title()
        else:
            nome_personagem = interaction.user.display_name
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="✏️ Descreva Sua Ação",
                description=(
                    f"**{nome_personagem}**, use o comando `!acao <descrição>` para descrever o que seu personagem faz.\n\n"
                    "💡 **Exemplos:**\n"
                    "• `!acao examino a porta com cuidado`\n"
                    "• `!acao ataco o goblin com minha espada`\n"
                    "• `!acao tento persuadir o guarda`"
                ),
                color=discord.Color.blue()
            ),
            ephemeral=False
        )
        
        # Verifica se todos responderam (rolaram OU pularam OU escolheram outra ação)
        total_respostas = len(self.rolls_done) + len(getattr(self, 'players_skipped', [])) + len(self.players_other_action)
        if total_respostas >= len(self.players_needed):
            # Todos responderam - desabilita botões
            for item in self.children:
                item.disabled = True
            await interaction.message.edit(view=self)
            
            # Prepara resumo
            resumo_parts = []
            for uid in self.players_needed:
                membro = interaction.guild.get_member(uid)
                nome = membro.display_name if membro else f"Jogador {uid}"
                
                if uid in self.rolls_done:
                    resumo_parts.append(f"• **{nome}**: Rolou {self.rolls_done[uid]}")
                elif uid in getattr(self, 'players_skipped', []):
                    resumo_parts.append(f"• **{nome}**: Não fez nada")
                elif uid in self.players_other_action:
                    resumo_parts.append(f"• **{nome}**: Escolheu outra ação")
            
            await interaction.channel.send(
                embed=discord.Embed(
                    title="📊 Todos Responderam!",
                    description="\n".join(resumo_parts) + "\n\n⏳ *Aguardando ações alternativas com `!acao`...*",
                    color=discord.Color.blue()
                )
            )
            
            # Se houver rolagens, continua a história
            if self.rolls_done:
                await self._continue_story_with_choices(interaction.channel, sessao)
        else:
            faltam = len(self.players_needed) - total_respostas
            await interaction.channel.send(
                f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} responder..."
            )

    async def _continue_story(self, channel, sessao):
        """Continua a história após todas as rolagens."""
        from utils import chamar_groq, get_system_prompt
        
        sistema = sessao.get("sistema", "dnd5e")
        historia = sessao.get("historia", [])
        
        resumo_rolls = "\n".join([
            f"Jogador {uid} rolou: {resultado}"
            for uid, resultado in self.rolls_done.items()
        ])
        
        historia.append({
            "role": "user",
            "content": f"Resultados das rolagens ({self.roll_type}):\n{resumo_rolls}\n\nNarre as consequências destas rolagens de forma cinematográfica. Considere os valores obtidos e descreva o resultado de forma envolvente. 2-3 parágrafos."
        })
        
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
        ] + historia_recente
        
        estilo = sessao.get("estilo_narrativo", "extenso")
        max_tokens = 1200 if estilo == "extenso" else 500

        resposta = await chamar_groq(mensagens, max_tokens=max_tokens)
        
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        self.salvar_dados()
        
        embed = discord.Embed(
            title="📖 A História Continua...",
            description=resposta[:4000],
            color=discord.Color.gold()
        )
        
        view = ContinueStoryView(
            self.bot,
            self.sessoes_ativas,
            self.salvar_dados,
            chamar_groq,
            get_system_prompt
        )
        await channel.send(embed=embed, view=view)
    
    async def _continue_story_with_choices(self, channel, sessao):
        """Continua a história considerando TODAS as escolhas dos jogadores."""
        from utils import chamar_groq, get_system_prompt
        
        sistema = sessao.get("sistema", "dnd5e")
        historia = sessao.get("historia", [])
        
        # Monta resumo de TODAS as escolhas
        resumo_parts = []
        
        for uid in self.players_needed:
            membro = channel.guild.get_member(uid)
            nome = membro.display_name if membro else f"Jogador {uid}"
            
            if uid in self.rolls_done:
                resumo_parts.append(f"- {nome} rolou {self.roll_type}: {self.rolls_done[uid]}")
            elif uid in getattr(self, 'players_skipped', []):
                resumo_parts.append(f"- {nome} decidiu não realizar a ação")
            elif uid in getattr(self, 'players_other_action', []):
                resumo_parts.append(f"- {nome} escolheu fazer outra ação (aguardando descrição)")
        
        resumo_completo = "\n".join(resumo_parts)
        
        historia.append({
            "role": "user",
            "content": f"Escolhas dos jogadores:\n{resumo_completo}\n\nNarre as consequências destas escolhas de forma cinematográfica. Considere quem agiu e quem não agiu. 2-3 parágrafos."
        })
        
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
        ] + historia_recente
        
        estilo = sessao.get("estilo_narrativo", "extenso")
        max_tokens = 1200 if estilo == "extenso" else 500

        resposta = await chamar_groq(mensagens, max_tokens=max_tokens)
        
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        self.salvar_dados()
        
        embed = discord.Embed(
            title="📖 A História Continua...",
            description=resposta[:4000],
            color=discord.Color.gold()
        )
        
        view = ContinueStoryView(
            self.bot,
            self.sessoes_ativas,
            self.salvar_dados,
            chamar_groq,
            get_system_prompt
        )
        await channel.send(embed=embed, view=view)


class NarrativeStyleView(discord.ui.View):
    """View para o mestre escolher o estilo narrativo da Lyra."""

    def __init__(self, bot: commands.Bot, sessao_store: Dict[int, Dict[str, Any]], salvar_dados_cb, chamar_groq_cb, get_system_prompt_cb, channel_id: int):
        super().__init__(timeout=60)
        self.bot = bot
        self.sessoes_ativas = sessao_store
        self.salvar_dados = salvar_dados_cb
        self.chamar_groq = chamar_groq_cb
        self.get_system_prompt = get_system_prompt_cb
        self.channel_id = channel_id

    @discord.ui.button(label="📖 Narrativa Extensa", style=discord.ButtonStyle.primary, custom_id="narrative_long")
    async def narrative_long(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Narrativa detalhada e imersiva (3-5 parágrafos)."""
        sessao = self.sessoes_ativas.get(self.channel_id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode escolher o estilo narrativo.", ephemeral=True)
        
        sessao["estilo_narrativo"] = "extenso"
        self.salvar_dados()
        
        await interaction.response.send_message(
            "✅ **Estilo Narrativo Definido: EXTENSO**\n\n"
            "📖 Lyra contará histórias detalhadas e imersivas, com:\n"
            "• 3-5 parágrafos completos\n"
            "• Descrições ricas dos 5 sentidos\n"
            "• Narrativa cinematográfica e atmosférica\n"
            "• Maior profundidade emocional e contextual\n\n"
            "💡 *Ideal para sessões focadas em roleplay e imersão.*",
            ephemeral=False
        )
        await self._start_adventure(interaction)

    @discord.ui.button(label="📝 Narrativa Concisa", style=discord.ButtonStyle.secondary, custom_id="narrative_short")
    async def narrative_short(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Narrativa objetiva e direta (1-2 parágrafos)."""
        sessao = self.sessoes_ativas.get(self.channel_id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode escolher o estilo narrativo.", ephemeral=True)
        
        sessao["estilo_narrativo"] = "conciso"
        self.salvar_dados()
        
        await interaction.response.send_message(
            "✅ **Estilo Narrativo Definido: CONCISO**\n\n"
            "📝 Lyra será objetiva e direta, com:\n"
            "• 1-2 parágrafos curtos\n"
            "• Foco em ação e informação essencial\n"
            "• Narrativa ágil e dinâmica\n"
            "• Respostas mais rápidas\n\n"
            "💡 *Ideal para sessões focadas em combate e progressão rápida.*",
            ephemeral=False
        )
        await self._start_adventure(interaction)

    async def _start_adventure(self, interaction: discord.Interaction):
        """Inicia a aventura após escolha do estilo narrativo."""
        sessao = self.sessoes_ativas.get(self.channel_id)
        from config import fichas_personagens
        
        sistema = sessao.get("sistema", "dnd5e")
        estilo = sessao.get("estilo_narrativo", "extenso")
        fichas = sessao.get("fichas", {})
        
        if estilo == "extenso":
            max_tokens = 1500
            instrucao_tamanho = "3-5 parágrafos completos e detalhados"
            instrucao_estilo = "Seja MUITO descritiva, imersiva e cinematográfica. Use linguagem evocativa, apele aos 5 sentidos, crie atmosfera profunda."
        else:
            max_tokens = 600
            instrucao_tamanho = "1-2 parágrafos curtos e diretos"
            instrucao_estilo = "Seja objetiva e concisa. Foque no essencial: situação, desafio imediato e gancho para ação."
        
        prompt_intro = f"Gere uma introdução épica para a sessão de RPG, apresentando o cenário, tom e conexões entre os personagens. {instrucao_tamanho}. {instrucao_estilo} Termine com um gancho claro para a primeira cena.\n\nPersonagens:\n"
        
        for uid, chave in fichas.items():
            ficha_info = fichas_personagens.get(chave, {})
            nome_personagem = ficha_info.get('nome', 'Personagem Desconhecido')
            conteudo = ficha_info.get('conteudo', '')
            resumo = conteudo[:200] + "..." if len(conteudo) > 200 else conteudo
            prompt_intro += f"- **{nome_personagem}**: {resumo}\n"
        
        mensagens = [
            {"role": "system", "content": self.get_system_prompt(sistema)},
            {"role": "user", "content": prompt_intro}
        ]
        
        await interaction.channel.send("🎬 *Lyra está tecendo a história...*")
        intro = await self.chamar_groq(mensagens, max_tokens=max_tokens)
        
        sessao["status"] = "em_andamento"
        sessao["historia"] = [
            {"role": "system", "content": self.get_system_prompt(sistema)},
            {"role": "assistant", "content": intro}
        ]
        self.salvar_dados()
        
        embed = discord.Embed(
            title="🎬 Aventura Iniciada!",
            description=intro[:4000],
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Estilo Narrativo: {estilo.upper()}")
        
        continue_view = ContinueStoryView(
            self.bot,
            self.sessoes_ativas,
            self.salvar_dados,
            self.chamar_groq,
            self.get_system_prompt
        )
        await interaction.channel.send(embed=embed, view=continue_view)


class ContinueStoryView(discord.ui.View):
    """Botões para continuar a narrativa após cada resposta da IA."""

    def __init__(self, bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt):
        super().__init__(timeout=None)
        self.bot = bot
        self.sessoes_ativas = sessoes_ativas
        self.salvar_dados = salvar_dados
        self.chamar_groq = chamar_groq
        self.get_system_prompt = get_system_prompt

    @discord.ui.button(label="🎬 Continuar História", style=discord.ButtonStyle.primary, custom_id="continue_story", row=0)
    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para o mestre continuar a narrativa."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message(
                "⚠️ Use o comando `!acao` para descrever o que seu personagem faz!",
                ephemeral=True
            )
        
        await interaction.response.send_message(
            "📝 **Descreva a próxima cena ou acontecimento:**\n"
            "Use o comando `!cenanarrada <descrição>` ou aguarde as ações dos jogadores com `!acao`.",
            ephemeral=True
        )

    @discord.ui.button(label="⚔️ Rolar Iniciativa", style=discord.ButtonStyle.success, custom_id="roll_initiative", row=0)
    async def initiative_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Mestre rola iniciativa para todos os jogadores."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message(
                "⚠️ Apenas o **mestre** pode rolar iniciativa!",
                ephemeral=True
            )
        
        from config import fichas_personagens
        
        jogadores = sessao.get("jogadores", [])
        fichas_sel = sessao.get("fichas", {})
        
        resultados = {}
        
        for jogador_id in jogadores:
            membro = interaction.guild.get_member(jogador_id)
            if not membro:
                continue
            
            chave_ficha = fichas_sel.get(str(jogador_id)) or fichas_sel.get(jogador_id)
            if chave_ficha:
                nome = chave_ficha.split('_', 1)[-1].replace('_', ' ').title()
            else:
                nome = membro.display_name
            
            iniciativa = random.randint(1, 20) + random.randint(1, 4)
            resultados[nome] = iniciativa
        
        ranking = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        
        texto = "⚔️ **Ordem de Iniciativa:**\n\n"
        for i, (nome, valor) in enumerate(ranking, start=1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            texto += f"{emoji} **{nome}** → {valor}\n"
        
        embed = discord.Embed(
            title="⚔️ Iniciativa Rolada!",
            description=texto,
            color=discord.Color.red()
        )
        embed.set_footer(text="Os jogadores agem nesta ordem. Use !acao para descrever suas ações.")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
        
        historia = sessao.get("historia", [])
        historia.append({
            "role": "user",
            "content": f"Ordem de iniciativa estabelecida: {', '.join([f'{nome} ({valor})' for nome, valor in ranking])}"
        })
        sessao["historia"] = historia
        self.salvar_dados()


class SessionControlView(discord.ui.View):
    """Botões de controle principal da sessão."""

    def __init__(self, bot: commands.Bot, sessao_store: Dict[int, Dict[str, Any]], salvar_dados_cb, chamar_groq_cb, get_system_prompt_cb, timeout=None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.sessoes_ativas = sessao_store
        self.salvar_dados = salvar_dados_cb
        self.chamar_groq = chamar_groq_cb
        self.get_system_prompt = get_system_prompt_cb

    def _get_sessao(self, channel_id: int):
        return self.sessoes_ativas.get(channel_id)

    def _is_mestre(self, user_id: int, sessao: Dict[str, Any]) -> bool:
        return sessao and sessao.get("mestre_id") == user_id

    @discord.ui.button(label="🎬 Iniciar Aventura", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        sessao = self._get_sessao(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada neste canal.", ephemeral=True)

        if not self._is_mestre(interaction.user.id, sessao):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode iniciar a aventura.", ephemeral=True)

        # VALIDAÇÃO DE FICHAS RESTAURADA
        jogadores = sessao.get("jogadores", [])
        fichas = sessao.get("fichas", {})
        faltando = [uid for uid in jogadores if str(uid) not in fichas and uid not in fichas]
        
        if faltando:
            from core.sessao_helpers import user_mention
            faltantes_txt = ", ".join([user_mention(interaction.guild, uid) for uid in faltando])
            return await interaction.response.send_message(
                f"⏳ Ainda faltam fichas: {faltantes_txt}",
                ephemeral=True
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="📖 Escolha o Estilo Narrativo",
                description=(
                    "Como você quer que **Lyra, a Sábia** conte a história?\n\n"
                    "**📖 Narrativa Extensa:**\n"
                    "• 3-5 parágrafos detalhados\n"
                    "• Descrições ricas e imersivas\n"
                    "• Ideal para roleplay e exploração\n\n"
                    "**📝 Narrativa Concisa:**\n"
                    "• 1-2 parágrafos objetivos\n"
                    "• Foco em ação e progressão\n"
                    "• Ideal para combate e ritmo rápido"
                ),
                color=discord.Color.gold()
            ).set_footer(text="Escolha abaixo o estilo que preferir"),
            view=NarrativeStyleView(
                self.bot,
                self.sessoes_ativas,
                self.salvar_dados,
                self.chamar_groq,
                self.get_system_prompt,
                interaction.channel.id
            ),
            ephemeral=False
        )

    @discord.ui.button(label="📊 Ver Fichas", style=discord.ButtonStyle.primary)
    async def fichas_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        sessao = self._get_sessao(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada neste canal.", ephemeral=True)

        import json
        import os
        DATA_DIR = os.path.join(os.getcwd(), "bot_data")
        FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")
        
        fichas_atualizadas = {}
        try:
            if os.path.exists(FICHAS_PATH):
                with open(FICHAS_PATH, "r", encoding="utf-8") as f:
                    fichas_atualizadas = json.load(f)
        except Exception as e:
            print(f"⚠️ Erro ao recarregar fichas no botão: {e}")

        from core.sessao_helpers import user_mention
        jogadores = sessao.get("jogadores", [])
        fichas_sel = sessao.get("fichas", {})
        sistema = sessao.get("sistema", "dnd5e")
        status = sessao.get("status", "preparando")
        mestre_id = sessao.get("mestre_id")
        mestre_txt = user_mention(interaction.guild, mestre_id)

        jogadores_txt = []
        for uid in jogadores:
            if str(uid) in fichas_sel or uid in fichas_sel:
                chave_ficha = fichas_sel.get(str(uid)) or fichas_sel.get(uid)
                ficha_info = fichas_atualizadas.get(chave_ficha, {})
                nome_ficha = ficha_info.get('nome', 'Ficha Desconhecida')
                jogadores_txt.append(f"• {user_mention(interaction.guild, uid)} — ✅ **{nome_ficha}**")
            else:
                jogadores_txt.append(f"• {user_mention(interaction.guild, uid)} — ⏳ sem ficha")

        embed = discord.Embed(
            title="🎮 Status da Sessão",
            description=f"**Sistema**: `{sistema}`\n**Status**: **{status.upper()}**\n**Mestre**: {mestre_txt}",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="👥 Jogadores e Fichas", 
            value="\n".join(jogadores_txt) if jogadores_txt else "—", 
            inline=False
        )
        embed.set_footer(text="Use !verficha <nome> para ver detalhes de uma ficha")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🚪 Encerrar Sessão", style=discord.ButtonStyle.danger)
    async def end_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        sessao = self._get_sessao(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)

        if not self._is_mestre(interaction.user.id, sessao):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode encerrar.", ephemeral=True)

        await interaction.response.send_message("⚠️ Encerrando sessão e movendo jogadores para a Torre da Maga...", ephemeral=False)
        
        guild = interaction.guild
        
        # RESTAURADO: Busca Torre da Maga
        torre_da_maga = None
        for channel in guild.voice_channels:
            if "torre" in channel.name.lower() and "maga" in channel.name.lower():
                torre_da_maga = channel
                break
        
        # RESTAURADO: Move jogadores de volta
        canal_voz_id = sessao.get("voice_channel_id")
        if canal_voz_id:
            canal_voz = guild.get_channel(canal_voz_id)
            if canal_voz and isinstance(canal_voz, discord.VoiceChannel):
                for member in canal_voz.members:
                    if torre_da_maga:
                        try:
                            await member.move_to(torre_da_maga)
                            print(f"✅ {member.name} movido para Torre da Maga")
                        except Exception as e:
                            print(f"⚠️ Erro ao mover {member.name}: {e}")
        
        import asyncio
        await asyncio.sleep(3)
        
        try:
            # Remove dos dados
            self.sessoes_ativas.pop(interaction.channel.id, None)
            self.salvar_dados()
            
            # RESTAURADO: Deleta canal de voz primeiro
            if canal_voz_id:
                canal_voz = guild.get_channel(canal_voz_id)
                if canal_voz:
                    await canal_voz.delete(reason="Sessão encerrada pelo mestre (botão).")
            
            # Deleta canal de texto
            await interaction.channel.delete(reason="Sessão encerrada pelo mestre (botão).")
        except Exception as e:
            print(f"❌ Erro ao encerrar sessão: {e}")