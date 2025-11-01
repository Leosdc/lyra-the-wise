"""
Sistema de combate completo para Lyra the Wise.
Rastreia HP, iniciativa, turnos e integra com fichas estruturadas.
"""

import random
import re
from typing import Dict, List, Tuple, Any, Optional


class CombatTracker:
    """Rastreia estado de combate: HP, CA, iniciativa, turnos."""
    
    def __init__(self):
        self.is_active = False
        self.round = 0
        self.participants: Dict[str, Dict[str, Any]] = {}
        self.turn_order: List[str] = []
        self.current_turn_index = 0
    
    def start_combat(self):
        """Inicia o combate."""
        self.is_active = True
        self.round = 1
        self.current_turn_index = 0
    
    def add_participant(
        self, 
        name: str, 
        hp: int, 
        max_hp: int, 
        ca: int, 
        is_player: bool = True,
        player_id: Optional[int] = None,
        bonus_ini: int = 0
    ):
        """Adiciona participante (jogador ou inimigo)."""
        self.participants[name] = {
            "nome": name,
            "hp": hp,
            "max_hp": max_hp,
            "ca": ca,
            "initiative": 0,
            "tipo": "jogador" if is_player else "inimigo",
            "is_player": is_player,
            "is_dead": False,
            "bonus_ini": bonus_ini,
            "player_id": player_id
        }
    
    def roll_initiative(self, name: str, bonus: int = 0) -> int:
        """Rola iniciativa para um participante."""
        roll = random.randint(1, 20) + bonus
        if name in self.participants:
            self.participants[name]["initiative"] = roll
        return roll
    
    def sort_initiative(self):
        """Ordena participantes por iniciativa (maior primeiro)."""
        self.turn_order = sorted(
            self.participants.keys(),
            key=lambda x: self.participants[x]["initiative"],
            reverse=True
        )
        self.current_turn_index = 0
    
    def get_current_turn(self) -> Optional[str]:
        """Retorna o nome do participante no turno atual."""
        if not self.turn_order:
            return None
        return self.turn_order[self.current_turn_index]
    
    def next_turn(self):
        """Avança para o próximo turno."""
        if not self.turn_order:
            return
        
        self.current_turn_index += 1
        
        if self.current_turn_index >= len(self.turn_order):
            self.current_turn_index = 0
            self.round += 1
    
    def apply_damage(self, target: str, damage: int) -> bool:
        """Aplica dano a um alvo. Retorna True se morreu."""
        if target not in self.participants:
            return False
        
        self.participants[target]["hp"] -= damage
        
        if self.participants[target]["hp"] <= 0:
            self.participants[target]["hp"] = 0
            self.participants[target]["is_dead"] = True
            return True
        
        return False
    
    def heal(self, target: str, amount: int):
        """Cura um alvo."""
        if target not in self.participants:
            return
        
        participant = self.participants[target]
        participant["hp"] = min(participant["hp"] + amount, participant["max_hp"])
        
        if participant["hp"] > 0:
            participant["is_dead"] = False
    
    def get_status(self) -> str:
        """Retorna status visual do combate."""
        if not self.is_active:
            return "❌ Nenhum combate ativo."
        
        status = f"⚔️ **Combate — Rodada {self.round}**\n\n"
        
        # Jogadores
        players = [name for name, data in self.participants.items() if data.get("tipo") == "jogador"]
        if players:
            status += "👥 **Jogadores**\n"
            for name in players:
                data = self.participants[name]
                current = "👉 " if self.get_current_turn() == name else ""
                hp_bar = self._get_hp_bar(data["hp"], data["max_hp"])
                ini = data.get("initiative", 0)
                
                status += f"{current}**{name}** (Ini: {ini})\n"
                status += f"{hp_bar} {data['hp']}/{data['max_hp']} HP | CA {data['ca']}\n\n"
        
        # Inimigos
        enemies = [name for name, data in self.participants.items() if data.get("tipo") == "inimigo"]
        if enemies:
            status += "👹 **Inimigos**\n"
            for name in enemies:
                data = self.participants[name]
                current = "👉 " if self.get_current_turn() == name else ""
                
                if data.get("is_dead", False):
                    status += f"{current}💀 **{name}** (Ini: {data.get('initiative', 0)})\n"
                    status += f"💀 0/{data['max_hp']} HP | CA {data['ca']}\n\n"
                else:
                    hp_bar = self._get_hp_bar(data["hp"], data["max_hp"])
                    status += f"{current}**{name}** (Ini: {data.get('initiative', 0)})\n"
                    status += f"{hp_bar} {data['hp']}/{data['max_hp']} HP | CA {data['ca']}\n\n"
        
        # Turno atual
        current = self.get_current_turn()
        if current:
            status += f"**Turno de:** {current}\n"
            current_data = self.participants.get(current, {})
            if current_data.get("tipo") == "jogador":
                status += "Use `!atacar <alvo> <dano>` ou `!curar <alvo> <HP>`"
            else:
                status += "Turno do inimigo (mestre narra)"
        
        return status
    
    def _get_hp_bar(self, current: int, maximum: int) -> str:
        """Gera barra visual de HP."""
        if maximum == 0:
            return "💀"
        
        percent = current / maximum
        filled = int(percent * 10)
        
        if percent > 0.6:
            bar_char = "🟩"
        elif percent > 0.3:
            bar_char = "🟨"
        else:
            bar_char = "🟥"
        
        bar = bar_char * filled + "▱" * (10 - filled)
        return bar
    
    def check_combat_end(self) -> Optional[str]:
        """Verifica se o combate terminou. Retorna 'players' ou 'enemies' se um lado venceu."""
        players_alive = any(
            not data.get("is_dead", False)
            for name, data in self.participants.items() 
            if data.get("tipo") == "jogador"
        )
        
        enemies_alive = any(
            not data.get("is_dead", False)
            for name, data in self.participants.items() 
            if data.get("tipo") == "inimigo"
        )
        
        # Debug: mostra estado atual
        print(f"🔍 Check Combat End:")
        print(f"  Jogadores vivos: {players_alive}")
        print(f"  Inimigos vivos: {enemies_alive}")
        for name, data in self.participants.items():
            tipo = data.get("tipo", "desconhecido")
            status = "VIVO" if not data.get("is_dead", False) else "MORTO"
            print(f"  - {tipo.capitalize()} '{name}': HP {data['hp']}/{data['max_hp']} ({status})")
        
        # Só declara derrota se TODOS de um lado morrerem
        if not players_alive and not enemies_alive:
            # Empate (todos mortos)
            return None
        elif not players_alive:
            return "enemies"
        elif not enemies_alive:
            return "players"
        
        return None
    
    def end_combat(self) -> Dict[str, int]:
        """Encerra combate e retorna HP final dos jogadores."""
        self.is_active = False
        
        # Retorna HP final dos jogadores para salvar nas fichas
        player_hp = {}
        for name, data in self.participants.items():
            if data.get("tipo") == "jogador":
                player_hp[name] = data["hp"]
        
        # Limpa dados de combate
        self.participants.clear()
        self.turn_order.clear()
        self.round = 0
        self.current_turn_index = 0
        
        return player_hp
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o tracker para dicionário serializável em JSON."""
        return {
            "is_active": self.is_active,
            "round": self.round,
            "participants": self.participants,
            "turn_order": self.turn_order,
            "current_turn_index": self.current_turn_index
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CombatTracker':
        """Reconstrói o tracker a partir de um dicionário."""
        tracker = cls()
        tracker.is_active = data.get("is_active", False)
        tracker.round = data.get("round", 0)
        tracker.participants = data.get("participants", {})
        tracker.turn_order = data.get("turn_order", [])
        tracker.current_turn_index = data.get("current_turn_index", 0)
        return tracker


def extract_character_stats(ficha: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    Extrai HP máximo, HP atual e CA de uma ficha estruturada.
    Retorna (hp_max, hp_atual, ca)
    """
    hp_max = 10  # Padrão
    hp_atual = 10
    ca = 10
    
    # Tenta extrair de ficha estruturada (novo formato)
    if isinstance(ficha, dict):
        # HP
        if "hp_maximo" in ficha:
            hp_max = ficha["hp_maximo"]
        elif "hp" in ficha:
            hp_max = ficha["hp"]
        
        if "hp_atual" in ficha:
            hp_atual = ficha["hp_atual"]
        else:
            hp_atual = hp_max
        
        # CA
        if "ca" in ficha:
            ca = ficha["ca"]
        elif "classe_armadura" in ficha:
            ca = ficha["classe_armadura"]
    
    return hp_max, hp_atual, ca


