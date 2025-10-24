# sessoes_rpg.py
# Sistema de sessões privadas de RPG com rolagens interativas
# NOVO: IA solicita rolagens automaticamente durante a aventura!

from __future__ import annotations

import discord
from discord.ext import commands
from typing import Dict, List, Optional, Any
import asyncio
import datetime
import re

# -----------------------------
# Estrutura de sessão
# -----------------------------
# sessoes_ativas[channel_id] = {
#   "guild_id": int,
#   "channel_id": int,
#   "categoria_id": Optional[int],
#   "mestre_id": int,
#   "jogadores": List[int],
#   "fichas": {user_id: chave_ficha},
#   "status": "preparando" | "em_andamento" | "pausada",
#   "sistema": "dnd5e" | "cthulhu" | ...,
#   "criada_em": iso_str,
#   "historia": List[Dict] - mantém contexto da aventura
# }

SESSOES_CATEGORY_NAME = "🎲 Sessões RPG"


# -----------------------------
# Helpers
# -----------------------------

def _user_mention(guild: discord.Guild, user_id: int) -> str:
    member = guild.get_member(user_id)
    return member.mention if member else f"<@{user_id}>"


def _coletar_fichas_usuario(fichas_personagens: Dict[str, Any], user_id: int) -> List[Dict[str, Any]]:
    """Retorna a lista de fichas (dict) do usuário - APENAS FICHAS VÁLIDAS."""
																	  
    import json
    import os
    DATA_DIR = os.path.join(os.getcwd(), "bot_data")
    FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")
    
    try:
        if os.path.exists(FICHAS_PATH):
            with open(FICHAS_PATH, "r", encoding="utf-8") as f:
                fichas_do_arquivo = json.load(f)
                fichas_personagens.clear()
                fichas_personagens.update(fichas_do_arquivo)
                print(f"🔄 Fichas recarregadas: {len(fichas_do_arquivo)} total")
    except Exception as e:
        print(f"⚠️ Erro ao recarregar fichas: {e}")
    
    fichas_validas = []
						
	
    for chave, ficha in fichas_personagens.items():
							 
        if ficha.get("autor") == user_id:
																																																													 
			
            if (ficha.get("nome") and 
                ficha.get("sistema") and
                ficha.get("conteudo")):
                fichas_validas.append(ficha)
    
    print(f"📊 User {user_id}: {len(fichas_validas)} ficha(s) válida(s)")
    return fichas_validas


async def _garantir_categoria(guild: discord.Guild) -> discord.CategoryChannel:
    cat = discord.utils.get(guild.categories, name=SESSOES_CATEGORY_NAME)
    if cat:
        return cat
    return await guild.create_category(SESSOES_CATEGORY_NAME, reason="Categoria para sessões privadas de RPG")


async def _criar_canal_de_sessao(
    guild: discord.Guild,
    categoria: discord.CategoryChannel,
    mestre: discord.Member,
    jogadores: List[discord.Member],
    bot_member: discord.Member,
    nome_sugerido: Optional[str] = None,
) -> discord.TextChannel:
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        bot_member: discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True, attach_files=True),
        mestre: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, embed_links=True),
    }
    for j in jogadores:
        overwrites[j] = discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True)

    nome = nome_sugerido or f"sessao-{mestre.name.lower()}"
    channel = await guild.create_text_channel(
        name=nome,
        category=categoria,
        overwrites=overwrites,
        reason="Criação de canal privado para sessão de RPG",
    )
    return channel


def _formatar_lista_fichas(fichas: List[Dict[str, Any]], SISTEMAS_DISPONIVEIS: Dict) -> str:
    """Formata lista de fichas válidas para exibição."""
    if not fichas:
        return "— Nenhuma ficha encontrada."
    
    linhas = []
    for f in fichas[:25]:
        sistema_code = f.get("sistema", "dnd5e")
        sistema_nome = SISTEMAS_DISPONIVEIS.get(sistema_code, {}).get("nome", sistema_code)
        nome = f.get("nome", "Sem nome")
        linhas.append(f"• **{nome}** *(Sistema: {sistema_nome})*")
    
    if len(fichas) > 25:
        linhas.append(f"… e mais {len(fichas) - 25}")
    
    return "\n".join(linhas)


def _embed_status_sessao(guild: discord.Guild, sessao: Dict[str, Any]) -> discord.Embed:
    jogadores = sessao.get("jogadores", [])
    fichas_sel = sessao.get("fichas", {})
    sistema = sessao.get("sistema", "dnd5e")
    status = sessao.get("status", "preparando")
    mestre_id = sessao.get("mestre_id")
    mestre_txt = _user_mention(guild, mestre_id)

    jogadores_txt = "\n".join(
        [f"• {_user_mention(guild, uid)} — {'✅' if str(uid) in fichas_sel or uid in fichas_sel else '⏳ sem ficha'}"
         for uid in jogadores]
    ) or "—"

    embed = discord.Embed(
        title="🎮 Sessão de RPG",
        description=f"**Sistema**: `{sistema}`\n**Status**: **{status.upper()}**\n**Mestre**: {mestre_txt}",
        color=discord.Color.purple()
    )
    embed.add_field(name="👥 Jogadores", value=jogadores_txt, inline=False)
    if fichas_sel:
        picks = []
        for k, chave in fichas_sel.items():
            uid = int(k) if isinstance(k, str) else k
            picks.append(f"• {_user_mention(guild, uid)} → **{chave.split('_', 1)[-1].replace('_',' ').title()}**")
        embed.add_field(name="🧾 Fichas Selecionadas", value="\n".join(picks)[:1024], inline=False)
    return embed


