const token = "6e1a9ed4834ca3e5d27436b9e3df54f4d65114e4";
const ws = new WebSocket(`ws://localhost:8080/chat?token=${token}`);
let app = {
    web_socket: function(){
        let self = this;
        ws.onopen = function () {
            console.log('websocket is connected ...')
            let room_data = {
               'room_id': '435523c9-c5fd-4675-8ffb-4d4bd3bcc68f'
            }
            self._send(room_data)
        }

        ws.onmessage = function (ev) {
            console.log(ev);
        }
    },
    _send: function(data){
        ws.send(JSON.stringify(data))
    },
    on_message: function(){
        $('.msg_send_btn').click(function(){
            let msg = $('.write_msg').val();
            let room_data = {
                'message': msg,
            }
            ws.send(JSON.stringify(room_data))
            $('.write_msg').val('')
        })
    },
    init: function(){
      app.web_socket();
      app.on_message();
    }
}

$('document').ready(function(){
    app.init();
})