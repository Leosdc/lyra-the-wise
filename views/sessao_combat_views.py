# views/sessao_combat_views.py
"""Views para controle de combate nas sessões."""

import discord
from discord.ui import View, Button
from typing import Dict, Any


class CombatControlView(discord.ui.View):
    """
    Botões de controle de combate.
    Aparece APENAS quando há combate ativo.
    """

    def __init__(self, bot, sessoes_ativas, salvar_dados):
        super().__init__(timeout=None)
        self.bot = bot
        self.sessoes_ativas = sessoes_ativas
        self.salvar_dados = salvar_dados

    @discord.ui.button(label="⚔️ Rolar Iniciativa", style=discord.ButtonStyle.success, custom_id="combat_initiative", row=0)
    async def initiative_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Mestre rola iniciativa para combate."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message(
                "⚠️ Apenas o **mestre** pode rolar iniciativa!",
                ephemeral=True
            )
        
        combat = sessao.get("combat")
        if not combat:
            return await interaction.response.send_message(
                "⚠️ Nenhum combate ativo! Use `!iniciarcombate` primeiro.",
                ephemeral=True
            )
        
        # Rola iniciativa
        turn_order = combat.roll_initiative()
        self.salvar_dados()
        
        # Formata resultado
        texto = "⚔️ **Ordem de Iniciativa:**\n\n"
        for i, (cid, nome, valor) in enumerate(turn_order, start=1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            tipo = combat.combatants[cid]["type"]
            icone = "👤" if tipo == "player" else "👹"
            texto += f"{emoji} {icone} **{nome}** → {valor}\n"
        
        embed = discord.Embed(
            title="⚔️ Iniciativa Rolada!",
            description=texto,
            color=discord.Color.red()
        )
        embed.set_footer(text="O combate começou! Use !atacar, !curar, !proximoturno")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
        
        # Mostra status inicial
        await interaction.channel.send(embed=combat.get_status_embed())
    
    @discord.ui.button(label="📊 Status Combate", style=discord.ButtonStyle.primary, custom_id="combat_status", row=0)
    async def status_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Mostra status atual do combate."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        combat = sessao.get("combat")
        if not combat:
            return await interaction.response.send_message(
                "⚠️ Nenhum combate ativo no momento.",
                ephemeral=True
            )
        
        embed = combat.get_status_embed()
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    @discord.ui.button(label="⏭️ Próximo Turno", style=discord.ButtonStyle.secondary, custom_id="combat_next", row=1)
    async def next_turn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Avança para o próximo turno."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message(
                "⚠️ Apenas o **mestre** pode avançar turnos!",
                ephemeral=True
            )
        
        combat = sessao.get("combat")
        if not combat or not combat.is_active:
            return await interaction.response.send_message(
                "⚠️ Nenhum combate ativo.",
                ephemeral=True
            )
        
        next_id, next_name = combat.next_turn()
        self.salvar_dados()
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"⏭️ Próximo Turno — Rodada {combat.round_number}",
                description=f"É a vez de **{next_name}**!",
                color=discord.Color.blue()
            ),
            ephemeral=False
        )
        
        # Mostra status atualizado
        await interaction.channel.send(embed=combat.get_status_embed())
    
    @discord.ui.button(label="🏁 Encerrar Combate", style=discord.ButtonStyle.danger, custom_id="combat_end", row=1)
    async def end_combat_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Encerra combate manualmente."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message(
                "⚠️ Apenas o **mestre** pode encerrar combate!",
                ephemeral=True
            )
        
        combat = sessao.get("combat")
        if not combat:
            return await interaction.response.send_message(
                "⚠️ Nenhum combate ativo.",
                ephemeral=True
            )
        
        # Atualiza HP das fichas
        from config import fichas_personagens
        fichas_sel = sessao.get("fichas", {})
        
        for jogador_id in sessao.get("jogadores", []):
            if jogador_id in combat.combatants:
                player_data = combat.combatants[jogador_id]
                chave_ficha = fichas_sel.get(str(jogador_id)) or fichas_sel.get(jogador_id)
                
                if chave_ficha and chave_ficha in fichas_personagens:
                    ficha = fichas_personagens[chave_ficha]
                    if "secoes" in ficha and ficha["secoes"]:
                        recursos = ficha["secoes"].get("recursos", {})
                        recursos["HP Atual"] = player_data["hp_current"]
        
        # Remove combate
        sessao.pop("combat", None)
        self.salvar_dados()
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🏁 Combate Encerrado",
                description="✅ HP dos jogadores atualizado nas fichas.\n\n💡 A aventura continua...",
                color=discord.Color.gold()
            ),
            ephemeral=False
        )


def should_show_combat_buttons(sessao: Dict[str, Any]) -> bool:
    """
    Determina se os botões de combate devem ser exibidos.
    Retorna True se houver combate ativo.
    """
    return sessao.get("combat") is not None
