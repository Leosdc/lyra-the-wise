# views/sessao_roll_views.py
"""Views para gerenciar solicitações de rolagem de dados."""

import discord
from discord.ui import View, Button
from typing import Dict, Any
from discord.ext import commands

# Import da função de rolagem do módulo correto
from commands.dados import rolar_dados


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
        
        texto, total = rolar_dados(self.roll_type)
        
        if total is None:
            return await interaction.response.send_message(
                f"❌ Erro ao processar rolagem: {texto}",
                ephemeral=True
            )
        
        self.rolls_done[interaction.user.id] = total
        
        
        # Registra no estado global da sessão para sincronizar com !acao
        sessao = self.sessoes_ativas.get(self.channel_id)
        if sessao:
            if "rolls_done_ids" not in sessao:
                sessao["rolls_done_ids"] = []
            sessao["rolls_done_ids"].append(interaction.user.id)
            sessao["players_needed_action"] = self.players_needed
            self.salvar_dados()
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
                f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} rolar...\n"
                f"💡 *Ou use `!acao <descrição>` para fazer outra coisa*"
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
        
        
        # Registra no estado global da sessão
        if "players_skipped_ids" not in sessao:
            sessao["players_skipped_ids"] = []
        sessao["players_skipped_ids"].append(interaction.user.id)
        sessao["players_needed_action"] = self.players_needed
        self.salvar_dados()
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

    async def _continue_story(self, channel, sessao):
        """Continua a história após todas as rolagens."""
        from views.sessao_continue_views import ContinueStoryView
        from utils import chamar_groq, get_system_prompt
        
        sistema = sessao.get("sistema", "dnd5e")
        historia = sessao.get("historia", [])
        estilo = sessao.get("estilo_narrativo", "extenso")  
        
        resumo_rolls = "\n".join([
            f"Jogador {uid} rolou: {resultado}"
            for uid, resultado in self.rolls_done.items()
        ])
        
        if estilo == "extenso":
            instrucao = "Narre as consequências de forma cinematográfica. 2-3 parágrafos completos."
        else:
            instrucao = "MÁXIMO 4 FRASES CURTAS E DIRETAS. Foque apenas no resultado essencial das rolagens."

        historia.append({
            "role": "user",
            "content": f"Resultados das rolagens ({self.roll_type}):\n{resumo_rolls}\n\n{instrucao}"
        })
        
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
        ] + historia_recente
        
        max_tokens = 1200 if estilo == "extenso" else 400

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
        """Continua a história considerando TODAS as escolhas dos jogadores (rolls, skip, ações alternativas)."""
        from views.sessao_continue_views import ContinueStoryView
        from utils import chamar_groq, get_system_prompt
        
        sistema = sessao.get("sistema", "dnd5e")
        historia = sessao.get("historia", [])
        estilo = sessao.get("estilo_narrativo", "extenso")  
        
        # Monta resumo DETALHADO de TODAS as escolhas
        resumo_parts = []
        fichas_sel = sessao.get("fichas", {})
        
        for uid in self.players_needed:
            membro = channel.guild.get_member(uid)
            nome = membro.display_name if membro else f"Jogador {uid}"
            
            # Busca nome do personagem
            chave_ficha = fichas_sel.get(str(uid)) or fichas_sel.get(uid)
            if chave_ficha:
                nome_personagem = chave_ficha.split('_', 1)[-1].replace('_', ' ').title()
            else:
                nome_personagem = nome
            
            if uid in self.rolls_done:
                resumo_parts.append(f"- {nome_personagem} rolou {self.roll_type} e obteve: {self.rolls_done[uid]}")
            elif uid in getattr(self, 'players_skipped', []):
                resumo_parts.append(f"- {nome_personagem} decidiu NÃO realizar a ação proposta e permaneceu imóvel/inativo")
            elif uid in sessao.get("acoes_pendentes", {}):
                acao_alternativa = sessao["acoes_pendentes"][uid]
                resumo_parts.append(f"- {nome_personagem} ignorou a ação sugerida e fez outra coisa: {acao_alternativa}")
        
        resumo_completo = "\n".join(resumo_parts)
        
        if estilo == "extenso":
            instrucao_narrativa = "Seja específico sobre o impacto de cada escolha. 2-3 parágrafos cinematográficos."
        else:
            instrucao_narrativa = "MÁXIMO 5 FRASES CURTAS. Seja direto: o que aconteceu com quem agiu e com quem não agiu."

        historia.append({
            "role": "user",
            "content": (
                f"Escolhas dos jogadores sobre a situação anterior:\n{resumo_completo}\n\n"
                f"INSTRUÇÃO CRÍTICA: Narre as consequências considerando:\n"
                f"1. Quem AGIU e obteve resultados (considere os valores das rolagens)\n"
                f"2. Quem NÃO FEZ NADA e as consequências dessa INAÇÃO (ex: perdeu oportunidade, foi pego de surpresa, etc)\n"
                f"3. Quem fez AÇÕES ALTERNATIVAS diferentes do sugerido\n\n"
                f"{instrucao_narrativa}"
            )
        })
        
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
        ] + historia_recente
        
        max_tokens = 1200 if estilo == "extenso" else 400

        resposta = await chamar_groq(mensagens, max_tokens=max_tokens)
        
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        
        # Limpa ações pendentes
        sessao["acoes_pendentes"] = {}
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
