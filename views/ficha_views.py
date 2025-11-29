# views/ficha_views.py (CORRIGIDO)
"""Views (botões de navegação) para fichas estruturadas."""

import discord
from discord.ui import View, Button
import json
from typing import Dict, Any


class FichaNavigationView(View):
    """View para navegar entre páginas da ficha."""
    
    def __init__(self, ficha_data: Dict[str, Any], sistema: str, timeout: int = 180):
        super().__init__(timeout=timeout)
        self.ficha_data = ficha_data
        self.sistema = sistema
        
        from core.ficha_helpers import get_estrutura_ficha
        self.estrutura = get_estrutura_ficha(sistema)
        
        secoes_json = list(ficha_data.get("secoes", {}).keys())
        secoes_estrutura = self.estrutura["secoes"]
        
        # Combina seções estruturadas + seções extras do JSON
        self.all_sections = list(dict.fromkeys(secoes_estrutura + secoes_json))
        
        self.current_page = 0
        self.max_pages = len(self.all_sections)
        
    def get_embed(self) -> discord.Embed:
        """Gera embed para a página atual."""
        from sistemas_rpg import SISTEMAS_DISPONIVEIS
        
        secao_nome = self.all_sections[self.current_page]
        
        # Títulos bonitos para as seções
        titulos_secoes = {
            "basico": "📋 Dados Básicos",
            "atributos": "💪 Atributos",
            "recursos": "❤️ Recursos e Pontos",
            "combate": "⚔️ Combate",
            "equipamento": "🎒 Equipamento",
            "magia": "✨ Magia e Conjuração",
            "disciplinas": "🩸 Disciplinas Vampíricas",
            "pericia": "🔍 Perícias",
            "perícias": "🔍 Perícias",
            "pericias": "🔍 Perícias",
            "historia": "📖 História e Personalidade",
            "progressao": "📊 Progressão e XP"
        }
        
        titulo = titulos_secoes.get(secao_nome, secao_nome.title())
        
        # Pega dados estruturados ou conteúdo antigo
        if "secoes" in self.ficha_data and self.ficha_data["secoes"]:
            conteudo_secao = self.ficha_data["secoes"].get(secao_nome, {})
            descricao = ""
            
            if isinstance(conteudo_secao, dict):
                for campo, valor in conteudo_secao.items():
                    # Formata o valor
                    if valor is None:
                        valor = "—"
                    elif isinstance(valor, list):
                        if not valor:
                            valor = "—"
                        else:
                            # Lista de dicts (ex: inventário)
                            if valor and isinstance(valor[0], dict):
                                valor_formatado = []
                                for item in valor:
                                    if isinstance(item, dict):
                                        nome_item = item.get("nome", "Item")
                                        qtd = item.get("quantidade", 1)
                                        valor_formatado.append(f"{nome_item} x{qtd}")
                                    else:
                                        valor_formatado.append(str(item))
                                valor = "\n  • " + "\n  • ".join(valor_formatado)
                            else:
                                # Lista simples
                                valor = ", ".join(str(item) for item in valor)
                    elif isinstance(valor, dict):
                        # Dict aninhado (ex: Equipado)
                        valor_formatado = []
                        for k, v in valor.items():
                            valor_formatado.append(f"{k}: {v}")
                        valor = "\n  • " + "\n  • ".join(valor_formatado)
                    
                    descricao += f"**{campo}:** {valor}\n"
            else:
                # Seção não é dict (texto puro)
                descricao = str(conteudo_secao)
        else:
            # Formato antigo - exibe conteúdo bruto
            descricao = self.ficha_data.get("conteudo", "Ficha no formato antigo. Use !editarficha para atualizar.")[:4000]
        
        if not descricao or descricao.strip() == "":
            descricao = "— Nenhum dado nesta seção."
        
        embed = discord.Embed(
            title=f"📜 {self.ficha_data.get('nome', 'Ficha')}",
            description=descricao[:4000],
            color=discord.Color.gold()
        )
        
        sistema_nome = SISTEMAS_DISPONIVEIS.get(self.sistema, {}).get('nome', self.sistema)
        embed.set_footer(text=f"Página {self.current_page + 1}/{self.max_pages} • {titulo} • Sistema: {sistema_nome}")
        
        return embed
    
    @discord.ui.button(label="◀️ Anterior", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        """Vai para a página anterior."""
        self.current_page = (self.current_page - 1) % self.max_pages
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    @discord.ui.button(label="▶️ Próxima", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        """Vai para a próxima página."""
        self.current_page = (self.current_page + 1) % self.max_pages
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: discord.Interaction, button: Button):
        """Fecha a visualização."""
        await interaction.message.delete()