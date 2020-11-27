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
            }
        }

        socket.onopen = function(e) {
            console.log(">>>>>>>>>> WEB_SOCKET: [open]")
            console.log(e)
            console.log("==========")
            var data = {'message': "TEST SEND MESSAGE"}
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
