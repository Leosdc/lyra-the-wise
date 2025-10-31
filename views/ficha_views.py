# views/ficha_views.py
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
        
        self.current_page = 0
        self.max_pages = len(self.estrutura["secoes"])
        
    def get_embed(self) -> discord.Embed:
        """Gera embed para a página atual."""
        from sistemas_rpg import SISTEMAS_DISPONIVEIS
        
        secao_nome = self.estrutura["secoes"][self.current_page]
        campos = self.estrutura["campos"][secao_nome]
        
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
            "historia": "📖 História e Personalidade"
        }
        
        titulo = titulos_secoes.get(secao_nome, secao_nome.title())
        
        # Pega dados estruturados ou conteúdo antigo
        if "secoes" in self.ficha_data and self.ficha_data["secoes"]:
            conteudo_secao = self.ficha_data["secoes"].get(secao_nome, {})
            descricao = ""
            
            # NORMALIZA nomes de campos (remove acentos quebrados)
            for campo in campos:
                # Tenta encontrar o campo com encoding correto OU incorreto
                valor = None
                
                # 1. Tenta nome correto
                if campo in conteudo_secao:
                    valor = conteudo_secao[campo]
                else:
                    # 2. Tenta variações com encoding quebrado
                    campo_lower = campo.lower()
                    for k, v in conteudo_secao.items():
                        if k.lower().replace('ã§', 'ç').replace('ã£', 'ã').replace('ãª', 'ê') == campo_lower:
                            valor = v
                            break
                
                if valor is None:
                    valor = "—"
                
                # Formata o valor
                if isinstance(valor, list):
                    valor = ", ".join(str(item) for item in valor)
                elif isinstance(valor, dict):
                    valor = json.dumps(valor, ensure_ascii=False)
                
                descricao += f"**{campo}:** {valor}\n"
        else:
            # Formato antigo - exibe conteúdo bruto
            descricao = self.ficha_data.get("conteudo", "Ficha no formato antigo. Use !editarficha para atualizar.")[:4000]
        
        embed = discord.Embed(
            title=f"📜 {self.ficha_data.get('nome', 'Ficha')}",
            description=descricao,
            color=discord.Color.gold()
        )
        
        embed.set_footer(text=f"Página {self.current_page + 1}/{self.max_pages} • {titulo} • Sistema: {SISTEMAS_DISPONIVEIS[self.sistema]['nome']}")
        
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