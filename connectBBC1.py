import json
import paho.mqtt.client as mqtt

ADAFRUIT_IO_USERNAME = ""
ADAFRUIT_IO_KEY = ""
# ADAFRUIT_IO_USERNAME = "nguyenngoc"
# ADAFRUIT_IO_KEY = "aio_pxwm06skCqgXBTCHqSB7PwAVf9lP"
# ADAFRUIT_IO_USERNAME = "CSE_BBC1"
# ADAFRUIT_IO_KEY = "aio_GOii70J59sAf8pkCYFQzT9q6SIXk"
client = mqtt.Client()
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
ADAFRUIT_HOST = 'io.adafruit.com'
client.connect(ADAFRUIT_HOST)

def PublishData(data):
    jdata = json.dumps(data)
    client.publish('CSE_BBC1/feeds/bk-iot-relay', jdata)


# if __name__ == '__main__':
#     PublishData()