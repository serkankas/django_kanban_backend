from channels.generic.websocket import AsyncWebsocketConsumer

from datetime import datetime
import asyncio
import json

class ServerTimeWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_server_time()

    async def send_server_time(self):
        while(True):
            date = datetime.now().strftime('%Y-%m-%d')
            time = datetime.now().strftime('%H:%M:%S')

            await self.send(text_data=json.dumps({"date":date, "time":time}))
            await asyncio.sleep(1)
