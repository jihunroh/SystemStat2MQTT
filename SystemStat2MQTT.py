import paho.mqtt.client as mqtt
import psutil
from shutil import disk_usage
from socket import gethostname
from json import dumps as json_dumps

MQTT_SERVER = 'localhost'
MQTT_TOPIC_PREFIX = 'custom_things/' + gethostname() + '/'

class Status:
    def __init__(self):
        return
    def cpu(self):
        return {
            'percent': psutil.cpu_percent()
        }
    def memory(self):
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'used': memory.used,
            'percent': memory.percent
        }
    def disk(self):
        disk = disk_usage('/')
        return {
            'total': disk.total,
            'used:': disk.used,
            'percent': 100 * round(disk.used / disk.total, 1)
        }

status = Status()

client = mqtt.Client()
client.connect(MQTT_SERVER, 1883)
client.publish(MQTT_TOPIC_PREFIX + 'cpu', json_dumps(status.cpu()), qos=0, retain=True)
client.publish(MQTT_TOPIC_PREFIX + 'memory', json_dumps(status.memory()), qos=0, retain=True)
client.publish(MQTT_TOPIC_PREFIX + 'disk', json_dumps(status.disk()), qos=0, retain=True)
client.disconnect()
exit(0)
