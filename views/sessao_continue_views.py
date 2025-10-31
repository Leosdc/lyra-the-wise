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
