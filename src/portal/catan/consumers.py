import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .data_layer import init_game

class CatanConsumer(AsyncConsumer):
    counter = 0

    def print_counter(self):
        print(">>>>>>>>>>>>>>>>>>>>>>> INFO: counter")
        print(f"counter = {CatanConsumer.counter}")
        print("<<<<<<<<<<<<<<<<<<<<<<<")

    def print_event(self, name, event):
        print(f">>>>>>>>>>>>>>>>>>>>>>> EVENT: {name}")
        print(event)
        print(f"<<<<<<<<<<<<<<<<<<<<<<<")

    async def websocket_connect(self, event):
        self.print_event("connected", event)

        await self.send(
            {
                "type": "websocket.accept",
            }
        )
        response = {
            "action": "CONFIRM_CONNECTION",
        }
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(response),
            }
        )

        if CatanConsumer.counter == 0:
            map_name = "normal"
            init_game()

        CatanConsumer.counter = CatanConsumer.counter + 1

        self.print_counter()

        self.game_room = f"game_room_1"
        await self.channel_layer.group_add(
            self.game_room,
            self.channel_name, # channel_name appear only when channel layer is setup
        )

    async def websocket_receive(self, event):

        # TODO: Before the state machine, add a lock to protect the states.
        self.print_event("receive", event)

        text = event.get('text', None)
        response = {'action': 'UNKNOWN'}

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
                elif data['action'] == "MOVE_ROBBER":
                    response = {
                        'action': 'COMFIRM_MOVE_ROBBER',
                        'x': data['x'],
                        'y': data['y'],
                    }
                elif data['action'] == "ROLL_DICE":
                    response = {
                        'action': 'COMFIRM_ROLL_DICE',
                        'num1': data['num1'],
                        'num2': data['num2'],
                    }
            elif "message" in data:
                # print(f"message is: {data['message']}")
                response = {
                    "message": f"ECHO: {data['message']}",
                }

        await self.channel_layer.group_send(
            self.game_room,
            {
                "type": "chat_message",  # handler name
                "text": json.dumps(response) # handler event data
            }
        )

    async def chat_message(self, event):
        # print("message", event)
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })


    async def websocket_disconnect(self, event):
        CatanConsumer.counter = CatanConsumer.counter - 1
        self.print_event("disconnected", event)
        self.print_counter()
