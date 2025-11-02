# fix_inventario_structure.py
"""
Correção de estrutura de inventário e HP pós-combate.
"""

import discord
from discord.ext import commands
from typing import Dict, Any
import copy


def garantir_estrutura_inventario(ficha: Dict[str, Any]) -> Dict[str, Any]:
    """
    Garante que a estrutura de inventário está correta.
    Corrige automaticamente estruturas antigas.
    """
    if "progressao" not in ficha:
        ficha["progressao"] = {}
    
    if "inventario" not in ficha["progressao"]:
        ficha["progressao"]["inventario"] = []
    
    # CRÍTICO: Corrige se inventario for string
    if isinstance(ficha["progressao"]["inventario"], str):
        ficha["progressao"]["inventario"] = []
    
    # Garante que é uma lista
    if not isinstance(ficha["progressao"]["inventario"], list):
        ficha["progressao"]["inventario"] = []
    
    return ficha


def garantir_estrutura_xp(ficha: Dict[str, Any]) -> Dict[str, Any]:
    """Garante estrutura de XP."""
    if "progressao" not in ficha:
        ficha["progressao"] = {}
    
    if "xp_atual" not in ficha["progressao"]:
        ficha["progressao"]["xp_atual"] = 0
    
    if "xp_proximo_nivel" not in ficha["progressao"]:
        nivel = int(ficha.get("basico", {}).get("Nível", "1"))
        ficha["progressao"]["xp_proximo_nivel"] = calcular_xp_nivel(nivel + 1)
    
    return ficha


def calcular_xp_nivel(nivel: int) -> int:
    """Tabela de XP por nível."""
    XP_TABLE = {
        1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
        6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
        11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
        16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
    }
    return XP_TABLE.get(nivel, 0)


def salvar_hp_pos_combate(bot, sessoes_ativas: Dict, fichas: Dict, salvar_dados):
    """
    Salva HP de todas as fichas após combate.
    """
    for sessao_id, sessao in sessoes_ativas.items():
        if sessao.get("combate_ativo"):
            iniciativa = sessao.get("iniciativa", [])
            
            for entry in iniciativa:
                nome = entry.get("nome")
                hp_atual = entry.get("hp_atual")
                
                # Atualiza na ficha permanente
                if nome in fichas:
                    if "combate" not in fichas[nome]:
                        fichas[nome]["combate"] = {}
                    
                    fichas[nome]["combate"]["HP Atual"] = hp_atual
            
            # Salva após atualizar
            salvar_dados(fichas)


# ===== COMANDO DE MIGRAÇÃO =====
def register(bot: commands.Bot):
    
    @bot.command(name="migrarinventario")
    @commands.has_permissions(administrator=True)
    async def migrar_inventario(ctx: commands.Context):
        """
        [ADMIN] Migra todas as fichas para estrutura v3.0.
        """
        from utils import carregar_dados, salvar_dados
        
        fichas = carregar_dados()
        corrigidas = 0
        erros = []
        
        for nome, ficha in fichas.items():
            try:
                # Garante estruturas
                ficha = garantir_estrutura_inventario(ficha)
                ficha = garantir_estrutura_xp(ficha)
                
                # Garante HP Atual em combate
                if "combate" in ficha:
                    if "HP Atual" not in ficha["combate"]:
                        hp_max = ficha["combate"].get("HP Máximo", 10)
                        ficha["combate"]["HP Atual"] = hp_max
                
                fichas[nome] = ficha
                corrigidas += 1
                
            except Exception as e:
                erros.append(f"{nome}: {str(e)}")
        
        salvar_dados(fichas)
        
        embed = discord.Embed(
            title="✅ Migração Concluída",
            description=f"**{corrigidas}** fichas atualizadas para v3.0",
            color=discord.Color.green()
        )
        
        if erros:
            embed.add_field(
                name="⚠️ Erros",
                value="\n".join(erros[:10]),
                inline=False
            )
        
        await ctx.send(embed=embed)


