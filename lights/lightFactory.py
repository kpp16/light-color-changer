from lights.AbstractLight import get_light_class, BaseLight
from lights.vendors import KasaLight

class LightFactory:
    def __init__(self):
        pass

    async def create_light(self, vendor: str, **kwargs) -> BaseLight:
        light_cls = get_light_class(vendor)
        return await light_cls.connect(**kwargs)
