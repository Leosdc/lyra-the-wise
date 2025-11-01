# views/sessao_master_control_views.py
"""
Botões de controle EXCLUSIVOS DO MESTRE.
Mestre escolhe quais fichas participam e que ações tomar.
"""

import discord
from discord.ui import View, Button, Select
from typing import Dict, Any


class PlayerSelectionView(discord.ui.View):
    """View para mestre selecionar quais jogadores participam da cena."""
    
    def __init__(self, bot, sessao, guild, callback_action):
        super().__init__(timeout=60)
        self.bot = bot
        self.sessao = sessao
        self.guild = guild
        self.callback_action = callback_action
        self.selected_players = []
        
        # Adiciona select com jogadores
        options = []
        for player_id in sessao.get("jogadores", []):
            member = guild.get_member(player_id)
            if member:
                options.append(discord.SelectOption(
                    label=member.display_name,
                    value=str(player_id),
                    description=f"Jogador: {member.name}"
                ))
        
        if options:
            select = Select(
                placeholder="Escolha os jogadores desta cena...",
                options=options,
                min_values=1,
                max_values=len(options),
                custom_id="player_select"
            )
            select.callback = self.player_select_callback
            self.add_item(select)
    
    async def player_select_callback(self, interaction: discord.Interaction):
        """Callback quando jogadores são selecionados."""
        self.selected_players = [int(val) for val in interaction.data["values"]]
        
        await interaction.response.send_message(
            f"✅ **{len(self.selected_players)} jogador(es) selecionado(s)!**\n"
            f"Clique em 'Confirmar' para executar a ação.",
            ephemeral=True
        )
    
    @discord.ui.button(label="✅ Confirmar", style=discord.ButtonStyle.success)
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        """Confirma seleção e executa ação."""
        if not self.selected_players:
            return await interaction.response.send_message(
                "⚠️ Selecione pelo menos 1 jogador!",
                ephemeral=True
            )
        
        await self.callback_action(interaction, self.selected_players)
        
        # Desabilita view
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
    
    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
    async def cancel_button(self, interaction: discord.Interaction, button: Button):
        """Cancela seleção."""
        await interaction.response.send_message("❌ Ação cancelada.", ephemeral=True)
        await interaction.message.delete()


