import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json

eventlet.monkey_patch()

app = Flask(__name__, template_folder='./templates')
#app.config['SECRET'] = '872c3a63c69a2c5b9e044da737803d758f14ccb79edc64285aaf40dd0aa996c4'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'io.adafruit.com'
# app.config['MQTT_USERNAME'] = 'mihoangvuong'
# app.config['MQTT_PASSWORD'] = 'aio_MUtm603EUF1gKloK3LaxxYrB4RrA'
#app.config['MQTT_USERNAME'] = 'nguyenminh'
#app.config['MQTT_PASSWORD'] = 'aio_SCDj76SgM1gB7kffAsd8MSP7L3N8'
app.config['MQTT_USERNAME'] = 'nguyenngoc'
app.config['MQTT_PASSWORD'] = 'aio_pxwm06skCqgXBTCHqSB7PwAVf9lP'
# app.config['MQTT_USERNAME'] = 'CSE_BBC'
# app.config['MQTT_PASSWORD'] = 'aio_eIzx84QrfGct3jkJM5aW02aKAIbB'
# app.config['MQTT_USERNAME'] = 'CSE_BBC1'
# app.config['MQTT_PASSWORD'] = 'aio_GOii70J59sAf8pkCYFQzT9q6SIXk'
app.config['MQTT_KEEPALIVE'] = 2

mqtt = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins='*')

# temp variable
topic = [
    'nguyenngoc/feeds/bk-iot-soil',
    'nguyenngoc/feeds/bk-iot-temp-humid',
    'nguyenngoc/feeds/bk-iot-relay'
    #'nguyenminh/feeds/bk-iot-soil',
    #'nguyenminh/feeds/bk-iot-temp-humid',
    #'nguyenminh/feeds/bk-iot-relay'
    # 'mihoangvuong/feeds/bk-iot-soil',
    # 'mihoangvuong/feeds/bk-iot-temp-humid',
    # 'mihoangvuong/feeds/bk-iot-relay',
    # 'CSE_BBC/feeds/bk-iot-soil',
    # 'CSE_BBC/feeds/bk-iot-temp-humid',
    # 'CSE_BBC1/feeds/bk-iot-relay',
]
relay_data = {"id": "11", "name": "RELAY", "data": "", "unit": ""}
save_data = dict(nhietdo=0, doamdat=0, doamkk=0, tuoinuoc=False)


@app.route('/')
def index():
    return render_template(
        'index.html',
        nhietdo=save_data['nhietdo'],
        doamdat=save_data['doamdat'],
        doamkk=save_data['doamkk'],
        tuoinuoc=save_data['tuoinuoc'],
    )


# ---------
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    for t in topic:
        mqtt.subscribe(t)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    print("Receive: " + str(data))
    # save data
    if data['id'] == '7':
        save_data['nhietdo'] = data['data']
        save_data['doamkk'] = data['unit']
    elif data['id'] == '9':
        save_data['doamdat'] = data['data']
    elif data['id'] == '11':
        save_data['tuoinuoc'] = False if data['data'] == '0' else True
        data['data'] = save_data['tuoinuoc']
    # send data to client
    socketio.emit('mqtt_message', data=data, broadcast=True)


# ---------
@socketio.on('change_relay')
def change_relay(message):
    print("switch " + message['data'])
    relay_data['data'] = message['data']
    mqtt.publish(topic[2], str(relay_data).replace("'", '"'))


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
