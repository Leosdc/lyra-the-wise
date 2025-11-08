# views/pagination_views.py
"""
Sistema de paginação reutilizável para listas.
"""

import discord
from discord.ui import View, Button
from typing import List, Callable, Optional
import math


class PaginatedListView(View):
    """
    View genérica para paginar qualquer lista de itens.
    
    Args:
        items: Lista de itens a paginar
        items_per_page: Quantos itens por página
        format_func: Função que recebe (item, index) e retorna string formatada
        title: Título do embed
        color: Cor do embed
        footer_template: Template do footer (usa {current}, {total})
        timeout: Timeout da view em segundos
    """
    
    def __init__(
        self,
        items: List,
        items_per_page: int = 10,
        format_func: Callable = None,
        title: str = "Lista",
        color: discord.Color = discord.Color.blurple(),
        footer_template: str = "Página {current}/{total}",
        timeout: int = 180
    ):
        super().__init__(timeout=timeout)
        self.items = items
        self.items_per_page = items_per_page
        self.format_func = format_func or (lambda item, idx: f"• {item}")
        self.title = title
        self.color = color
        self.footer_template = footer_template
        
        self.current_page = 0
        self.max_pages = max(1, math.ceil(len(items) / items_per_page))
        
        # Atualiza botões
        self._update_buttons()
    
    def _update_buttons(self):
        """Atualiza estado dos botões baseado na página atual."""
        # Botão anterior
        self.children[0].disabled = (self.current_page == 0)
        
        # Botão próximo
        self.children[1].disabled = (self.current_page >= self.max_pages - 1)
        
        # Atualiza label da página
        self.children[2].label = f"Página {self.current_page + 1}/{self.max_pages}"
    
    def get_embed(self) -> discord.Embed:
        """Gera embed para a página atual."""
        # Calcula índices
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.items))
        
        # Pega itens da página
        page_items = self.items[start_idx:end_idx]
        
        # Formata itens
        description = "\n".join([
            self.format_func(item, start_idx + i)
            for i, item in enumerate(page_items)
        ])
        
        if not description:
            description = "— Nenhum item encontrado."
        
        embed = discord.Embed(
            title=self.title,
            description=description[:4000],
            color=self.color
        )
        
        # Footer
        footer_text = self.footer_template.format(
            current=self.current_page + 1,
            total=self.max_pages
        )
        embed.set_footer(text=footer_text)
        
        return embed
    
    @discord.ui.button(label="◀️ Anterior", style=discord.ButtonStyle.secondary, row=0)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        """Vai para a página anterior."""
        self.current_page = max(0, self.current_page - 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    @discord.ui.button(label="▶️ Próxima", style=discord.ButtonStyle.secondary, row=0)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        """Vai para a próxima página."""
        self.current_page = min(self.max_pages - 1, self.current_page + 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    @discord.ui.button(label="Página 1/1", style=discord.ButtonStyle.primary, disabled=True, row=0)
    async def page_indicator(self, interaction: discord.Interaction, button: Button):
        """Indicador de página (não clicável)."""
        pass
    
    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger, row=0)
    async def close_button(self, interaction: discord.Interaction, button: Button):
        """Fecha a visualização."""
        await interaction.message.delete()


class PaginatedEmbedsView(View):
    """
    View para paginar embeds completos (quando cada página é um embed diferente).
    Útil para conteúdo mais complexo como !verficha.
    
    Args:
        embeds: Lista de embeds pré-criados
        timeout: Timeout da view em segundos
    """
    
    def __init__(self, embeds: List[discord.Embed], timeout: int = 180):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.current_page = 0
        self.max_pages = len(embeds)
        
        self._update_buttons()
    
    def _update_buttons(self):
        """Atualiza estado dos botões."""
        self.children[0].disabled = (self.current_page == 0)
        self.children[1].disabled = (self.current_page >= self.max_pages - 1)
        self.children[2].label = f"Página {self.current_page + 1}/{self.max_pages}"
    
    def get_current_embed(self) -> discord.Embed:
        """Retorna o embed da página atual."""
        return self.embeds[self.current_page]
    
    @discord.ui.button(label="◀️ Anterior", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        self.current_page = max(0, self.current_page - 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_current_embed(), view=self)
    
    @discord.ui.button(label="▶️ Próxima", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        self.current_page = min(self.max_pages - 1, self.current_page + 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_current_embed(), view=self)
    
    @discord.ui.button(label="Página 1/1", style=discord.ButtonStyle.primary, disabled=True)
    async def page_indicator(self, interaction: discord.Interaction, button: Button):
        pass
    
    @discord.ui.button(label="❌ Fechar", style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: discord.Interaction, button: Button):
        await interaction.message.delete()


# ===== FUNÇÕES AUXILIARES =====

def create_sistemas_pages(sistemas_dict: dict) -> PaginatedListView:
    """
    Cria view paginada para !sistemas.
    
    Args:
        sistemas_dict: SISTEMAS_DISPONIVEIS
    
    Returns:
        PaginatedListView configurada
    """
    items = [
        (codigo, info['nome'])
        for codigo, info in sorted(sistemas_dict.items(), key=lambda x: x[1]['nome'])
    ]
    
    def format_sistema(item, idx):
        codigo, nome = item
        return f"**{nome}** (`{codigo}`)"
    
    return PaginatedListView(
        items=items,
        items_per_page=15,
        format_func=format_sistema,
        title="📚 Sistemas de RPG Suportados",
        color=discord.Color.blue(),
        footer_template="Página {current}/{total} • Total: " + str(len(items)) + " sistemas"
    )


def create_monstros_pages(monstros_lista: list, sistema_nome: str) -> PaginatedListView:
    """
    Cria view paginada para !monstros.
    
    Args:
        monstros_lista: Lista de nomes de monstros
        sistema_nome: Nome do sistema
    
    Returns:
        PaginatedListView configurada
    """
    def format_monstro(item, idx):
        return f"• {item}"
    
    return PaginatedListView(
        items=sorted(monstros_lista),
        items_per_page=20,
        format_func=format_monstro,
        title=f"👹 Monstros — {sistema_nome}",
        color=discord.Color.dark_red(),
        footer_template="Página {current}/{total} • Total: " + str(len(monstros_lista)) + " monstros"
    )


def create_fichas_pages(fichas_dict: dict, user_id: int, SISTEMAS_DISPONIVEIS: dict) -> PaginatedListView:
    """
    Cria view paginada para !minhasfichas.
    
    Args:
        fichas_dict: fichas_personagens
        user_id: ID do usuário
        SISTEMAS_DISPONIVEIS: Dicionário de sistemas
    
    Returns:
        PaginatedListView configurada
    """
    # Filtra e organiza fichas por sistema
    fichas_user = {k: v for k, v in fichas_dict.items() if v.get("autor") == user_id}
    
    sistemas_dict = {}
    for ficha in fichas_user.values():
        sistema = ficha.get("sistema", "dnd5e")
        sistemas_dict.setdefault(sistema, []).append(ficha)
    
    # Cria lista formatada
    items = []
    for sistema, fichas_lista in sorted(sistemas_dict.items()):
        sistema_nome = SISTEMAS_DISPONIVEIS.get(sistema, {}).get('nome', sistema)
        items.append(('header', sistema_nome, len(fichas_lista)))
        
        for ficha in sorted(fichas_lista, key=lambda f: f.get('nome', '')):
            nome = ficha['nome']
            tipo = " 📋" if "secoes" in ficha and ficha["secoes"] else " 📄"
            items.append(('ficha', nome + tipo, sistema))
    
    def format_ficha(item, idx):
        tipo, conteudo, extra = item
        if tipo == 'header':
            return f"\n🎲 **{conteudo}** ({extra} ficha{'s' if extra > 1 else ''})"
        else:
            return f"  • {conteudo}"
    
    return PaginatedListView(
        items=items,
        items_per_page=15,
        format_func=format_ficha,
        title="📚 Suas Fichas de Personagem",
        color=discord.Color.gold(),
        footer_template="Página {current}/{total} • 📋 = Estruturada | 📄 = Legado"
    )