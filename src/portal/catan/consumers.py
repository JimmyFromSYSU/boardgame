import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .data_layer.api import (
    init_game, get_last_game_id,

    update_user,
    get_users_in_room,
)
from .data_layer.player_data import PLAYERS_DATA
from django.contrib.auth.models import User


class CatanConsumer(AsyncConsumer):
    connection_counter = 0
    game_id = None
    user_to_player = {}
    player_orders = {}

    def print_connection_counter(self):
        print(">>>>>>>>>>>>>>>>>>>>>>> INFO: connection_counter")
        print(f"connection_counter = {CatanConsumer.connection_counter}")
        print("<<<<<<<<<<<<<<<<<<<<<<<")

    def print_game_id(self, game_id):
        print(">>>>>>>>>>>>>>>>>>>>>>> INFO: game_id")
        print(f"game_id = {game_id}")
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

        if CatanConsumer.connection_counter == 0:
            map_name = "normal"
            (game_id, user_to_player, player_orders) = init_game(map_name, {})
            CatanConsumer.game_id = game_id
            CatanConsumer.user_to_player = user_to_player
            CatanConsumer.player_orders = player_orders
        else:
            # game_id = get_last_game_id()
            game_id = CatanConsumer.game_id
            user_to_player = CatanConsumer.user_to_player
            player_orders = CatanConsumer.player_orders

        CatanConsumer.connection_counter = CatanConsumer.connection_counter + 1

        self.print_connection_counter()

        self.print_game_id(game_id)
        self.game_room = f"game_room_{game_id}"
        await self.channel_layer.group_add(
            self.game_room,
            self.channel_name, # channel_name appear only when channel layer is setup
        )

        # # send to single user
        # response = {
        #     'action': 'INIT_INFO',
        #     'game_id': game_id,
        #     # 'number_of_players': len()
        #     # 'players': PLAYERS_DATA,
        # }
        # await self.send(
        #     {
        #         "type": "websocket.send",
        #         "text": json.dumps(response),
        #     }
        # )

        # send to all users
        response = {
            'action': 'INIT_GAME',
            'game_id': game_id,
            'players': PLAYERS_DATA,
        }

        await self.channel_layer.group_send(
            self.game_room,
            {
                "type": "chat_message",  # handler name
                "text": json.dumps(response) # handler event data
            }
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
        CatanConsumer.connection_counter = CatanConsumer.connection_counter - 1
        self.print_event("disconnected", event)
        self.print_connection_counter()




class CatanRoomConsumer(AsyncConsumer):
    def print_id(self, room_id, user_id):
        print(">>>>>>>>>>>>>>>>>>>>>>> INFO: id")
        print(f"room_id = {room_id}")
        print(f"user_id = {user_id}")
        print("<<<<<<<<<<<<<<<<<<<<<<<")


    def print_event(self, name, event):
        print(f">>>>>>>>>>>>>>>>>>>>>>> EVENT: {name}")
        print(event)
        print(f"<<<<<<<<<<<<<<<<<<<<<<<")

    async def websocket_connect(self, event):
        # self.print_event("connected", event)

        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    @database_sync_to_async
    def get_users(self, user_ids):
        users = [User.objects.get(id=user_id) for user_id in user_ids]
        return users

    async def websocket_receive(self, event):

        # TODO: Before the state machine, add a lock to protect the states.
        self.print_event("receive", event)

        text = event.get('text', None)
        response = {'action': 'UNKNOWN'}

        if text:
            data = json.loads(text)
            if "action" in data:
                room_id = int(data['room_id'])
                user_id = int(data['user_id'])
                if data['action'] == "ADD_USER":
                    update_user(user_id, room_id)
                    users = await get_users_in_room(room_id)
                    # users = await self.get_users(user_ids)
                    users_info = [
                        {
                            'id': user.id,
                            'first_name': user.first_name,
                        }
                        for user in users
                    ]
                    response = {
                        'action': 'COMFIRM_ADD_USER',
                        'users': users_info,
                    }


                self.print_id(room_id, user_id)
                self.room = f"room_{room_id}"
                await self.channel_layer.group_add(
                    self.room,
                    self.channel_name, # channel_name appear only when channel layer is setup
                )


        await self.channel_layer.group_send(
            self.room,
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
        self.print_event("disconnected", event)
