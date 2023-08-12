# Complete project details at https://RandomNerdTutorials.com

from time import sleep
from utime import sleep_ms

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
from utils.robust2 import MQTTClient

class MqttConnectionWrapper():
    def __init__(self,
                 config_file: str,
                 user=None,
                 keepalive=0,
                 clean_session=True,
                 ssl=False,
                 ssl_params={}, ):
        print('-' * 60)
        print("Starting MQTT Broker...")
        print("Reading config files...")

        # stores parameters inside class

        with open(config_file, "r") as f:
            self.config 		    = load(f)
            self.wifi_ssid 		    = self.config["wifi_ssid"]
            self.wifi_password 	    = self.config["wifi_password"]
            self.client_id 		    = self.config["client_id"]
            self.client_password    = self.config["client_password"]
            self.mqtt_server 	    = self.config["mqtt_server"]
            self.port 			    = self.config["mqtt_port"]
            self.pub_topics 	    = self.config["publish_topics"]
            self.sub_topics 	    = self.config["subscribe_topics"]

        self.user = user
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
        self.last_will_topic = 'notification'
        self.client.set_last_will(topic = self.last_will_topic,
                                  msg='offline',
                                  qos=1,
                                  retain=True)

        # sets a default callback
        self.client.set_callback(self._callback)
        self.client.DEBUG = True
        self.client.MSG_QUEUE_MAX = 2

        self.last_arrive_topic = None
        self.last_recieved_message = None
        

        print("Mqtt client created!")

        # starts mqtt connection
        # self.mqtt_connect()

    ##############################################
    #           Connection Section
    #############################################

    def mqtt_connect(self) -> None:
        
        if not self.client.connect(clean_session=False):
            print("New session being set up")
            self.subscribe()
            

    def _callback(self, topic, msg):
        self.last_arrive_topic = topic.decode('utf-8')
        self.last_recieved_message = msg.decode('utf-8')

        print('Received message {1} on topic: {0}'.format(topic, msg))


    def take_care_of_business(self):
        
        # At this point in the code you must consider how to handle
        # connection errors.  And how often to resume the connection.
        if self.client.is_conn_issue():
            self.client.disconnect()
            self.client.connect(clean_session=False)
            self.client.ping()
            self.client.publish(self.last_will_topic, 'Connected', retain=True)
            
        else:
            self.client.resubscribe()

        for _ in range(500):
            self.client.check_msg()  # needed when publish(qos=1), ping(), subscribe()
            self.client.send_queue()  # needed when using the caching capabilities for unsent messages
            
            if not self.client.things_to_do():
                break
            sleep_ms(1)
            
        self.client.log()

    ##############################################
    #          Communication Section
    ##############################################

    def log(self, msg, retain = True, qos = 1):
        self.client.publish(self.pub_topics['log'],
                            msg,
                            retain,
                            qos)

    def error(self, msg, retain = True, qos = 1):
        self.client.publish(self.pub_topics['error'],
                            msg,
                            retain,
                            qos)

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
