# commands/geracao_combate.py
"""Comandos de geração de monstros, encontros e armadilhas."""

import discord
from discord.ext import commands


def register_combate_commands(bot: commands.Bot, sistemas_rpg, SISTEMAS_DISPONIVEIS, chamar_groq, get_system_prompt, buscar_monstro, listar_monstros_por_sistema, formatar_monstro):
    """Registra comandos de geração de combate."""

    def get_sistema_usuario(user_id):
        """Retorna o sistema configurado para o USUÁRIO."""
        return sistemas_rpg.get(user_id, "dnd5e")

    # Remove comandos duplicados
    for cmd in ["monstro", "monstros", "encontro", "armadilha"]:
        try:
            bot.remove_command(cmd)
        except Exception:
            pass

    @bot.command(name="monstro")
    async def monstro(ctx, *, nome: str = None):
        """Busca ou gera um monstro. Uso: !monstro <nome> ou !monstro para gerar novo"""
        sistema = get_sistema_usuario(ctx.author.id)
        
        if nome:
            monstro_db = buscar_monstro(nome, sistema)
            
            if monstro_db:
                texto = formatar_monstro(monstro_db)
                embed = discord.Embed(
                    title=f"👹 {monstro_db['nome']}",
                    description=texto[:4000],
                    color=discord.Color.dark_red()
                )
                embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']} | Do banco de dados")
                await ctx.send(embed=embed)
                return
            
            system_prompt = get_system_prompt(sistema)
            prompt = f"Crie as estatísticas completas de combate para o monstro **{nome}** no sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Inclua: atributos, ataques, habilidades especiais, pontos de vida e nível de desafio. Seja detalhado e balanceado."
        else:
            system_prompt = get_system_prompt(sistema)
            prompt = f"Crie um monstro original e interessante para o sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']}, com estatísticas completas de combate, habilidades únicas e uma breve descrição atmosférica. Seja criativo!"
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"👹 {'Gerando' if nome else 'Criando'} monstro{' ' + nome if nome else ' aleatório'}...")
        resposta = await chamar_groq(mensagens, max_tokens=1500)
        
        embed = discord.Embed(
            title=f"👹 {nome if nome else 'Monstro Gerado'}",
            description=resposta[:4000],
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=f"Sistema: {SISTEMAS_DISPONIVEIS[sistema]['nome']} | Gerado por IA")
        await ctx.send(embed=embed)

    @bot.command(name="monstros")
    async def listar_monstros(ctx):
        """Lista todos os monstros disponíveis no banco de dados para o sistema atual."""
        from views.pagination_views import create_monstros_pages
        
        sistema = get_sistema_usuario(ctx.author.id)
        monstros = listar_monstros_por_sistema(sistema)
        
        if not monstros:
            await ctx.send(f"❌ Nenhum monstro catalogado para {SISTEMAS_DISPONIVEIS[sistema]['nome']} ainda.")
            return
        
        try:
            view = create_monstros_pages(monstros, SISTEMAS_DISPONIVEIS[sistema]['nome'])
            await ctx.send(embed=view.get_embed(), view=view)
        except Exception as e:
            print(f"❌ Erro ao criar view paginada: {e}")
            # Fallback para método antigo
            lista = "\n".join([f"• {m}" for m in monstros])
            embed = discord.Embed(
                title=f"👹 Monstros - {SISTEMAS_DISPONIVEIS[sistema]['nome']}",
                description=f"Use `!monstro <nome>` para ver detalhes\n\n{lista}",
                color=discord.Color.dark_red()
            )
            embed.set_footer(text=f"{len(monstros)} monstros disponíveis")
            await ctx.send(embed=embed)

    @bot.command(name="encontro")
    async def encontro(ctx, nivel: int = None, dificuldade: str = "medio"):
        """Gera um encontro balanceado. Uso: !encontro <nível> <facil/medio/dificil>"""
        sistema = get_sistema_usuario(ctx.author.id)
        system_prompt = get_system_prompt(sistema)
        
        if not nivel:
            nivel = 5
        
        dif_map = {
            "facil": "fácil", "fácil": "fácil",
            "medio": "médio", "médio": "médio",
            "dificil": "difícil", "difícil": "difícil"
        }
        dificuldade = dif_map.get(dificuldade.lower(), "médio")
        
        prompt = f"Crie um encontro de combate balanceado para um grupo de nível {nivel} no sistema {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Dificuldade: {dificuldade}. Inclua: inimigos com estatísticas completas, táticas de combate, descrição do ambiente e possíveis recompensas."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"⚔️ Gerando encontro nível {nivel} ({dificuldade})...")
        resposta = await chamar_groq(mensagens, max_tokens=1800)
        
        embed = discord.Embed(
            title=f"⚔️ Encontro - Nível {nivel} ({dificuldade.capitalize()})",
            description=resposta[:4000],
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @bot.command(name="armadilha")
    async def armadilha(ctx, dificuldade: str = "medio"):
        """Gera uma armadilha. Uso: !armadilha <facil/medio/dificil>"""
        sistema = get_sistema_usuario(ctx.author.id)
        system_prompt = get_system_prompt(sistema)
        
        dif_map = {
            "facil": "fácil", "fácil": "fácil",
            "medio": "médio", "médio": "médio",
            "dificil": "difícil", "difícil": "difícil"
        }
        dificuldade = dif_map.get(dificuldade.lower(), "médio")
        
        prompt = f"Crie uma armadilha criativa para {SISTEMAS_DISPONIVEIS[sistema]['nome']}. Dificuldade: {dificuldade}. Inclua: mecanismo de ativação, efeito, CD para detectar, CD para desarmar, dano/efeito e possível forma de evitar ou mitigar."
        
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        await ctx.send(f"🪤 Gerando armadilha ({dificuldade})...")
        resposta = await chamar_groq(mensagens, max_tokens=1000)
        
        embed = discord.Embed(
            title=f"🪤 Armadilha ({dificuldade.capitalize()})",
            description=resposta[:4000],
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)