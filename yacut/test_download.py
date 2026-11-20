import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISK_TOKEN')
URL = "http://127.0.0.1:5000/OwB8UO"


async def main():
    headers = {"Authorization": f"OAuth {TOKEN}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=headers) as resp:
            print(f"Статус ответа: {resp.status}")
            resp.raise_for_status()
            content = await resp.read()
            print(f"Размер файла: {len(content)} байт")
            # Сохраняем, чтобы убедиться, что файл целый
            with open("test_download1.jpg", "wb") as f:
                f.write(content)
            print("Файл успешно скачан и сохранён как test_download1.jpg")

asyncio.run(main())