# game/events.py

class Event:
    def __init__(self, name):
        self._handlers = []
        self.name = name
        print(f"Создано новое событие {self.name}: {id(self)}")  # Отладочный вывод

    def subscribe(self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)
            print(f"[EVENT] [+] К {self.name} подписан обработчик: : {handler}")  # Отладка

    def unsubscribe(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)
            print(f"[EVENT] [-] От {self.name} отписан обработчик: {handler}")  # Отладка

    def fire(self, **kwargs):
        print(f"[EVENT] {self.name} вызывает обработчик {len(self._handlers)} ")  # Отладка
        for handler in self._handlers:
            try:
                handler(**kwargs)
            except Exception as e:
                print(f"Ошибка в обработчике: {e}")
                self.unsubscribe(handler)

# class EventsMeta(type):
#     """Метакласс для реализации синглтона"""
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             print(f"Создаем новый экземпляр Events")  # Отладка
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]
# metaclass=EventsMeta

class Events():
    """Центральный реестр событий"""
    LOG_MESSAGE = Event('LOG_MESSAGE')
    ENTITY_CREATED = Event('ENTITY_CREATED')
    ENTITY_MOVED = Event('ENTITY_MOVED')
    ENTITY_DIED = Event('ENTITY_DIED')
    print("Инициализация событий")

    # def __new__(cls):
    #     if not hasattr(cls, 'initialized'):
    #         print("Инициализация событий")
    #         cls.LOG_MESSAGE = Event('LOG_MESSAGE')
    #         cls.ENTITY_CREATED = Event('ENTITY_CREATED')
    #         cls.ENTITY_MOVED = Event('ENTITY_MOVED')
    #         cls.ENTITY_DIED = Event('ENTITY_DIED')
    #         cls.initialized = True
    #     return super().__new__(cls)

    @classmethod
    def get_log_event(cls):
        return cls.LOG_MESSAGE  # Для отладки

# events = Events()