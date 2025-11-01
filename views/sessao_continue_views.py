# views/sessao_continue_views.py
"""Views para continuar a narrativa após respostas da IA."""

import discord
from discord.ui import View, Button
import random
from typing import Dict, Any
from discord.ext import commands


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