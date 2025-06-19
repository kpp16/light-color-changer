from abc import ABC, abstractmethod
from typing import Type, Dict

class BaseLight(ABC):
    @property
    @abstractmethod
    def is_on(self) -> bool:
        """Return whether the light is currently on."""
        pass

    @is_on.setter
    @abstractmethod
    def is_on(self, value: bool):
        pass

    @abstractmethod
    async def connect(cls, **kwargs):
        pass

    @abstractmethod
    async def turn_on(self):
        pass

    @abstractmethod
    async def turn_off(self):
        pass

    @abstractmethod
    async def set_color(self, rgb):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

_light_registry: Dict[str, Type['BaseLight']] = {}

def register_light(vendor_name: str):
    print("Vendor name: ", vendor_name)
    def decorator(cls):
        _light_registry[vendor_name.lower()] = cls
        return cls
    return decorator

def get_light_class(vendor: str):
    cls = _light_registry.get(vendor.lower())
    if not cls:
        raise ValueError(f"No light class registered for vendor: {vendor}")
    return cls
