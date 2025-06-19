import asyncio
import os
import time

from kasa import Discover, Module
from dotenv import load_dotenv
from kasa import Discover, Module, Device

from ImageLib import rgb_to_hsv
from lights.AbstractLight import BaseLight, register_light

@register_light("kasa")
@register_light("tp-link")
class KasaLight(BaseLight):
    def __init__(self, ip: str, dev: Device, light: Module):
        self.ip = ip
        self.dev = dev
        self.light = light
        self.is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on
    
    @is_on.setter
    def is_on(self, value: bool):
        self._is_on = value
    
    @classmethod
    async def connect(cls, **kwargs):
        dev = await Discover.discover_single(
            host = kwargs["ip"],
            username = kwargs.get("username"),
            password = kwargs.get("password"),
            discovery_timeout = kwargs.get("discovery_timeout", 10)
        )
        await dev.update()
        light = dev.modules[Module.Light]
        return cls(kwargs["ip"], dev, light)

    async def turn_on(self):
        await self.dev.turn_on()
        self.is_on = True
    
    async def turn_off(self):
        await self.dev.turn_off()
        self.is_on = False
    
    async def set_color(self, rgb):
        if self.is_on:
            h,s,v = rgb_to_hsv(*rgb)
            await self.light.set_hsv(h, s, v)
        else:
            print("Light is turned off!")
    
    async def disconnect(self):
        await self.dev.disconnect()