# -----------------------------
# View para Rolagens Interativas (NOVO!)
# -----------------------------

class RollRequestView(discord.ui.View):
    """Botões para rolar dados quando solicitado pela IA."""
    
    def __init__(self, bot, sessoes_ativas, salvar_dados, channel_id, roll_type, players_needed):
        super().__init__(timeout=300)  # 5 minutos para rolar
        self.bot = bot
        self.sessoes_ativas = sessoes_ativas
        self.salvar_dados = salvar_dados
        self.channel_id = channel_id
        self.roll_type = roll_type  # Ex: "1d20+3", "2d6"
        self.players_needed = players_needed  # Lista de user_ids que precisam rolar
        self.rolls_done = {}  # user_id -> resultado
    
    @discord.ui.button(label="🎲 Rolar Dados", style=discord.ButtonStyle.success, custom_id="roll_dice")
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
        
        # Importa função de rolagem
        from rpg_core import rolar_dados
        texto, total = rolar_dados(self.roll_type)
        
        if total is None:
            return await interaction.response.send_message(
                f"❌ Erro ao processar rolagem: {texto}",
                ephemeral=True
            )
        
        # Registra resultado
        self.rolls_done[interaction.user.id] = total
        
        # Responde ao jogador
        await interaction.response.send_message(
            f"🎲 **{interaction.user.display_name}** rolou:\n{texto}",
            ephemeral=False
        )
        
        # Verifica se todos rolaram
        if len(self.rolls_done) >= len(self.players_needed):
            # Todos rolaram - continua a história
            sessao = self.sessoes_ativas.get(self.channel_id)
            if sessao:
                # Desabilita botão
                button.disabled = True
                await interaction.message.edit(view=self)
                
                # Prepara resumo das rolagens
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
                
                # Continua narrativa automaticamente
                await self._continue_story(interaction.channel, sessao)
        else:
            # Ainda faltam jogadores
            faltam = len(self.players_needed) - len(self.rolls_done)
            await interaction.channel.send(
                f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} rolar..."
            )
    
    async def _continue_story(self, channel, sessao):
        """Continua a história após todas as rolagens."""
        from utils import chamar_groq, get_system_prompt
        
        sistema = sessao.get("sistema", "dnd5e")
        historia = sessao.get("historia", [])
        
        # Adiciona contexto das rolagens
        resumo_rolls = "\n".join([
            f"Jogador {uid} rolou: {resultado}"
            for uid, resultado in self.rolls_done.items()
        ])
        
        historia.append({
            "role": "user",
            "content": f"Resultados das rolagens ({self.roll_type}):\n{resumo_rolls}\n\nNarre as consequências destas rolagens de forma cinematográfica. Considere os valores obtidos e descreva o resultado de forma envolvente. 2-3 parágrafos."
        })
        
        # Limita histórico
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
        ] + historia_recente
        
        resposta = await chamar_groq(mensagens, max_tokens=1200)
        
        # Adiciona ao histórico
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        self.salvar_dados()
        
        # Envia resposta
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


# -----------------------------
# View para Continuação da História
# -----------------------------