# ===== INVENTÁRIO COMMANDS (CORRIGIDO) =====
def register_inventario_commands(bot: commands.Bot):
    
    @bot.command(name="addinventario")
    async def add_inventario(ctx: commands.Context, *, item_info: str):
        """
        Adiciona item ao inventário.
        Uso: !addinventario <item> [quantidade]
        """
        from utils import carregar_dados, salvar_dados
        
        fichas = carregar_dados()
        jogador = ctx.author.display_name
        
        if jogador not in fichas:
            await ctx.send(f"❌ Ficha de **{jogador}** não encontrada.")
            return
        
        # Parse: nome [quantidade]
        parts = item_info.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].isdigit():
            nome_item = parts[0]
            quantidade = int(parts[1])
        else:
            nome_item = item_info
            quantidade = 1
        
        # CRÍTICO: Garante estrutura antes de adicionar
        fichas[jogador] = garantir_estrutura_inventario(fichas[jogador])
        
        # Adiciona item
        item = {
            "nome": nome_item,
            "quantidade": quantidade,
            "equipado": False
        }
        
        # Verifica se já existe
        inventario = fichas[jogador]["progressao"]["inventario"]
        item_existente = None
        
        for i in inventario:
            if i.get("nome", "").lower() == nome_item.lower():
                item_existente = i
                break
        
        if item_existente:
            item_existente["quantidade"] += quantidade
            msg = f"✅ **{nome_item}** x{quantidade} adicionado (Total: {item_existente['quantidade']})"
        else:
            inventario.append(item)
            msg = f"✅ **{nome_item}** x{quantidade} adicionado ao inventário!"
        
        salvar_dados(fichas)
        await ctx.send(msg)
    
    
    @bot.command(name="inventario")
    async def ver_inventario(ctx: commands.Context, *, jogador: str = None):
        """
        Mostra inventário do jogador.
        Uso: !inventario [jogador]
        """
        from utils import carregar_dados
        
        fichas = carregar_dados()
        alvo = jogador if jogador else ctx.author.display_name
        
        if alvo not in fichas:
            await ctx.send(f"❌ Ficha de **{alvo}** não encontrada.")
            return
        
        # Garante estrutura
        fichas[alvo] = garantir_estrutura_inventario(fichas[alvo])
        
        inventario = fichas[alvo]["progressao"].get("inventario", [])
        
        if not inventario:
            await ctx.send(f"🎒 **{alvo}** não possui itens no inventário.")
            return
        
        embed = discord.Embed(
            title=f"🎒 Inventário de {alvo}",
            color=discord.Color.gold()
        )
        
        # Separa equipados e não equipados
        equipados = [i for i in inventario if i.get("equipado")]
        nao_equipados = [i for i in inventario if not i.get("equipado")]
        
        if equipados:
            texto = "\n".join([
                f"⚔️ **{i['nome']}** x{i['quantidade']}"
                for i in equipados
            ])
            embed.add_field(name="✅ Equipado", value=texto, inline=False)
        
        if nao_equipados:
            texto = "\n".join([
                f"📦 **{i['nome']}** x{i['quantidade']}"
                for i in nao_equipados
            ])
            embed.add_field(name="📦 Itens", value=texto, inline=False)
        
        await ctx.send(embed=embed)


# ===== FIM DO COMBATE (CORRIGIDO) =====
def register_fim_combate_fix(bot: commands.Bot):
    
    @bot.command(name="fimcombate")
    async def fim_combate(ctx: commands.Context):
        """
        [MESTRE] Finaliza combate e SALVA HP.
        """
        from utils import carregar_dados, salvar_dados
        
        sessoes_ativas = bot.sessoes_ativas
        fichas = carregar_dados()
        
        canal_id = ctx.channel.id
        
        if canal_id not in sessoes_ativas:
            await ctx.send("❌ Não há sessão ativa neste canal.")
            return
        
        sessao = sessoes_ativas[canal_id]
        
        if not sessao.get("combate_ativo"):
            await ctx.send("❌ Não há combate ativo.")
            return
        
        # CRÍTICO: Salva HP antes de limpar
        iniciativa = sessao.get("iniciativa", [])
        salvos = []
        
        for entry in iniciativa:
            nome = entry.get("nome")
            hp_atual = entry.get("hp_atual")
            
            if nome in fichas:
                if "combate" not in fichas[nome]:
                    fichas[nome]["combate"] = {}
                
                fichas[nome]["combate"]["HP Atual"] = hp_atual
                salvos.append(f"{nome}: {hp_atual} HP")
        
        # Salva fichas
        salvar_dados(fichas)
        
        # Limpa combate
        sessao["combate_ativo"] = False
        sessao["iniciativa"] = []
        sessao["turno_atual"] = 0
        
        embed = discord.Embed(
            title="⚔️ Combate Finalizado",
            description="HP salvo nas fichas:",
            color=discord.Color.green()
        )
        
        if salvos:
            embed.add_field(
                name="💾 HP Salvo",
                value="\n".join(salvos),
                inline=False
            )
        
        await ctx.send(embed=embed)
