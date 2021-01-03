var CatanRoomWebSocket = {
    createNew: function(vm) {
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
                console.log(`all users: ${user_names}`)
                $("#user_list").text(user_names.join(", "))
                vm.setMap(data.map_name)
            } else if (data.action == "COMFIRM_CHANGE_MAP") {
                vm.setMap(data.map_name)
            } else if (data.action == "COMFIRM_START_GAME") {
                const room_id = $('#rid').text()
                const game_id = data.game_id
                window.location.href = "/catan/?game_id=" + game_id
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
    sendData: function(socket, action, data){
        const uid = $('#uid').text()
        const room_id = $('#rid').text()
        data.user_id = uid
        data.room_id = room_id
        data.action = action
        socket.send(JSON.stringify(data))
    },
    sendUserInfo: function(socket) {
        this.sendData(socket, "ADD_USER", {})
    },
    sendMapName: function(socket, map_name) {
        this.sendData(socket, "CHANGE_MAP", {'map_name': map_name})
    }
}

window.onload = function()
{

};



var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#catan_room',
    data: {
        socket: null,
        maps: [
            {display_name: '标准六边形', name: 'normal', selected: false},
            {display_name: '内海', name: 'inland_sea', selected: true},
            {display_name: '富饶之国', name: 'fertile_land', selected: false},
        ],
    },
    created() {
        var vm = this
        console.log(">>>>>>>>>> Function call")
        console.log("created()")
        console.log("CatanRoomWebSocket.createNew()")
        console.log("==========")
        vm.socket = CatanRoomWebSocket.createNew(this)
    },
    methods: {
        startGame() {
            var vm = this
            console.log(">>>>>>>>>> Function call")
            console.log("startGame()")
            console.log("==========")
            CatanRoomWebSocket.sendData(vm.socket, "START_GAME", {})
        },
        onChangeMap(event) {
            var vm = this
            console.log(event.target.value)
            CatanRoomWebSocket.sendMapName(vm.socket, event.target.value)
        },
        setMap(selected_map_name) {
            var vm = this
            vm.maps.forEach(map => {
                if(map.name == selected_map_name) {
                    map.selected = true
                } else {
                    map.selected = false
                }
            });
        }
    },
})
