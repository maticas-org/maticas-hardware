from time import sleep, ticks_ms, time
from machine import deepsleep


class MQTTModuleScheduler():

    def __init__(self, mqtt_conn, module):

        self.mqtt_conn  = mqtt_conn
        self.module     = module
        self.pub_topics = self.module.pub_topics

    def send_messages(self):

        for alias in self.pub_topics.keys():

            # gets the measurement

            if self.pub_topics[alias]["exec"] == "":
                print("topic \"{}\" has no candidate for answering a call".format(alias))
                self.mqtt_conn.publish(topic = self.pub_topics[alias]["topic"],
                                       msg = "ERROR: no {} sensor".format(alias))
                continue

            value = str(self.pub_topics[alias]["exec"]())

            # sends the measurement
            self.mqtt_conn.publish(topic = self.pub_topics[alias]["topic"], msg = value)
            sleep(0.1)
            print("message sent on topic {}".format(self.pub_topics[alias]["topic"]))

    def deep_sleep(self, secs = 90):

        """
            Sets the module on deep sleep.
        """
        print("going to sleep for {} seconds".format(secs))
        deepsleep(secs * 1000)


    def wake_up(self):
        """
            Wakes the module up, and connects back to wifi and mqtt broker.
        """
        pass


    def loop(self):


        print("starting loop...")
        time_init = time()

        while True:

            self.send_messages()
            sleep(0.1)
            time_now = time()

            print("time elapsed sending messages: {}".format(time_now - time_init))
            self.deep_sleep()
            self.wake_up()


