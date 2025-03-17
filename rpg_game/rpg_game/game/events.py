# game/events.py
from rpg_game.my_logging import Logger

class Event:
    def __init__(self, name):
        self._handlers = []
        self.name = name
        Logger().debug(f"Создано новое событие {self.name}: {id(self)}")  # Отладочный вывод

    def subscribe(self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)
            Logger().debug(f"[EVENT] [+] К {self.name} подписан обработчик: : {handler}")  # Отладка

    def unsubscribe(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)
            Logger().debug(f"[EVENT] [-] От {self.name} отписан обработчик: {handler}")  # Отладка

    def fire(self, **kwargs):
        Logger().debug(f"[EVENT] {self.name} вызывает обработчик {len(self._handlers)} ")  # Отладка
        for handler in self._handlers:
            try:
                handler(**kwargs)
            except Exception as e:
                Logger().error(f"Ошибка в обработчике: {e}")
                self.unsubscribe(handler)


class Events():
    """Центральный реестр событий"""
    _instance = None

    LOG_MESSAGE = None
    ENTITY_CREATED = None
    ENTITY_MOVED = None
    ENTITY_DIED = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls):
        Logger().debug("Инициализация событий")
        cls.LOG_MESSAGE = Event('LOG_MESSAGE')
        cls.ENTITY_CREATED = Event('ENTITY_CREATED')
        cls.ENTITY_MOVED = Event('ENTITY_MOVED')
        cls.ENTITY_DIED = Event('ENTITY_DIED')

    @classmethod
    def get_log_event(cls):
        return cls.LOG_MESSAGE  # Для отладки

# events = Events()