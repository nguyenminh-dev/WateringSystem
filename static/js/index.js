

$(document).ready(function() {
    var socket = io.connect('https://' + document.domain + ':' + location.port);

    socket.on('mqtt_message', function(data) {
        console.log(data);
        if (data.id === '7') {
            document.getElementById("nhietdo").innerHTML = data['data'] + "&deg;C"
            document.getElementById("doamkk").innerHTML = data['unit']
        }
        else if (data.id === '9') {
            document.getElementById("doamdat").innerHTML = data['data']
        }
        else if (data.id == '11') {
            document.getElementById("switch").checked = data['data']
        }
    });

    $('#switch').on('input', function(event) {
        var ret_data = '0';
        if (document.getElementById("switch").checked)
            ret_data = '1';
        
        socket.emit('change_relay', {data:  ret_data})
    });

});