class ContinueStoryView(discord.ui.View):
    """Botões para continuar a narrativa após cada resposta da IA."""
    
    def __init__(self, bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt):
        super().__init__(timeout=None)  # Sem timeout para sessões longas
        self.bot = bot
        self.sessoes_ativas = sessoes_ativas
        self.salvar_dados = salvar_dados
        self.chamar_groq = chamar_groq
        self.get_system_prompt = get_system_prompt
    
    @discord.ui.button(label="🎬 Continuar História", style=discord.ButtonStyle.primary, custom_id="continue_story")
    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para o mestre continuar a narrativa."""
        sessao = self.sessoes_ativas.get(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada.", ephemeral=True)
        
        # Apenas mestre pode usar este botão
        if interaction.user.id != sessao.get("mestre_id"):
            return await interaction.response.send_message(
                "⚠️ Use o comando `!acao` para descrever o que seu personagem faz!",
                ephemeral=True
            )
        
        # Pede ao mestre que descreva a próxima cena
        await interaction.response.send_message(
            "📝 **Descreva a próxima cena ou acontecimento:**\n"
            "Use o comando `!cenanarrada <descrição>` ou aguarde as ações dos jogadores com `!acao`.",
            ephemeral=True
        )


# -----------------------------
# Views (Botões de Controle)
# -----------------------------

class SessionControlView(discord.ui.View):
    def __init__(self, bot: commands.Bot, sessao_store: Dict[int, Dict[str, Any]], salvar_dados_cb, chamar_groq_cb, get_system_prompt_cb, timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.sessoes_ativas = sessao_store
        self.salvar_dados = salvar_dados_cb
        self.chamar_groq = chamar_groq_cb
        self.get_system_prompt = get_system_prompt_cb

    def _get_sessao(self, channel_id: int) -> Optional[Dict[str, Any]]:
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

        # Verifica se todos possuem fichas selecionadas
        jogadores = sessao.get("jogadores", [])
        fichas = sessao.get("fichas", {})
        faltando = [uid for uid in jogadores if str(uid) not in fichas and uid not in fichas]
        if faltando:
            faltantes_txt = ", ".join([_user_mention(interaction.guild, uid) for uid in faltando])
            return await interaction.response.send_message(f"⏳ Ainda faltam fichas: {faltantes_txt}", ephemeral=True)

        # Monta resumo das fichas selecionadas para a IA
        from config import fichas_personagens
        
        sistema = sessao.get("sistema", "dnd5e")
        prompt_intro = "Gere uma **introdução épica** para a sessão de RPG, apresentando o cenário, tom e conexões entre os personagens. 3-5 parágrafos curtos. Termine com um gancho claro para a primeira cena.\n\nPersonagens:\n"
        
        for uid, chave in fichas.items():
            # Busca nome real da ficha
            ficha_info = fichas_personagens.get(chave, {})
            nome_personagem = ficha_info.get('nome', 'Personagem Desconhecido')
            conteudo = ficha_info.get('conteudo', '')
            resumo = conteudo[:200] + "..." if len(conteudo) > 200 else conteudo
            prompt_intro += f"- **{nome_personagem}**: {resumo}\n"

        # Chama IA
        mensagens = [
            {"role": "system", "content": self.get_system_prompt(sistema)},
            {"role": "user", "content": prompt_intro}
        ]
        await interaction.response.defer(thinking=True)
        intro = await self.chamar_groq(mensagens, max_tokens=900)
        
        # Inicializa histórico narrativo
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
        
        # View com botão para continuar
        continue_view = ContinueStoryView(
            self.bot,
            self.sessoes_ativas,
            self.salvar_dados,
            self.chamar_groq,
            self.get_system_prompt
        )
        await interaction.followup.send(embed=embed, view=continue_view)

    @discord.ui.button(label="📊 Ver Fichas", style=discord.ButtonStyle.primary)
    async def fichas_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        sessao = self._get_sessao(interaction.channel.id)
        if not sessao:
            return await interaction.response.send_message("❌ Sessão não encontrada neste canal.", ephemeral=True)

        # Recarrega fichas antes de mostrar
        import json
        import os
        DATA_DIR = os.path.join(os.getcwd(), "bot_data")
        FICHAS_PATH = os.path.join(DATA_DIR, "fichas_personagens.json")
        
        fichas_atualizadas = {}
        try:
            if os.path.exists(FICHAS_PATH):
                with open(FICHAS_PATH, "r", encoding="utf-8") as f:
                    fichas_atualizadas = json.load(f)
                print(f"🔄 [Botão Ver Fichas] Recarregadas: {len(fichas_atualizadas)} fichas")
        except Exception as e:
            print(f"⚠️ Erro ao recarregar fichas no botão: {e}")

        # Cria embed customizado com fichas recarregadas
        jogadores = sessao.get("jogadores", [])
        fichas_sel = sessao.get("fichas", {})
        sistema = sessao.get("sistema", "dnd5e")
        status = sessao.get("status", "preparando")
        mestre_id = sessao.get("mestre_id")
        mestre_txt = _user_mention(interaction.guild, mestre_id)

        jogadores_txt = []
        for uid in jogadores:
            if str(uid) in fichas_sel or uid in fichas_sel:
                chave_ficha = fichas_sel.get(str(uid)) or fichas_sel.get(uid)
                ficha_info = fichas_atualizadas.get(chave_ficha, {})
                nome_ficha = ficha_info.get('nome', 'Ficha Desconhecida')
                jogadores_txt.append(f"• {_user_mention(interaction.guild, uid)} — ✅ **{nome_ficha}**")
            else:
                jogadores_txt.append(f"• {_user_mention(interaction.guild, uid)} — ⏳ sem ficha")

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

        await interaction.response.send_message("⚠️ Encerrando sessão e **apagando este canal** em 5 segundos…", ephemeral=False)
        await asyncio.sleep(5)
        try:
            self.sessoes_ativas.pop(interaction.channel.id, None)
            self.salvar_dados()
            await interaction.channel.delete(reason="Sessão encerrada pelo mestre (botão).")
        except Exception:
            pass


# -----------------------------
# Setup de Comandos
# -----------------------------

def setup_sessoes(
    bot: commands.Bot,
    SISTEMAS_DISPONIVEIS: Dict[str, Any],
    fichas_personagens: Dict[str, Any],
    sistemas_rpg: Dict[int, str],
    sessoes_ativas: Dict[int, Dict[str, Any]],
    chamar_groq,
    get_system_prompt,
    salvar_dados,
):
    """Registra comandos de sessão no bot."""

    # ------------- Comando: acao (COM ROLAGENS!) -------------
    @bot.command(name="acao")
    @commands.guild_only()
    async def acao(ctx: commands.Context, *, descricao: str = None):
        """Jogadores descrevem suas ações durante a sessão."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado **no canal da sessão**.")
        
        if not descricao:
            return await ctx.send("❌ Use: `!acao <descrição do que seu personagem faz>`")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        # Verifica se a pessoa faz parte da sessão
        if ctx.author.id != sessao["mestre_id"] and ctx.author.id not in sessao["jogadores"]:
            return await ctx.send("⚠️ Você não faz parte desta sessão.")
        
        # Verifica se a sessão já começou
        if sessao.get("status") != "em_andamento":
            return await ctx.send("⚠️ A aventura ainda não começou! O mestre precisa iniciar a sessão.")
        
        # Pega o nome do personagem (se tiver ficha selecionada)
        fichas_sel = sessao.get("fichas", {})
        chave_ficha = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
        
        if chave_ficha:
																	  
            nome_personagem = chave_ficha.split('_', 1)[-1].replace('_', ' ').title()
        else:
            nome_personagem = ctx.author.display_name
        
        # Formata a ação do jogador
        acao_formatada = f"**{nome_personagem}** ({ctx.author.display_name}): {descricao}"
        
        # Adiciona ao histórico da sessão
        historia = sessao.get("historia", [])
        historia.append({
            "role": "user",
            "content": f"Ação de {nome_personagem}: {descricao}"
        })
        
        # Envia mensagem visual
        await ctx.send(
            embed=discord.Embed(
                title=f"🎭 {nome_personagem} age!",
                description=descricao,
                color=discord.Color.blue()
            ).set_footer(text=f"Jogador: {ctx.author.display_name}")
        )
        
        # Gera resposta narrativa da IA
        await ctx.send("✨ *A história se desenrola...*")
        
        sistema = sessao.get("sistema", "dnd5e")
        
        # Limita histórico para não estourar tokens (últimas 20 interações)
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        # Monta mensagens para IA com instrução para solicitar rolagens
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema) + "\n\n**IMPORTANTE:** Quando apropriado, solicite rolagens de dados aos jogadores. Use o formato exato:\n[ROLL: tipo_de_dado, jogadores]\nExemplos:\n- [ROLL: 1d20+3, todos] - todos rolam\n- [ROLL: 2d6, " + nome_personagem + "] - apenas este personagem\n- [ROLL: 1d20, todos] - múltiplos jogadores\n\nSOLICITE rolagens em situações de: combate, testes de perícia, percepção, furtividade, etc."},
        ] + historia_recente + [
            {"role": "user", "content": f"Narre as consequências da ação de {nome_personagem}: {descricao}. Seja cinematográfico, use os 5 sentidos. Se a ação requer teste de habilidade/combate/perícia, SOLICITE a rolagem apropriada usando [ROLL: dado, jogadores]. Termine com gancho claro. 2-4 parágrafos."}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=1200)
        
        # Adiciona resposta ao histórico
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        salvar_dados()
        
        # NOVO: Detecta se há solicitação de rolagem
        roll_match = re.search(r'\[ROLL:\s*([^,\]]+),\s*([^\]]+)\]', resposta, re.IGNORECASE)
												 
										
									  
		 
        
        if roll_match:
            roll_type = roll_match.group(1).strip()
            players_str = roll_match.group(2).strip()
            
            # Remove a tag [ROLL:...] da resposta exibida
            resposta_limpa = re.sub(r'\[ROLL:[^\]]+\]', '', resposta).strip()
            
            # Determina quem deve rolar
            if players_str.lower() in ['todos', 'all', 'grupo', 'party']:
                players_needed = sessao.get("jogadores", [])
            else:
                # Tenta encontrar personagens mencionados
                players_needed = []
                for jogador_id in sessao.get("jogadores", []):
                    fichas_sel = sessao.get("fichas", {})
                    chave_ficha = fichas_sel.get(str(jogador_id)) or fichas_sel.get(jogador_id)
                    if chave_ficha:
                        nome_ficha = chave_ficha.split('_', 1)[-1].replace('_', ' ').lower()
                        if nome_ficha in players_str.lower():
                            players_needed.append(jogador_id)
                
                # Se não encontrou ninguém específico, assume todos
                if not players_needed:
                    players_needed = sessao.get("jogadores", [])
            
            # Envia narrativa
            embed = discord.Embed(
                title="📖 A História Continua...",
                description=resposta_limpa[:4000],
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
            
            # Cria embed de solicitação de rolagem
            jogadores_nomes = []
            for uid in players_needed:
                membro = ctx.guild.get_member(uid)
                if membro:
                    jogadores_nomes.append(membro.mention)
            
            roll_embed = discord.Embed(
                title="🎲 Rolagem Necessária!",
                description=(
                    f"**Tipo de Rolagem:** `{roll_type}`\n"
                    f"**Jogadores:** {', '.join(jogadores_nomes) if jogadores_nomes else 'Todos'}\n\n"
                    f"Clique no botão abaixo para rolar seus dados!"
                ),
                color=discord.Color.blue()
            )
            
            view = RollRequestView(
                bot, 
                sessoes_ativas, 
                salvar_dados, 
                ctx.channel.id,
                roll_type,
                players_needed
            )
            await ctx.send(embed=roll_embed, view=view)
            
        else:
            # Sem rolagem solicitada - continua normal
            embed = discord.Embed(
                title="📖 A História Continua...",
                description=resposta[:4000],
                color=discord.Color.gold()
            )
            
            view = ContinueStoryView(bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt)
            await ctx.send(embed=embed, view=view)

    # ------------- Comando: cenanarrada (COM ROLAGENS!) -------------
    @bot.command(name="cenanarrada")
    @commands.guild_only()
    async def cena_narrada(ctx: commands.Context, *, descricao: str = None):
        """Mestre narra uma cena e a IA expande cinematograficamente."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado **no canal da sessão**. Use `!cena` para descrições gerais.")
        
        if not descricao:
            return await ctx.send("❌ Use: `!cenanarrada <descrição da cena>`")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        # Apenas mestre pode narrar cenas
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o **mestre** pode narrar cenas. Use `!acao` para descrever o que seu personagem faz.")
        
        # Verifica se a sessão já começou
        if sessao.get("status") != "em_andamento":
            return await ctx.send("⚠️ A aventura ainda não começou! Use o botão 'Iniciar Aventura' primeiro.")
        
        # Adiciona ao histórico
        historia = sessao.get("historia", [])
        historia.append({
            "role": "user",
            "content": f"Mestre descreve nova cena: {descricao}"
        })
        
        await ctx.send("🎬 *Expandindo a cena...*")
        
        sistema = sessao.get("sistema", "dnd5e")
        historia_recente = historia[-20:] if len(historia) > 20 else historia
        
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema) + "\n\n**IMPORTANTE:** Quando apropriado, solicite rolagens de dados aos jogadores. Use o formato exato:\n[ROLL: tipo_de_dado, jogadores]\nExemplos:\n- [ROLL: 1d20+3, todos] - todos rolam\n- [ROLL: 2d6, jogador_específico] - apenas um\n\nSOLICITE rolagens em situações de: combate, percepção, investigação, furtividade, etc."},
        ] + historia_recente + [
            {"role": "user", "content": f"Expanda esta cena de forma cinematográfica: {descricao}. Use linguagem evocativa, apele aos 5 sentidos. Se a situação requer rolagens (percepção, combate, etc), SOLICITE usando [ROLL: dado, jogadores]. Termine com momento que convide ação. 2-4 parágrafos."}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=1200)
        
        # Adiciona resposta ao histórico
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        salvar_dados()
        
        # NOVO: Detecta se há solicitação de rolagem
        roll_match = re.search(r'\[ROLL:\s*([^,\]]+),\s*([^\]]+)\]', resposta, re.IGNORECASE)
								   
										
										
		 
        
        if roll_match:
            roll_type = roll_match.group(1).strip()
            players_str = roll_match.group(2).strip()
            
            # Remove a tag [ROLL:...] da resposta exibida
            resposta_limpa = re.sub(r'\[ROLL:[^\]]+\]', '', resposta).strip()
            
            # Determina quem deve rolar
            if players_str.lower() in ['todos', 'all', 'grupo', 'party']:
                players_needed = sessao.get("jogadores", [])
            else:
                # Tenta encontrar personagens mencionados
                players_needed = []
                for jogador_id in sessao.get("jogadores", []):
                    fichas_sel = sessao.get("fichas", {})
                    chave_ficha = fichas_sel.get(str(jogador_id)) or fichas_sel.get(jogador_id)
                    if chave_ficha:
                        nome_ficha = chave_ficha.split('_', 1)[-1].replace('_', ' ').lower()
                        if nome_ficha in players_str.lower():
                            players_needed.append(jogador_id)
                
                # Se não encontrou ninguém específico, assume todos
                if not players_needed:
                    players_needed = sessao.get("jogadores", [])
            
            # Envia narrativa
            embed = discord.Embed(
                title="🎬 Nova Cena",
                description=resposta_limpa[:4000],
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            
            # Cria embed de solicitação de rolagem
            jogadores_nomes = []
            for uid in players_needed:
                membro = ctx.guild.get_member(uid)
                if membro:
                    jogadores_nomes.append(membro.mention)
            
            roll_embed = discord.Embed(
                title="🎲 Rolagem Necessária!",
                description=(
                    f"**Tipo de Rolagem:** `{roll_type}`\n"
                    f"**Jogadores:** {', '.join(jogadores_nomes) if jogadores_nomes else 'Todos'}\n\n"
                    f"Clique no botão abaixo para rolar seus dados!"
                ),
                color=discord.Color.blue()
            )
            
            view = RollRequestView(
                bot, 
                sessoes_ativas, 
                salvar_dados, 
                ctx.channel.id,
                roll_type,
                players_needed
            )
            await ctx.send(embed=roll_embed, view=view)
            
        else:
            # Sem rolagem solicitada - continua normal
            embed = discord.Embed(
                title="🎬 Nova Cena",
                description=resposta[:4000],
                color=discord.Color.purple()
            )
            
            view = ContinueStoryView(bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt)
            await ctx.send(embed=embed, view=view)

    # ------------- Comando: iniciarsessao -------------
    @bot.command(name="iniciarsessao")
    @commands.guild_only()
    async def iniciarsessao(ctx: commands.Context, *membros: discord.Member):
        if not membros:
            return await ctx.send("❌ Use: `!iniciarsessao @Jogador1 @Jogador2 ...`")

        guild = ctx.guild
        mestre: discord.Member = ctx.author
        jogadores: List[discord.Member] = list(membros)
        bot_member = guild.get_member(bot.user.id)

        # Categoria + canal
        categoria = await _garantir_categoria(guild)
        canal = await _criar_canal_de_sessao(
            guild=guild,
            categoria=categoria,
            mestre=mestre,
            jogadores=jogadores,
            bot_member=bot_member,
            nome_sugerido=f"sessao-{mestre.name.lower()}",
        )

        # Inicializa sessão
        sistema = sistemas_rpg.get(mestre.id, "dnd5e")
        sessoes_ativas[canal.id] = {
            "guild_id": guild.id,
            "channel_id": canal.id,
            "categoria_id": categoria.id if categoria else None,
            "mestre_id": mestre.id,
            "jogadores": [j.id for j in jogadores],
            "fichas": {},
            "status": "preparando",
            "sistema": sistema,
            "criada_em": datetime.datetime.utcnow().isoformat(),
            "historia": [],
        }
        salvar_dados()

        # Mensagem inicial com botões
        view = SessionControlView(bot, sessoes_ativas, salvar_dados, chamar_groq, get_system_prompt, timeout=None)

        # Construir embed
        sistema_nome = SISTEMAS_DISPONIVEIS.get(sistema, {}).get('nome', sistema)
        descr = f"Sessão criada por {mestre.mention}.\nSistema configurado: **{sistema_nome}**\n\n**Jogadores convidados:**\n"
        for j in jogadores:
            descr += f"• {j.mention}\n"

        embed = discord.Embed(title="🎲 Sessão de RPG Criada!", description=descr, color=discord.Color.blurple())
        embed.add_field(
            name="🗂️ Como selecionar sua ficha",
            value="Use o comando `!selecionarficha <Nome exato>` aqui neste canal.",
            inline=False,
        )
        await canal.send(embed=embed, view=view)

        # Lista fichas de cada jogador
        for j in jogadores:
            fichas = _coletar_fichas_usuario(fichas_personagens, j.id)
            
            if fichas:
                lista = _formatar_lista_fichas(fichas, SISTEMAS_DISPONIVEIS)
                total_fichas = len(fichas)
                await canal.send(
                    embed=discord.Embed(
                        title=f"📚 Fichas de {j.display_name} ({total_fichas} encontrada{'s' if total_fichas != 1 else ''})",
                        description=lista,
                        color=discord.Color.dark_teal()
                    ).set_footer(text="💡 Use !selecionarficha <nome> para escolher sua ficha")
                )
            else:
                await canal.send(
                    embed=discord.Embed(
                        title=f"📚 Fichas de {j.display_name}",
                        description=f"— Nenhuma ficha encontrada.\n💡 Use `!ficha <nome>` ou `!criarficha` para criar uma nova!",
                        color=discord.Color.orange()
                    )
                )

        await ctx.send(f"✅ Sessão criada com sucesso em {canal.mention}")

    # ------------- Comando: selecionarficha -------------
    @bot.command(name="selecionarficha")
    @commands.guild_only()
    async def selecionarficha(ctx: commands.Context, *, nome_personagem: str = None):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado **dentro do canal da sessão**.")
        if not nome_personagem:
            return await ctx.send("❌ Use: `!selecionarficha <Nome da Ficha>`")

        sessao = sessoes_ativas[ctx.channel.id]
        # Verifica se autor faz parte
        if ctx.author.id != sessao["mestre_id"] and ctx.author.id not in sessao["jogadores"]:
            return await ctx.send("⚠️ Você não faz parte desta sessão.")

        # Localiza ficha do usuário pelo nome
        chave_encontrada = None
							   
        for chave, ficha in fichas_personagens.items():
																		  
            if (ficha.get("autor") == ctx.author.id and 
                ficha.get("nome") and 
                ficha.get("conteudo") and
                ficha.get("nome", "").lower() == nome_personagem.lower()):
                chave_encontrada = chave
																   
                break

        if not chave_encontrada:
            return await ctx.send("❌ Ficha não encontrada no seu perfil. Verifique o nome com `!verficha` ou `!minhasfichas`.")

        # Registra
        sessao["fichas"][str(ctx.author.id)] = chave_encontrada
        salvar_dados()

        # Confirmação
        embed = discord.Embed(
            title=f"✅ Ficha Selecionada: {nome_personagem}",
            description=f"Ficha `{nome_personagem}` selecionada com sucesso! Use `!verficha {nome_personagem}` para ver os detalhes completos.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
        # Notifica quantos jogadores já selecionaram
        jogadores_total = len(sessao.get("jogadores", []))
        fichas_selecionadas = len(sessao.get("fichas", {}))
        
        if fichas_selecionadas >= jogadores_total:
            await ctx.send("🎉 **Todos os jogadores selecionaram suas fichas!** O mestre pode iniciar a aventura.")
        else:
            faltam = jogadores_total - fichas_selecionadas
            await ctx.send(f"⏳ Aguardando {faltam} jogador{'es' if faltam > 1 else ''} selecionar ficha...")

    # ------------- Comando: sessoes -------------
    @bot.command(name="sessoes")
    @commands.guild_only()
    async def sessoes_cmd(ctx: commands.Context):
        guild = ctx.guild
        ativos = [s for s in sessoes_ativas.values() if s.get("guild_id") == guild.id]
        if not ativos:
            return await ctx.send("— Não há sessões ativas neste servidor.")

        linhas = []
        for s in ativos[:20]:
            canal = guild.get_channel(s["channel_id"])
            mestre_txt = _user_mention(guild, s["mestre_id"])
            jogadores = s.get("jogadores", [])
            linhas.append(f"• {canal.mention if canal else '#apagado'} — Mestre: {mestre_txt} — Jogadores: {len(jogadores)} — Sistema: `{s.get('sistema')}` — Status: **{s.get('status')}**")

        embed = discord.Embed(title="📋 Sessões Ativas", description="\n".join(linhas), color=discord.Color.blurple())
        await ctx.send(embed=embed)

    # ------------- Comando: convidarsessao -------------
    @bot.command(name="convidarsessao")
    @commands.guild_only()
    async def convidarsessao(ctx: commands.Context, *novos: discord.Member):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado **no canal da sessão**.")

        sessao = sessoes_ativas[ctx.channel.id]
        if ctx.author.id != sessao["mestre_id"]:
            return await ctx.send("⚠️ Apenas o mestre pode convidar jogadores.")

        if not novos:
            return await ctx.send("❌ Use: `!convidarsessao @NovoJogador [@Outro]`")

        guild = ctx.guild
        canal: discord.TextChannel = ctx.channel

        # Atualiza permissões e sessão
        adicionados = []
        for m in novos:
            try:
                await canal.set_permissions(m, view_channel=True, send_messages=True, embed_links=True)
                if m.id not in sessao["jogadores"]:
                    sessao["jogadores"].append(m.id)
                adicionados.append(m.mention)
            except Exception:
                pass

            # Lista fichas do novo jogador
            fichas = _coletar_fichas_usuario(fichas_personagens, m.id)
            if fichas:
                total_fichas = len(fichas)
                await ctx.send(
                    embed=discord.Embed(
                        title=f"📚 Fichas de {m.display_name} ({total_fichas} encontrada{'s' if total_fichas != 1 else ''})",
                        description=_formatar_lista_fichas(fichas, SISTEMAS_DISPONIVEIS),
                        color=discord.Color.dark_teal()
                    ).set_footer(text="💡 Use !selecionarficha <nome> para escolher sua ficha")
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title=f"📚 Fichas de {m.display_name}",
                        description=f"— Nenhuma ficha encontrada.\n💡 Use `!ficha <nome>` ou `!criarficha` para criar uma nova!",
                        color=discord.Color.orange()
                    )
                )

        salvar_dados()
        if adicionados:
            await ctx.send(f"✅ Adicionados: {', '.join(adicionados)}")

    # ------------- Comando: removerjogador -------------
    @bot.command(name="removerjogador")
    @commands.guild_only()
    async def removerjogador(ctx: commands.Context, jogador: discord.Member):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use este comando **no canal da sessão**.")

        sessao = sessoes_ativas[ctx.channel.id]
        if ctx.author.id != sessao["mestre_id"]:
            return await ctx.send("⚠️ Apenas o mestre pode remover jogadores.")

        canal: discord.TextChannel = ctx.channel
        try:
            await canal.set_permissions(jogador, overwrite=None)
        except Exception:
            pass

        if jogador.id in sessao["jogadores"]:
            sessao["jogadores"].remove(jogador.id)
        sessao["fichas"].pop(str(jogador.id), None)
        salvar_dados()

        await ctx.send(f"✅ Jogador removido: {jogador.mention}")

    # ------------- Comando: mudarficha -------------
    @bot.command(name="mudarficha")
    @commands.guild_only()
    async def mudarficha(ctx: commands.Context, *, nome_personagem: str = None):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use este comando **no canal da sessão**.")
        if not nome_personagem:
            return await ctx.send("❌ Use: `!mudarficha <Nome da Ficha>`")

        sessao = sessoes_ativas[ctx.channel.id]
        em_andamento = sessao.get("status") == "em_andamento"
        mestre_id = sessao.get("mestre_id")

        # Se já iniciou, precisa de aprovação do mestre
        if em_andamento and ctx.author.id != mestre_id:
            msg = await ctx.send(f"⚠️ {_user_mention(ctx.guild, mestre_id)}, aprova a troca de ficha de {ctx.author.mention}? ✅/❌")
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            def check(reaction: discord.Reaction, user: discord.User):
                return reaction.message.id == msg.id and str(reaction.emoji) in ["✅", "❌"] and user.id == mestre_id

            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
                if str(reaction.emoji) == "❌":
                    return await ctx.send("❌ Troca não aprovada pelo mestre.")
            except asyncio.TimeoutError:
                return await ctx.send("⏰ Tempo esgotado — troca não aprovada.")

        # Busca ficha
        chave_encontrada = None
        for chave, ficha in fichas_personagens.items():
            if (ficha.get("autor") == ctx.author.id and 
                ficha.get("nome") and 
                ficha.get("conteudo") and
                ficha.get("nome", "").lower() == nome_personagem.lower()):
                chave_encontrada = chave
                break

        if not chave_encontrada:
            return await ctx.send("❌ Ficha não encontrada no seu perfil.")

        sessao["fichas"][str(ctx.author.id)] = chave_encontrada
        salvar_dados()
        await ctx.send(f"✅ Ficha atualizada para **{nome_personagem}**.")

    # ------------- Comando: pausarsessao -------------
    @bot.command(name="pausarsessao")
    @commands.guild_only()
    async def pausarsessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use este comando **no canal da sessão**.")
        sessao = sessoes_ativas[ctx.channel.id]
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o mestre pode pausar/retomar.")

        if sessao["status"] == "pausada":
            sessao["status"] = "em_andamento"
            salvar_dados()
            return await ctx.send(embed=discord.Embed(title="▶️ Sessão retomada", color=discord.Color.green()))

        if sessao["status"] in ("preparando", "em_andamento"):
            sessao["status"] = "pausada"
            salvar_dados()
            return await ctx.send(embed=discord.Embed(title="⏸️ Sessão pausada", color=discord.Color.orange()))

        await ctx.send("ℹ️ Estado inalterado.")

    # ------------- Comando: infosessao -------------
    @bot.command(name="infosessao")
    @commands.guild_only()
    async def infosessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado no canal da sessão.")

        sessao = sessoes_ativas[ctx.channel.id]
        embed = _embed_status_sessao(ctx.guild, sessao)
        await ctx.send(embed=embed)

    # ------------- Comando: resumosessao -------------
    @bot.command(name="resumosessao")
    @commands.guild_only()
    async def resumosessao(ctx: commands.Context):
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Este comando deve ser usado no canal da sessão.")

        # Captura últimas mensagens
        logs = []
        async for m in ctx.channel.history(limit=50, oldest_first=False):
            if m.author.bot:
                continue
            content = (m.content or "").strip()
            if content:
                logs.append(f"{m.author.display_name}: {content}")
        logs = list(reversed(logs))
        resumo_input = "\n".join(logs[-40:])

        sessao = sessoes_ativas[ctx.channel.id]
        sistema = sessao.get("sistema", "dnd5e")
        mensagens = [
            {"role": "system", "content": get_system_prompt(sistema)},
            {"role": "user", "content": f"Faça um resumo narrativo (3-5 parágrafos) do seguinte chat de sessão:\n\n{resumo_input}"}
        ]

        await ctx.send("🧠 Gerando resumo com IA…")
        texto = await chamar_groq(mensagens, max_tokens=800)
        await ctx.send(embed=discord.Embed(title="📝 Resumo da Sessão", description=texto[:4000], color=discord.Color.purple()))

    # ------------- Comando: ajudasessao -------------
    @bot.command(name="ajudasessao")
    async def ajudasessao(ctx: commands.Context):
        descr = (
            "**Comandos principais**\n"
            "• `!iniciarsessao @jog1 @jog2` — Cria sessão privada\n"
            "• `!selecionarficha Nome` — Escolhe sua ficha\n"
            "• `!sessoes` — Lista sessões ativas\n"
            "• `!infosessao` — Detalhes da sessão atual\n"
            "• `!resumosessao` — Resumo com IA das últimas mensagens\n"
            "• `!convidarsessao @Novo` — Adiciona jogador\n"
            "• `!removerjogador @Jog` — Remove jogador\n"
            "• `!mudarficha Nome` — Troca de personagem\n"
            "• `!pausarsessao` — Pausa/retoma\n\n"
            "**🎭 Durante a Aventura (Sistema Interativo!)**\n"
            "• `!acao <descrição>` — Jogadores descrevem o que fazem\n"
            "• `!cenanarrada <descrição>` — Mestre narra nova cena\n"
            "• **🎲 Rolagens Automáticas:** Quando a IA solicitar rolagens, um botão aparecerá!\n"
            "  - Clique em 'Rolar Dados' quando solicitado\n"
            "  - O sistema aguarda TODOS rolarem antes de continuar\n"
            "  - Os resultados são mostrados e a história prossegue automaticamente\n"
            "• Botão 'Continuar História' — Aparece após cada ação\n\n"
            "**Botões no canal da sessão**\n"
            "• 🎬 Iniciar Aventura — Inicia a narrativa (mestre)\n"
            "• 📊 Ver Fichas — Mostra status das seleções\n"
            "• 🎲 Rolar Dados — Aparece quando a IA solicita rolagens\n"
            "• 🎬 Continuar História — Aparece após cada ação\n"
            "• 🚪 Encerrar Sessão — Apaga o canal (mestre)\n\n"
            "**💡 Exemplo de Jogo com Rolagens:**\n"
            "1. Mestre clica 'Iniciar Aventura'\n"
            "2. Jogador usa `!acao examino a porta trancada`\n"
            "3. IA narra: 'A porta está trancada... [SOLICITA ROLAGEM 1d20+Percepção]'\n"
            "4. Botão 🎲 aparece para o jogador rolar\n"
            "5. Jogador clica, rola 18+3 = 21\n"
            "6. IA continua: 'Com esse resultado excepcional, você nota...'\n"
            "7. História flui naturalmente!\n\n"
            "**🎯 Dicas para Mestres:**\n"
            "• A IA pedirá rolagens em situações apropriadas (combate, perícia, etc)\n"
            "• Use `!cenanarrada` para introduzir desafios que exigem testes\n"
            "• O sistema aguarda automaticamente todos os jogadores rolarem\n"
            "• Você pode usar `!rolar` manualmente a qualquer momento também"
        )
        await ctx.send(embed=discord.Embed(title="📖 Ajuda — Sessões de RPG", description=descr, color=discord.Color.blurple()))

    # Fim do setup
    return