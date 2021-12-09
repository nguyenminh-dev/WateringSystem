import json, datetime, time, threading, pytz
import database
from Adafruit_IO import Client

ADAFRUIT_IO_USERNAME = ""
ADAFRUIT_IO_KEY = ""
# ADAFRUIT_IO_USERNAME = "CSE_BBC1"
# ADAFRUIT_IO_KEY = "aio_GOii70J59sAf8pkCYFQzT9q6SIXk"
# ADAFRUIT_IO_USERNAME = "nguyenngoc"
# ADAFRUIT_IO_KEY = "aio_pxwm06skCqgXBTCHqSB7PwAVf9lP"
aio=Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def getDataRelay():
    hcm_time_zone = pytz.timezone("Asia/Ho_Chi_Minh")
    relay_server = aio.receive('bk-iot-relay')
    timestamp_p = datetime.datetime.strptime(relay_server[1], '%Y-%m-%dT%H:%M:%S%z')
    timestamp_p = timestamp_p.astimezone(hcm_time_zone)
    if str(timestamp_p) != database.getLastPump()[1]:
        data = relay_server[3]
        data = data.replace("'", '"')
        data = json.loads(data)
        relay = data['data']
        if relay == '1':
            database.insertPump('ON', timestamp_p)
        else:
            database.insertPump('OFF', timestamp_p)
    else: pass