class MasterControlView(discord.ui.View):
    """Botões de controle do mestre após cada narrativa."""
    
    def __init__(self, bot, sessoes_ativas, fichas_personagens, chamar_groq, get_system_prompt, salvar_dados):
        super().__init__(timeout=None)
        self.bot = bot
        self.sessoes_ativas = sessoes_ativas
        self.fichas_personagens = fichas_personagens
        self.chamar_groq = chamar_groq
        self.get_system_prompt = get_system_prompt
        self.salvar_dados = salvar_dados
    
    @discord.ui.button(label="🎲 Solicitar Rolagens", style=discord.ButtonStyle.primary, row=0)
    async def request_rolls_button(self, interaction: discord.Interaction, button: Button):
        """Mestre escolhe jogadores e tipo de rolagem."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode solicitar rolagens!", ephemeral=True)
        
        # Modal para definir tipo de rolagem
        from discord.ui import Modal, TextInput
        
        class RollModal(Modal, title="Solicitar Rolagem de Dados"):
            roll_type = TextInput(
                label="Tipo de Rolagem",
                placeholder="Ex: 1d20+3, 2d6, 3d8+5",
                required=True,
                max_length=50
            )
            
            def __init__(self, parent_view):
                super().__init__()
                self.parent_view = parent_view
            
            async def on_submit(self, interaction: discord.Interaction):
                roll_expr = self.roll_type.value.strip()
                
                await interaction.response.send_message(
                    f"📊 **Rolagem definida:** `{roll_expr}`\n"
                    f"Agora selecione os jogadores que devem rolar:",
                    ephemeral=True
                )
                
                # Mostra seleção de jogadores
                async def execute_roll_request(inter, selected_players):
                    from views.sessao_roll_views import RollRequestView
                    
                    jogadores_nomes = [
                        inter.guild.get_member(uid).mention 
                        for uid in selected_players 
                        if inter.guild.get_member(uid)
                    ]
                    
                    roll_embed = discord.Embed(
                        title="🎲 Rolagem Solicitada!",
                        description=(
                            f"**Tipo:** `{roll_expr}`\n"
                            f"**Jogadores:** {', '.join(jogadores_nomes)}\n\n"
                            f"Clique nos botões abaixo para rolar ou usar `!acao`"
                        ),
                        color=discord.Color.blue()
                    )
                    
                    view = RollRequestView(
                        self.parent_view.bot,
                        self.parent_view.sessoes_ativas,
                        self.parent_view.salvar_dados,
                        inter.channel.id,
                        roll_expr,
                        selected_players
                    )
                    
                    await inter.response.send_message(embed=roll_embed, view=view)
                
                view = PlayerSelectionView(
                    self.parent_view.bot,
                    self.parent_view.sessoes_ativas[interaction.channel.id],
                    interaction.guild,
                    execute_roll_request
                )
                
                await interaction.channel.send(
                    "👥 **Mestre, selecione os jogadores:**",
                    view=view
                )
        
        modal = RollModal(self)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="⚔️ Iniciar Combate", style=discord.ButtonStyle.danger, row=0)
    async def start_combat_button(self, interaction: discord.Interaction, button: Button):
        """Inicia combate manualmente."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode iniciar combate!", ephemeral=True)
        
        # Executar comando !iniciarcombate
        channel = interaction.channel
        ctx = await self.bot.get_context(interaction.message)
        ctx.author = interaction.user
        ctx.channel = channel
        
        comando = self.bot.get_command("iniciarcombate")
        if comando:
            await ctx.invoke(comando)
            await interaction.response.send_message("✅ Combate iniciado!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Comando de combate não encontrado!", ephemeral=True)
    
    @discord.ui.button(label="📊 Status Geral", style=discord.ButtonStyle.secondary, row=1)
    async def status_button(self, interaction: discord.Interaction, button: Button):
        """Mostra status de todos os jogadores."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode ver status!", ephemeral=True)
        
        fichas_sel = sessao.get("fichas", {})
        descricao = ""
        
        for uid in sessao.get("jogadores", []):
            member = interaction.guild.get_member(uid)
            if not member:
                continue
            
            chave = fichas_sel.get(str(uid)) or fichas_sel.get(uid)
            if not chave or chave not in self.fichas_personagens:
                descricao += f"• {member.mention} — ⚠️ Sem ficha\n"
                continue
            
            ficha = self.fichas_personagens[chave]
            nome = ficha.get("nome", member.display_name)
            
            # Extrai stats
            secoes = ficha.get("secoes", {})
            recursos = secoes.get("recursos", {})
            combate = secoes.get("combate", {})
            
            hp_atual = recursos.get("HP Atual", "?")
            hp_max = recursos.get("HP Máximo", "?")
            ca = combate.get("CA", "?")
            
            descricao += f"• **{nome}** ({member.mention})\n"
            descricao += f"  HP: {hp_atual}/{hp_max} | CA: {ca}\n\n"
        
        embed = discord.Embed(
            title="📊 Status dos Jogadores",
            description=descricao or "Nenhum jogador com ficha válida.",
            color=discord.Color.gold()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="📖 Ver Ações Pendentes", style=discord.ButtonStyle.secondary, row=1)
    async def view_actions_button(self, interaction: discord.Interaction, button: Button):
        """Mostra ações declaradas pelos jogadores."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message("⚠️ Apenas o **mestre** pode ver ações!", ephemeral=True)
        
        acoes = sessao.get("acoes_pendentes", {})
        
        if not acoes:
            return await interaction.response.send_message("✅ Não há ações pendentes.", ephemeral=True)
        
        descricao = ""
        for uid, info in acoes.items():
            descricao += f"• **{info['nome']}**: {info['acao']}\n\n"
        
        embed = discord.Embed(
            title="📋 Ações Declaradas",
            description=descricao[:4000],
            color=discord.Color.blue()
        )
        embed.set_footer(text="Use !narrativa para narrar as consequências")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
