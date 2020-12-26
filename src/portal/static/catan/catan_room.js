var CatanRoomWebSocket = {
    createNew: function(
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

            if (data.action == "COMFIRM_ADD_USER") {
                var user_names = []
                data.users.forEach(user => {
                    user_names.push(user.first_name)
                })
                console.log(user_names)
                $("#user_list").text(user_names.join(", "))
            }
        }

        socket.onopen = function(e) {
            console.log(">>>>>>>>>> WEB_SOCKET: [open]")
            console.log(e)
            console.log("==========")
            CatanRoomWebSocket.sendUserInfo(socket)
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
    },

    sendUserInfo: function(socket) {
        const uid = $('#uid').text()
        const room_id = $('#rid').text()
        console.log(`uid = ${uid}`)
        console.log(`room_id = ${room_id}`)
        var data = {'action': "ADD_USER", 'user_id': uid, 'room_id': room_id}
        socket.send(JSON.stringify(data))
    }
}

window.onload = function()
{
    socket = CatanRoomWebSocket.createNew()
};
