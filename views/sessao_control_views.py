# views/sessao_control_views.py
"""Views de controle principal da sessão (iniciar, encerrar, status)."""

import discord
from discord.ui import View, Button
from typing import Dict, Any
from discord.ext import commands


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
        from views.sessao_continue_views import ContinueStoryView
        
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
        
        # Busca Torre da Maga
        torre_da_maga = None
        for channel in guild.voice_channels:
            if "torre" in channel.name.lower() and "maga" in channel.name.lower():
                torre_da_maga = channel
                break
        
        # Move jogadores de volta
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
            
            # Deleta canal de voz primeiro
            if canal_voz_id:
                canal_voz = guild.get_channel(canal_voz_id)
                if canal_voz:
                    await canal_voz.delete(reason="Sessão encerrada pelo mestre (botão).")
            
            # Deleta canal de texto
            await interaction.channel.delete(reason="Sessão encerrada pelo mestre (botão).")
        except Exception as e:
            print(f"❌ Erro ao encerrar sessão: {e}")
