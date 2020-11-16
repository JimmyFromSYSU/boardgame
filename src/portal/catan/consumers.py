import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async


class CatanConsumer(AsyncConsumer):
    counter = 0
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )
        response = {
            "message": "Hello world",
        }
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(response),
            }
        )

        self.game_room = f"game_room_1"
        await self.channel_layer.group_add(
            self.game_room,
            self.channel_name, # channel_name appear only when channel layer is setup
        )

    async def websocket_receive(self, event):
        print("receive", event)
        text = event.get('text', None)
        response = {}

        if text:
            data = json.loads(text)
            if "action" in data:
                if data['action'] == "BUILD_HOUSE":
                    response = {
                        'action': 'COMFIRM_BUILD_HOUSE',
                        'x': data['x'],
                        'y': data['y'],
                        'z': data['z'],
                    }
                elif data['action'] == "BUILD_TOWN":
                    response = {
                        'action': 'COMFIRM_BUILD_TOWN',
                        'x': data['x'],
                        'y': data['y'],
                        'z': data['z'],
                    }
                elif data['action'] == "BUILD_ROAD":
                    response = {
                        'action': 'COMFIRM_BUILD_ROAD',
                        'x': data['x'],
                        'y': data['y'],
                        'z': data['z'],
                    }
            elif "message" in data:
                print(f"message is: {data['message']}")
                response = {
                    "message": f"echo {data['message']}",
                }

        CatanConsumer.counter = CatanConsumer.counter + 1
        print(f"counter: {CatanConsumer.counter}")
        await self.channel_layer.group_send(
            self.game_room,
            {
                "type": "chat_message",  # handler name
                "text": json.dumps(response) # handler event data
            }
        )

    async def chat_message(self, event):
        print("message", event)
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })


    async def websocket_disconnect(self, event):
        print("disconnected", event)
