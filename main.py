import asyncio
import time
import os

from ImageLib import get_dominant_color
from dotenv import load_dotenv
from lights.lightFactory import LightFactory
from SpotifyRunner import SpotifyRunner

load_dotenv()

USERNAME = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
LIGHT_HOST = os.getenv("LIGHT_HOST")

async def main():
    lightFactory = LightFactory()
    spotifyRunner = SpotifyRunner()

    light = await lightFactory.create_light("tp-link",
                                      ip = LIGHT_HOST,
                                      username = USERNAME,
                                      password = PASSWORD,
                                      discovery_timeout=10)
    try:
        if not light.is_on:
            await light.turn_on()

        while True:
            image = spotifyRunner.getImage()
            rgb = get_dominant_color(image)
            try:
                await light.set_color(rgb)
            except Exception as e:
                print(e)
            time.sleep(20)

    except KeyboardInterrupt:
        await light.disconnect()

if __name__ == "__main__":
    asyncio.run(main())