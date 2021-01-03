var CatanWebSocket = {
    createNew: function(
        game
    ) {
        var loc = window.location
        var wsStart = 'ws://'
        if (loc.protocol == 'https:') {
            wsStart = 'wss://'
        }
        var endpoint = wsStart + loc.host + loc.pathname
        // var socket = new WebSocket(endpoint)
        var socket = new ReconnectingWebSocket(endpoint)

        socket.onmessage = function(e) {
            var data = JSON.parse(e.data)
            console.log(">>>>>>>>>> WEB_SOCKET: [message]")
            console.log(e)
            // console.log(data)
            console.log("==========")
            const user_id = $('#uid').text()

            if (data.action == "COMFIRM_BUILD_HOUSE") {
                game.build_house_action({x: data.x, y: data.y, z: data.z})
            } else if (data.action == "COMFIRM_BUILD_TOWN") {
                game.build_town_action({x: data.x, y: data.y, z: data.z})
            } else if (data.action == "COMFIRM_BUILD_ROAD") {
                game.build_road_action({x: data.x, y: data.y, z: data.z})
            } else if (data.action == "COMFIRM_MOVE_ROBBER") {
                game.move_robber_action({x: data.x, y: data.y});
            } else if (data.action == "COMFIRM_ROLL_DICE") {
                game.roll_dice_action(data.num1, data.num2)
            } else if (data.action == "INIT_GAME" && game.is_initialized == false) {
                if (user_id == data.user_id.toString()) {
                    game.id = data.game_id
                    map_data = data.map_data
                    bank_data = data.bank_data

                    // load data
                    load_map_data_to_game(map_data.map_name, map_data.tiles, game)
                    load_bank_data_to_game(bank_data, game)
                    game.board.cards = data.handcard_data
                    game.board.cards.sort(game.card_compare);

                    // render UI
                    game.load_map()
                    game.load_cards()
                    game.load_main_button()

                    game.init_player_action(data.players_data)
                    game.init_info_action()
                    game.init_player_select_panel_action()

                    game.is_initialized = true
                } else {
                    // other user log into the game
                }
            } else if (data.action == "COMFIRM_REGISTER" && game.is_initialized == false) {
                const game_id = $('#gid').text()
                const user_id = $('#uid').text()
                var data = {
                    'action': 'REQUEST_INIT_DATA',
                    'game_id':  game_id,
                    'user_id': user_id,
                };
                socket.send(JSON.stringify(data))
            }
        }

        socket.onopen = function(e) {
            console.log(">>>>>>>>>> WEB_SOCKET: [open]")
            console.log(e)
            console.log("==========")
            var data = {'message': "TEST SEND MESSAGE"}
            socket.send(JSON.stringify(data))
            const game_id = $('#gid').text()
            const user_id = $('#uid').text()
            var data = {
                'action': 'REGISTER',
                'game_id':  game_id,
                'user_id': user_id,
            };
            socket.send(JSON.stringify(data))
        }

        socket.onerror = function(e) {
            console.log(">>>>>>>>>> WEB_SOCKET: [error]")
            console.log(e)
            console.log("==========")
        }

        socket.onclose = function(e) {
            console.log(">>>>>>>>>> WEB_SOCKET: [close]")
            console.log(e)
            console.log("==========")
        }

        return socket
    }
}
