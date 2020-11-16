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
            console.log("WebSocket: message", e)
            var data = JSON.parse(e.data)
            console.log(data)
            if (data.action == "COMFIRM_BUILD_HOUSE") {
                game.build_house_action(data)
            } else if (data.action == "COMFIRM_BUILD_TOWN") {
                game.build_town_action(data)
            } else if (data.action == "COMFIRM_BUILD_ROAD") {
                game.build_road_action(data)
            }
        }

        socket.onopen = function(e) {
            console.log("WebSocket: open", e)
            var data = {'message': "who are you?"}
            socket.send(JSON.stringify(data))
        }

        socket.onerror = function(e) {
            console.log("WebSocket: error", e)
        }

        socket.onclose = function(e) {
            console.log("WebSocket: close", e)
        }

        return socket
    }
}
