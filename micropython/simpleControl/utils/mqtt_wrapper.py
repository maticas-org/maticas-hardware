# Complete project details at https://RandomNerdTutorials.com

import time
import ubinascii
import machine
import micropython
import network
import esp

esp.osdebug(None)
import gc

gc.collect()

from json import load
from utils.internet_connection import *
from utils.umqttsimple import MQTTClient


class MqttConnectionWrapper():
    def __init__(self,
                 config_file: str,
                 client_password=None,
                 user=None,
                 keepalive=30,
                 clean_session=True,
                 ssl=False,
                 ssl_params={}, ):
        print('-' * 60)
        print("Starting MQTT Broker...")
        print("Reading config files...")

        # stores parameters inside class

        with open('config.json', "r") as f:
            self.config = load(f)
            self.wifi_ssid = self.config["wifi_ssid"]
            self.wifi_password = self.config["wifi_password"]
            self.client_id = self.config["client_id"]
            self.mqtt_server = self.config["mqtt_server"]
            self.port = self.config["mqtt_port"]
            self.pub_topics = self.config["publish_topics"]
            self.sub_topics = self.config["subscribe_topics"]

        self.user = user
        self.client_password = client_password
        self.keepalive = keepalive
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.clean_session = clean_session

        # creates the mqtt client
        self.client = MQTTClient(self.client_id,
                                 self.mqtt_server,
                                 self.port,
                                 self.user,
                                 self.client_password,
                                 self.keepalive,
                                 self.ssl,
                                 self.ssl_params)

        # configures the mqtt client

        # last will message, if the client disconnects this message will be published
        # just before that
        self.client.set_last_will(topic='notification',
                                  msg='offline',
                                  qos=1,
                                  retain=True)

        # sets a default callback
        self.client.set_callback(self._callback)

        self.last_arrive_topic = None
        self.last_recieved_message = None

        print("Mqtt client created!")

        # starts mqtt connection
        # self.mqtt_connect()

    ##############################################
    #           Connection Section
    #############################################

    def mqtt_connect(self) -> None:
        self.client.connect(clean_session=self.clean_session)
        print('Successfull connection to MQTT broker!')

        # once it's connected
        # subscribes to all topics in the sub_topics dictionary
        self.subscribe()

    def _callback(self, topic, msg):
        self.last_arrive_topic = topic.decode('utf-8')
        self.last_recieved_message = msg.decode('utf-8')

        print('Received message {1} on topic: {0}'.format(topic, msg))

    def restart_and_reconnect(self):
        print('Failed to connect to MQTT broker. Reconnecting...')
        time.sleep(10)
        machine.reset()

    ##############################################
    #          Communication Section
    ##############################################

    def publish(self, topic, msg, retain=False, qos=1):
        self.client.publish(topic, msg, retain, qos)

    def subscribe(self):
        # subscribes to all topics in the sub_topics dictionary
        # getting also the specified qos
        for alias in self.sub_topics.keys():
            print("Subscribed to topic: {0} with qos = {1}".format(self.sub_topics[alias]["topic"],
                                                                   self.sub_topics[alias]["qos"]))
            self.client.subscribe(topic=self.sub_topics[alias]["topic"],
                                  qos=self.sub_topics[alias]["qos"])

    def set_last_will(self, topic, msg, retain=False, qos=1):
        self.client.set_last_will(topic, msg, retain, qos)

    def set_callback(self, callback):
        self.client.set_callback(callback)
        print("Callback updated.")