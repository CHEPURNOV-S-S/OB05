# game/events.py

class Event:
    def __init__(self, name):
        self._handlers = []
        self.name = name

    def subscribe(self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)
            print(f"[EVENT] Subscribed to {self.name}: {handler}")  # Отладка

    def unsubscribe(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)
            print(f"[EVENT] Unsubscribed from {self.name}: {handler}")  # Отладка

    def fire(self, **kwargs):
        print(f"[EVENT] Firing {self.name} to {len(self._handlers)} handlers")  # Отладка
        for handler in self._handlers:
            try:
                handler(**kwargs)
            except Exception as e:
                print(f"Ошибка в обработчике: {e}")

class Events:
    ENTITY_CREATED = Event('ENTITY_CREATED')
    ENTITY_MOVED = Event('ENTITY_MOVED')
    ENTITY_DIED = Event('ENTITY_DIED')

    LOG_MESSAGE = Event('LOG_MESSAGE')

    @classmethod
    def get_log_event(cls):
        return cls.LOG_MESSAGE  # Для отладки