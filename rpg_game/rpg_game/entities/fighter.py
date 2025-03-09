# entities/fighter.py

from ..entities.base import Entity, Position, DrawableEntity


class Fighter(DrawableEntity):
    def __init__(self, position: Position, max_ap: int):
        self.max_ap = max_ap
        self.current_ap = max_ap
        self.weapon = None  # Начальное оружие
        self.carried_over_ap = 0
        super().__init__(position, health=100)

    def reset_ap(self):
        """Пересчет ОД после хода"""
        remaining = self.current_ap
        self.carried_over_ap = remaining // 2
        max_possible = int(self.max_ap * 1.5)
        self.current_ap = min(self.max_ap + self.carried_over_ap, max_possible)

    def get_render_info(self) -> dict:
        weapon_str = ''
        if self.weapon:
            weapon_str = self.weapon.name()
        return {
            'sprite_name': 'player.png',  # Только имя файла
            'size': (64, 64),             # Размер спрайта
            'offset': (0, 0),             # Смещение при отрисовки
            'health': self.health,        # Текущее здоровье
            'max_health': 100,            # Максимальное здоровье
            'current_ap': self.current_ap,
            'max_ap': self.max_ap,
            'weapon': weapon_str          # Название оружия
        }

    def change_weapon(self, weapon) -> bool:
        """Смена оружия (1 ОД)"""
        if self.current_ap >= 1:
            self.weapon = weapon
            self.current_ap -= 1
            return True
        return False

    def attack(self, target: Entity) -> bool:
        if not self.weapon:  # Дополнительная проверка
            return False
        if self.current_ap < 1:
            return False

        if self.weapon.is_valid_attack(self, target):
            self.current_ap -= 1
            if self.weapon.execute_attack(self, target):
                return True
        return False