def detect_combat_in_text(text: str) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Detecta se o texto indica início de combate E extrai detalhes dos inimigos.
    Retorna (is_combat, lista_de_dicionarios_de_inimigos)
    
    Cada inimigo é um dict: {"nome": str, "quantidade": int, "hp_sugerido": int, "ca_sugerido": int}
    """
    combat_keywords = [
        "ataca", "atacam", "investem", "avançam", "saltam",
        "embosca", "surpreendem", "aparecem de repente",
        "iniciativa", "combate", "batalha", "luta",
        "saca a espada", "prepara", "posição de ataque",
        "inimigos", "adversários", "hostis"
    ]
    
    text_lower = text.lower()
    is_combat = any(keyword in text_lower for keyword in combat_keywords)
    
    # Padrões mais avançados para detectar inimigos
    enemy_patterns = [
        # Padrão: "3 goblins", "2 orcs", etc
        (r'(\d+)\s+(goblin|orc|kobold|zumbi|esqueleto|ogro|troll|bandido|guarda|cultista|soldado)s?', 
         lambda m: {"tipo": m.group(2), "quantidade": int(m.group(1))}),
        
        # Padrão: "um dragão", "uma esfinge", etc
        (r'(um|uma)\s+(dragão|demônio|lobisomem|vampiro|lich|esfinge|hidra|golem|espectro)',
         lambda m: {"tipo": m.group(2), "quantidade": 1}),
        
        # Padrão: "grupo de X", "bando de Y"
        (r'(grupo|bando|horda)\s+de\s+(\w+)',
         lambda m: {"tipo": m.group(2), "quantidade": 3}),  # Assume 3 por padrão
    ]
    
    enemies_found = []
    
    for pattern, extractor in enemy_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            enemy_info = extractor(match)
            
            # Atribui HP e CA baseado no tipo
            tipo = enemy_info["tipo"]
            hp_base, ca_base = _get_enemy_stats_by_type(tipo)
            
            enemies_found.append({
                "nome": tipo.capitalize(),
                "quantidade": enemy_info["quantidade"],
                "hp_sugerido": hp_base,
                "ca_sugerido": ca_base
            })
    
    return is_combat, enemies_found


def _get_enemy_stats_by_type(tipo: str) -> Tuple[int, int]:
    """
    Retorna HP e CA base para um tipo de inimigo.
    Retorna (hp, ca)
    """
    # Tabela de stats por tipo (HP, CA)
    enemy_stats = {
        "goblin": (7, 13),
        "orc": (15, 13),
        "kobold": (5, 12),
        "zumbi": (22, 8),
        "esqueleto": (13, 13),
        "ogro": (59, 11),
        "troll": (84, 15),
        "bandido": (11, 12),
        "guarda": (11, 16),
        "cultista": (9, 12),
        "soldado": (16, 18),
        "dragão": (200, 19),
        "demônio": (52, 15),
        "lobisomem": (58, 11),
        "vampiro": (82, 15),
        "lich": (135, 17),
        "esfinge": (136, 17),
        "hidra": (172, 15),
        "golem": (210, 20),
        "espectro": (22, 12),
    }
    
    return enemy_stats.get(tipo, (15, 12))  # Valores padrão se não encontrar


def extract_damage_from_action(action_text: str) -> Optional[int]:
    """
    Tenta extrair valor de dano de uma ação.
    Ex: "ataco com a espada (12 de dano)" -> 12
    """
    # Padrões: "X de dano", "(Xd)" ou "causando X"
    patterns = [
        r'(\d+)\s*de\s*dano',
        r'\((\d+)d\)',
        r'causando\s*(\d+)',
        r'dano:\s*(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, action_text.lower())
        if match:
            return int(match.group(1))
    
    return None