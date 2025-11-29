# commands/inventario_commands.py
"""
Sistema completo de inventário para fichas.
"""

import discord
from discord.ext import commands
from typing import Dict, Any


def register_inventario_commands(bot: commands.Bot, fichas_personagens: Dict[str, Any], salvar_dados):
    """Registra todos os comandos de inventário."""
    
    @bot.command(name="inventario")
    async def inventario(ctx: commands.Context, *, nome_personagem: str = None):
        """Ver inventário de um personagem."""
        from core.ficha_helpers import encontrar_ficha
        
        chave, ficha = encontrar_ficha(ctx.author.id, nome_personagem or "")
        
        if not ficha:
            return await ctx.send(
                "❌ Ficha não encontrada!\n"
                "💡 Use: `!inventario` (dentro de sessão) ou `!inventario <nome>`"
            )
        
        nome = ficha.get("nome", "Personagem")
        secoes = ficha.get("secoes", {})
        equipamento = secoes.get("equipamento", {})
        
        # Inventário moderno (lista de dicts)
        inventario_items = equipamento.get("Inventário", [])
        
        # Equipado
        equipado = equipamento.get("Equipado", {})
        arma_equipada = equipado.get("Arma", "—")
        armadura_equipada = equipado.get("Armadura", "—")
        
        # Dinheiro
        dinheiro = equipamento.get("Dinheiro", "0 PO")
        
        # Formata inventário
        if isinstance(inventario_items, list) and inventario_items:
            itens_txt = ""
            for item in inventario_items:
                if isinstance(item, dict):
                    nome_item = item.get("nome", "Item")
                    qtd = item.get("quantidade", 1)
                    tipo = item.get("tipo", "")
                    itens_txt += f"• **{nome_item}** x{qtd}"
                    if tipo:
                        itens_txt += f" ({tipo})"
                    itens_txt += "\n"
                else:
                    itens_txt += f"• {item}\n"
        else:
            itens_txt = "— Vazio"
        
        embed = discord.Embed(
            title=f"🎒 Inventário de {nome}",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="⚔️ Equipado",
            value=f"**Arma:** {arma_equipada}\n**Armadura:** {armadura_equipada}",
            inline=False
        )
        
        embed.add_field(
            name="📦 Itens no Inventário",
            value=itens_txt[:1024],
            inline=False
        )
        
        embed.add_field(
            name="💰 Dinheiro",
            value=dinheiro,
            inline=False
        )
        
        embed.set_footer(text="Use !addinventario, !equiparitem, !usaritem, !jogarfora, !vender")
        
        await ctx.send(embed=embed)
    
    @bot.command(name="addinventario")
    async def add_inventario(ctx: commands.Context, *args):
        """
        Adicionar item ao inventário.
        Uso: 
        - !addinventario <item> [quantidade] [tipo]
        - !addinventario "item com espaços" 5 arma
        """
        from core.ficha_helpers import encontrar_ficha, salvar_fichas_agora
        from config import sessoes_ativas
        
        if not args:
            return await ctx.send(
                "❌ **Uso correto:**\n"
                "• `!addinventario <item>` — Adiciona 1 unidade\n"
                "• `!addinventario <item> <quantidade>` — Adiciona quantidade específica\n"
                "• `!addinventario <item> <quantidade> <tipo>` — Com tipo (arma/armadura/consumível/geral)\n\n"
                "**Exemplos:**\n"
                "• `!addinventario Espada` — Adiciona 1 Espada\n"
                "• `!addinventario Poção 5` — Adiciona 5 Poções\n"
                "• `!addinventario \"Cajado Mágico\" 1 arma` — Adiciona 1 Cajado Mágico (tipo: arma)"
            )
        
        # Parse de argumentos flexível
        # args pode ser: ("item",) ou ("item", "5") ou ("item", "5", "arma")
        # ou com aspas: ("item com espaços", "5", "arma")
        
        nome_item = args[0]
        quantidade = 1
        tipo = "geral"
        
        # Tenta extrair quantidade (segundo argumento)
        if len(args) >= 2:
            try:
                quantidade = int(args[1])
            except ValueError:
                # Se não for número, assume que é tipo e quantidade é 1
                tipo = args[1]
        
        # Tenta extrair tipo (terceiro argumento)
        if len(args) >= 3:
            tipo = args[2]
        
        # Valida quantidade
        if quantidade < 1:
            return await ctx.send("❌ Quantidade deve ser no mínimo 1!")
        
        # Detecta ficha ativa
        sessao = sessoes_ativas.get(ctx.channel.id)
        
        if sessao:
            # DENTRO de sessão - usa ficha ativa
            fichas_sel = sessao.get("fichas", {})
            chave = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
            ficha = fichas_personagens.get(chave) if chave else None
        else:
            # FORA de sessão - precisa especificar nome da ficha
            # Mas... isso complica muito. Melhor sempre usar dentro de sessão
            # OU buscar ficha pelo nome do autor (se tiver só uma)
            
            fichas_user = {k: v for k, v in fichas_personagens.items() if v.get("autor") == ctx.author.id}
            
            if len(fichas_user) == 0:
                return await ctx.send(
                    "❌ Você não tem fichas criadas!\n"
                    "💡 Use `!ficha <nome>` ou `!criarficha` para criar uma."
                )
            elif len(fichas_user) == 1:
                # Tem só uma ficha - usa ela
                chave = list(fichas_user.keys())[0]
                ficha = fichas_user[chave]
            else:
                # Tem múltiplas - precisa especificar
                nomes = [f['nome'] for f in fichas_user.values()]
                return await ctx.send(
                    f"❌ Você tem múltiplas fichas: {', '.join(nomes)}\n\n"
                    f"💡 Use este comando **dentro de uma sessão** após `!selecionarficha <nome>`,\n"
                    f"OU use `!inventario <nome_ficha>` para especificar qual ficha."
                )
        
        if not ficha:
            return await ctx.send("❌ Ficha não encontrada!")
        
        nome_personagem = ficha.get("nome", "Personagem")
        secoes = ficha.get("secoes", {})
        
        if "equipamento" not in secoes:
            secoes["equipamento"] = {}
        
        equipamento = secoes["equipamento"]
        
        if "Inventário" not in equipamento:
            equipamento["Inventário"] = []
        
        inventario = equipamento["Inventário"]
        
        # Verifica se item já existe
        item_encontrado = None
        for item in inventario:
            if isinstance(item, dict) and item.get("nome", "").lower() == nome_item.lower():
                item_encontrado = item
                break
        
        if item_encontrado:
            # Aumenta quantidade
            item_encontrado["quantidade"] = item_encontrado.get("quantidade", 1) + quantidade
            await ctx.send(
                f"✅ **{nome_item}** x{quantidade} adicionado! "
                f"Total: {item_encontrado['quantidade']}"
            )
        else:
            # Adiciona novo item
            novo_item = {
                "nome": nome_item,
                "quantidade": quantidade,
                "tipo": tipo
            }
            inventario.append(novo_item)
            await ctx.send(
                f"✅ **{nome_item}** x{quantidade} adicionado ao inventário de **{nome_personagem}**!\n"
                f"🏷️ Tipo: {tipo}"
            )
        
        salvar_fichas_agora()
    
    @bot.command(name="equiparitem")
    async def equipar_item(ctx: commands.Context, *, nome_item: str):
        """Equipar arma ou armadura do inventário."""
        from core.ficha_helpers import salvar_fichas_agora
        from config import sessoes_ativas
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Use dentro de uma sessão!")
        
        fichas_sel = sessao.get("fichas", {})
        chave = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
        ficha = fichas_personagens.get(chave) if chave else None
        
        if not ficha:
            return await ctx.send("❌ Ficha não encontrada!")
        
        nome_personagem = ficha.get("nome", "Personagem")
        secoes = ficha.get("secoes", {})
        equipamento = secoes.get("equipamento", {})
        inventario = equipamento.get("Inventário", [])
        
        # Busca item
        item_encontrado = None
        for item in inventario:
            if isinstance(item, dict) and item.get("nome", "").lower() == nome_item.lower():
                item_encontrado = item
                break
        
        if not item_encontrado:
            return await ctx.send(f"❌ **{nome_item}** não está no seu inventário!")
        
        tipo_item = item_encontrado.get("tipo", "geral").lower()
        
        if "Equipado" not in equipamento:
            equipamento["Equipado"] = {}
        
        equipado = equipamento["Equipado"]
        
        if "arma" in tipo_item or "espada" in nome_item.lower() or "arco" in nome_item.lower():
            equipado["Arma"] = nome_item
            await ctx.send(f"⚔️ **{nome_personagem}** equipou: **{nome_item}**!")
        elif "armadura" in tipo_item or "couro" in nome_item.lower() or "cota" in nome_item.lower():
            equipado["Armadura"] = nome_item
            await ctx.send(f"🛡️ **{nome_personagem}** vestiu: **{nome_item}**!")
        else:
            return await ctx.send("❌ Este item não pode ser equipado! (Apenas armas e armaduras)")
        
        salvar_fichas_agora()
    
    @bot.command(name="usaritem")
    async def usar_item(ctx: commands.Context, *, nome_item: str):
        """Usar/consumir item do inventário."""
        from core.ficha_helpers import salvar_fichas_agora
        from config import sessoes_ativas
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Use dentro de uma sessão!")
        
        fichas_sel = sessao.get("fichas", {})
        chave = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
        ficha = fichas_personagens.get(chave) if chave else None
        
        if not ficha:
            return await ctx.send("❌ Ficha não encontrada!")
        
        nome_personagem = ficha.get("nome", "Personagem")
        secoes = ficha.get("secoes", {})
        equipamento = secoes.get("equipamento", {})
        inventario = equipamento.get("Inventário", [])
        
        # Busca item
        item_encontrado = None
        item_index = None
        for i, item in enumerate(inventario):
            if isinstance(item, dict) and item.get("nome", "").lower() == nome_item.lower():
                item_encontrado = item
                item_index = i
                break
        
        if not item_encontrado:
            return await ctx.send(f"❌ **{nome_item}** não está no seu inventário!")
        
        # Reduz quantidade
        qtd_atual = item_encontrado.get("quantidade", 1)
        
        if qtd_atual > 1:
            item_encontrado["quantidade"] = qtd_atual - 1
            await ctx.send(f"✅ **{nome_personagem}** usou **{nome_item}**! Restam {qtd_atual - 1}.")
        else:
            # Remove item
            inventario.pop(item_index)
            await ctx.send(f"✅ **{nome_personagem}** usou o último **{nome_item}**!")
        
        salvar_fichas_agora()
    
    @bot.command(name="jogarfora")
    async def jogar_fora(ctx: commands.Context, *, nome_item: str):
        """Descartar item do inventário."""
        from core.ficha_helpers import salvar_fichas_agora
        from config import sessoes_ativas
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Use dentro de uma sessão!")
        
        fichas_sel = sessao.get("fichas", {})
        chave = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
        ficha = fichas_personagens.get(chave) if chave else None
        
        if not ficha:
            return await ctx.send("❌ Ficha não encontrada!")
        
        nome_personagem = ficha.get("nome", "Personagem")
        secoes = ficha.get("secoes", {})
        equipamento = secoes.get("equipamento", {})
        inventario = equipamento.get("Inventário", [])
        
        # Busca e remove item
        item_index = None
        for i, item in enumerate(inventario):
            if isinstance(item, dict) and item.get("nome", "").lower() == nome_item.lower():
                item_index = i
                break
        
        if item_index is None:
            return await ctx.send(f"❌ **{nome_item}** não está no seu inventário!")
        
        inventario.pop(item_index)
        salvar_fichas_agora()
        
        await ctx.send(f"🗑️ **{nome_personagem}** descartou **{nome_item}**!")
    
    @bot.command(name="vender")
    async def vender(ctx: commands.Context, nome_item: str, preco: int = 0):
        """Vender item do inventário."""
        from core.ficha_helpers import salvar_fichas_agora
        from config import sessoes_ativas
        
        sessao = sessoes_ativas.get(ctx.channel.id)
        if not sessao:
            return await ctx.send("❌ Use dentro de uma sessão!")
        
        fichas_sel = sessao.get("fichas", {})
        chave = fichas_sel.get(str(ctx.author.id)) or fichas_sel.get(ctx.author.id)
        ficha = fichas_personagens.get(chave) if chave else None
        
        if not ficha:
            return await ctx.send("❌ Ficha não encontrada!")
        
        nome_personagem = ficha.get("nome", "Personagem")
        secoes = ficha.get("secoes", {})
        equipamento = secoes.get("equipamento", {})
        inventario = equipamento.get("Inventário", [])
        
        # Busca e remove item
        item_index = None
        for i, item in enumerate(inventario):
            if isinstance(item, dict) and item.get("nome", "").lower() == nome_item.lower():
                item_index = i
                break
        
        if item_index is None:
            return await ctx.send(f"❌ **{nome_item}** não está no seu inventário!")
        
        inventario.pop(item_index)
        
        # Adiciona dinheiro
        dinheiro_atual = equipamento.get("Dinheiro", "0 PO")
        
        try:
            valor_atual = int(dinheiro_atual.split()[0])
        except:
            valor_atual = 0
        
        moeda = dinheiro_atual.split()[-1] if " " in dinheiro_atual else "PO"
        
        novo_valor = valor_atual + preco
        equipamento["Dinheiro"] = f"{novo_valor} {moeda}"
        
        salvar_fichas_agora()
        
        await ctx.send(f"💰 **{nome_personagem}** vendeu **{nome_item}** por **{preco} {moeda}**!")
