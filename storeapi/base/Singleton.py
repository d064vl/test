from typing import Any

class Singleton(type):
    def __init__(cls, name, base, namespace):
        cls._instance = None
        super().__init__(name, base, namespace)

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwds)
        
        return cls._instance