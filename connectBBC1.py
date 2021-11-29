import json
import paho.mqtt.client as mqtt

ADAFRUIT_IO_USERNAME = "nguyenminh"
ADAFRUIT_IO_KEY = "aio_SCDj76SgM1gB7kffAsd8MSP7L3N8"
client = mqtt.Client()
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
ADAFRUIT_HOST = 'io.adafruit.com'
client.connect(ADAFRUIT_HOST)

def PublishData(data):
    jdata = json.dumps(data)
    client.publish('nguyenminh/feeds/bk-iot-relay', jdata)


# if __name__ == '__main__':
#     PublishData()