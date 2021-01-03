import asyncio
import json
from typing import Dict, Any
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .data_layer.api import (
    init_game, get_last_game_id,
    update_user,
    get_users_in_room,
    get_room_data,
    set_selected_map,
    get_selected_map,
    get_users_config,
)
from .logic.catan_controller import CatanBaseController

from .data_layer.players_data import PLAYERS_DATA
from django.contrib.auth.models import User


def obj_to_json(obj):
    return json.dumps(
        obj,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )


class CatanConsumer(AsyncConsumer):
    def print_connection_counter(self):
        print(">>>>>>>>>>>>>>>>>>>>>>> INFO: connection_counter")
        print(f"connection_counter = {CatanConsumer.connection_counter}")
        print("<<<<<<<<<<<<<<<<<<<<<<<")

    def print_event(self, name, event):
        print(f">>>>>>>>>>>>>>>>>>>>>>> EVENT: {name}")
        print(event)
        print(f"<<<<<<<<<<<<<<<<<<<<<<<")

    async def get_players_data(self, game_id):
        return PLAYERS_DATA

    @database_sync_to_async
    def get_map_data(self, game_id) -> Dict[str, Any]:
        map_data = self.controller.get_map_resource(game_id)
        # self.print_event("map_data", obj_to_json(map_data))
        return map_data

    @database_sync_to_async
    def get_bank_data(self, game_id) -> Dict[str, int]:
        bank_data = self.controller.get_bank_card_set(game_id)
        dev_card_num = sum(value for key, value in bank_data.items() if key.startswith('dev'))
        bank_data = {
            'bank_cards': [
                {'name': 'brick', 'number': bank_data['brick']},
                {'name': 'grain', 'number': bank_data['grain']},
                {'name': 'lumber', 'number': bank_data['lumber']},
                {'name': 'ore', 'number': bank_data['ore']},
                {'name': 'wool', 'number': bank_data['wool']},
                {'name': 'dcs_back', 'number': dev_card_num},
            ],
        }
        self.print_event("bank_data", obj_to_json(bank_data))
        return bank_data

    @database_sync_to_async
    def get_handcard_data(self, game_id, user_id) -> Dict[str, Any]:
        handcard_data = self.controller.get_player_card_set(game_id, user_id)
        handcard_data = [
            [{'name': card_name}] * number
            for card_name, number in handcard_data.items()
        ]
        # flatten list of list
        handcard_data = [card for card_list in handcard_data for card in card_list]
        # NOTE: sort from front end
        self.print_event("handcard_data", obj_to_json(handcard_data))
        return handcard_data

    async def websocket_disconnect(self, event):
        self.print_event("disconnected", event)


    async def websocket_connect(self, event):
        self.print_event("connected", event)

        await self.send(
            {
                "type": "websocket.accept",
            }
        )

        self.game_room = None
        self.controller = CatanBaseController()

    # send to single user
    async def send_to_single_user(self, response):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(response),
            }
        )

    async def websocket_receive(self, event):

        # TODO: Before the state machine, add a lock to protect the states.
        self.print_event("receive", event)

        text = event.get('text', None)
        response = {'action': 'UNKNOWN'}


        if text:
            data = json.loads(text)

            if "game_id" in data:
                game_id = int(data["game_id"])
                self.print_event("game_id", game_id)

            if "user_id" in data:
                user_id = int(data["user_id"])
                self.print_event("user_id", user_id)

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
                elif data['action'] == "REGISTER":
                    # 添加到聊天室
                    self.game_room = f"game_room_{game_id}"
                    await self.channel_layer.group_add(
                        self.game_room,
                        self.channel_name, # channel_name appear only when channel layer is setup
                    )
                    response = {
                        'action': 'COMFIRM_REGISTER',
                        'game_id': game_id,
                    }
                elif data['action'] == "REQUEST_INIT_DATA":
                    players_data = await self.get_players_data(game_id)
                    map_data = await self.get_map_data(game_id)
                    bank_data = await self.get_bank_data(game_id)
                    handcard_data = await self.get_handcard_data(game_id, user_id)
                    response = {
                        'action': 'INIT_GAME',
                        'game_id': game_id,
                        'user_id': user_id,
                        'map_data': map_data,
                        'bank_data': bank_data,
                        'players_data': players_data,
                        # 'game_info': status/state/current_player
                        'handcard_data': handcard_data,
                    }
            elif "message" in data:
                # print(f"message is: {data['message']}")
                response = {
                    "message": f"ECHO: {data['message']}",
                }

        if self.game_room:
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
    def create_game(self, room_id):
        controller = CatanBaseController()
        map_name = get_selected_map(room_id)
        users_config = get_users_config(room_id)
        user_colors = {int(_id): user_config['color'] for _id, user_config in users_config.items()}
        self.print_event("input map_name", map_name)
        self.print_event("input user_colors", obj_to_json(user_colors))
        user_info = controller.initial_game(map_name, user_colors)
        self.print_event("return user info", obj_to_json(user_info))
        return user_info['game_id']

    async def websocket_receive(self, event):
        # TODO: Before the state machine, add a lock to protect the states.
        self.print_event("receive", event)
        text = event.get('text', None)
        if text is None:
            return

        request = json.loads(text)
        response = {'action': 'UNKNOWN'}
        if "action" in request:
            room_id = str(request['room_id'])
            user_id = str(request['user_id'])
            if request['action'] == "ADD_USER":
                update_user(user_id, room_id)
                users = await get_users_in_room(room_id)
                users_info = [
                    {
                        'id': user.id,
                        'first_name': user.first_name,
                    }
                    for user in users
                ]
                self.print_event("users_info", obj_to_json(users_info))
                response = {
                    'action': 'COMFIRM_ADD_USER',
                    'users': users_info,
                    'map_name': get_selected_map(room_id),
                }

                self.print_id(room_id, user_id)

                # 将user加入到room channel中。
                self.room = f"room_{room_id}"
                await self.channel_layer.group_add(
                    self.room,
                    self.channel_name, # channel_name appear only when channel layer is setup
                )
            elif request['action'] == "CHANGE_MAP":
                map_name = request['map_name']
                set_selected_map(room_id, map_name)
                response = {'action': 'COMFIRM_CHANGE_MAP', 'map_name': map_name}
            # TODO: support change color
            elif request['action'] == "CHANGE_COLOR":
                self.print_event("CHANGE_COLOR", "CHANGE_COLOR")
            elif request['action'] == "START_GAME":
                self.print_event("START_GAME", "START_GAME")
                game_id = await self.create_game(room_id)
                response = {'action': 'COMFIRM_START_GAME', 'game_id': game_id}

        # NOTE: print room_data for debug
        room_data = get_room_data()
        self.print_event("room_data", obj_to_json(room_data))

        if self.room:
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
