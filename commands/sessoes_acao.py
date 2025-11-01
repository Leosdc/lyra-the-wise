# commands/sessoes_acao.py (REFATORADO v3.0)
"""
Comandos de ação CONTROLADOS PELO MESTRE.
Lyra só narra - mestre decide tudo.
"""

import discord
from discord.ext import commands
from views.sessao_master_control_views import MasterControlView


def register_acao_commands(
    bot: commands.Bot,
    sessoes_ativas,
    fichas_personagens,
    chamar_groq,
    get_system_prompt,
    salvar_dados
):
    """Registra comandos de ação e narrativa."""

    @bot.command(name="narrativa")
    @commands.guild_only()
    async def narrativa(ctx: commands.Context, *, prompt: str = None):
        """[MESTRE] Lyra narra uma cena baseada no seu prompt."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use **no canal da sessão**.")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o **mestre** pode solicitar narrativas.")
        
        if not prompt:
            return await ctx.send("❌ Use: `!narrativa <descrição da situação>`")
        
        if sessao.get("status") != "em_andamento":
            return await ctx.send("⚠️ A aventura ainda não começou!")
        
        await ctx.send("✨ *Lyra está tecendo a narrativa...*")
        
        sistema = sessao.get("sistema", "dnd5e")
        estilo = sessao.get("estilo_narrativo", "extenso")
        historia = sessao.get("historia", [])
        
        if estilo == "extenso":
            max_tokens = 1200
            instrucao = "Narre em 3-5 parágrafos detalhados, cinematográficos e imersivos."
        else:
            max_tokens = 400
            instrucao = "MÁXIMO 4 FRASES CURTAS. Seja extremamente direto e objetivo."
        
        historia.append({"role": "user", "content": f"Mestre descreve situação: {prompt}"})
        historia_recente = historia[-20:]
        
        # Usa novos prompts v3.0
        from core.sessao_prompts import get_narrative_system_prompt, get_master_narrative_instructions
        
        system_prompt = get_narrative_system_prompt(sistema, estilo)
        
        mensagens = [
            {"role": "system", "content": system_prompt},
        ] + historia_recente + [
            {"role": "user", "content": f"{instrucao} Lembre-se: NUNCA solicite rolagens. O mestre humano decidirá isso."}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=max_tokens)
        
        historia.append({"role": "assistant", "content": resposta})
        sessao["historia"] = historia
        salvar_dados()
        
        embed = discord.Embed(
            title="📖 Narrativa de Lyra",
            description=resposta[:4000],
            color=discord.Color.purple()
        )
        
        # Usa nova função de instruções
        from core.sessao_prompts import get_master_narrative_instructions
        embed.set_footer(text=get_master_narrative_instructions())
        
        # Mestre recebe botões de controle
        view = MasterControlView(
            bot, sessoes_ativas, fichas_personagens, 
            chamar_groq, get_system_prompt, salvar_dados
        )
        
        await ctx.send(embed=embed, view=view)
        
        # Orientação visual para jogadores
        from core.sessao_prompts import get_post_narrative_message_for_players
        await ctx.send(get_post_narrative_message_for_players())

    @bot.command(name="acao")
    @commands.guild_only()
    async def acao(ctx: commands.Context, *, descricao: str = None):
        """[JOGADORES] Descrevem suas ações (aguardam aprovação do mestre)."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use **no canal da sessão**.")
        
        if not descricao:
            return await ctx.send("❌ Use: `!acao <descrição do que seu personagem faz>`")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        if ctx.author.id != sessao.get("mestre_id") and ctx.author.id not in sessao.get("jogadores", []):
            return await ctx.send("⚠️ Você não faz parte desta sessão.")
        
        if sessao.get("status") != "em_andamento":
            return await ctx.send("⚠️ A aventura ainda não começou!")
        
        # Pega nome do personagem
        fichas_sel = sessao.get("fichas", {})
        chave_ficha = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
        
        if chave_ficha and chave_ficha in fichas_personagens:
            ficha = fichas_personagens[chave_ficha]
            nome_personagem = ficha.get("nome", ctx.author.display_name)
        else:
            nome_personagem = ctx.author.display_name
        
        # Registra ação pendente
        if "acoes_pendentes" not in sessao:
            sessao["acoes_pendentes"] = {}
        
        sessao["acoes_pendentes"][ctx.author.id] = {
            "nome": nome_personagem,
            "acao": descricao
        }
        salvar_dados()
        
        await ctx.send(embed=discord.Embed(
            title=f"🎭 {nome_personagem} age!",
            description=descricao,
            color=discord.Color.blue()
        ).set_footer(text="Aguardando aprovação do mestre | Use !acoespendentes para ver"))
        
        # Notifica mestre
        mestre_id = sessao.get("mestre_id")
        mestre = ctx.guild.get_member(mestre_id)
        if mestre:
            await ctx.send(
                f"📢 {mestre.mention}, {nome_personagem} declarou uma ação!\n"
                f"💡 Use `!narrativa <consequências>` para narrar o resultado ou os botões de controle."
            )

    @bot.command(name="acoespendentes")
    @commands.guild_only()
    async def acoes_pendentes(ctx: commands.Context):
        """[MESTRE] Lista todas as ações declaradas pelos jogadores."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use **no canal da sessão**.")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o **mestre** pode ver ações pendentes.")
        
        acoes = sessao.get("acoes_pendentes", {})
        
        if not acoes:
            return await ctx.send("✅ Não há ações pendentes no momento.")
        
        descricao = ""
        for uid, info in acoes.items():
            descricao += f"• **{info['nome']}**: {info['acao']}\n\n"
        
        embed = discord.Embed(
            title="📋 Ações Declaradas pelos Jogadores",
            description=descricao[:4000],
            color=discord.Color.gold()
        )
        embed.set_footer(text="Use !narrativa para narrar as consequências")
        
        await ctx.send(embed=embed)

    @bot.command(name="limparacoes")
    @commands.guild_only()
    async def limpar_acoes(ctx: commands.Context):
        """[MESTRE] Limpa todas as ações pendentes após narrativa."""
        if ctx.channel.id not in sessoes_ativas:
            return await ctx.send("❌ Use **no canal da sessão**.")
        
        sessao = sessoes_ativas[ctx.channel.id]
        
        if ctx.author.id != sessao.get("mestre_id"):
            return await ctx.send("⚠️ Apenas o **mestre** pode limpar ações.")
        
        sessao["acoes_pendentes"] = {}
        salvar_dados()
        
        await ctx.send("🧹 Ações pendentes limpas!")