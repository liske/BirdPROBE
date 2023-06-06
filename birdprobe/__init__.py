__version__ = '0.0'

import argparse
import configparser
import logging
import os
import paho.mqtt.client as mqtt
import socket

logger = logging.getLogger(__name__)

class BirdPROBE():
    def __init__(self, component, description, mqtt_persist=False):
        self.component = component
        self.configparser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.configparser['DEFAULT'] = {
            'hostname': socket.gethostname(),
            'fqdn': socket.getfqdn(),
            'component': component,
            'pid': os.getpid(),

            'birdnet_input': '',

            'mqtt_host': 'localhost',
            'mqtt_client_id': '${fqdn}_${component}#${pid}',
            'mqtt_transport': 'tcp',

            'topic_prefix': 'BirdPROBE',
            'topic_component': '${topic_prefix}/component/${hostname}/${component}',
            'topic_detection': '${topic_prefix}/detection/${hostname}/${birdnet_label}',
            'topic_location': '${topic_prefix}/location/${hostname}',

        }

        parser = argparse.ArgumentParser(
                        description=description)
        parser.add_argument('--version', action='version',
                            version='%(prog)s {version}'.format(version=__version__))
        parser.add_argument("-c", "--config", type=str,
                            default="/etc/birdprobe/config.ini", help="configuration properties filename")
        parser.add_argument("-d", "--debug", action='store_true', help="set logging level to DEBUG")

        self.init(parser, self.configparser)

        self.args = parser.parse_args()

        if self.args.debug:
            logging.basicConfig(format='%(name)s %(levelname)s %(message)s', level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(name)s %(levelname)s %(message)s', level=logging.INFO)

        logger.debug('using config file %s', self.args.config)

        self.configparser.read(self.args.config)
        if not self.configparser.has_section(component):
            self.configparser.add_section(component)
        self.config = self.configparser[component]

        self.mqtt_persist = mqtt_persist
        self.mqtt_client = mqtt.Client(
            client_id=self.config['mqtt_client_id'],
#            clean_session=True,
#            userdata=None,
            protocol=mqtt.MQTTv311,
            transport=self.config['mqtt_transport'])

        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("MQTT connection has been established")
        client.publish(self.config['topic_component'], payload='{"active": true}', retain=True)
        self.mqtt_on_connect(client, userdata, flags, rc)

    def mqtt_on_connect(self, client, userdata, flags, rc):
        pass

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning("MQTT unexpected disconnection: %s", mqtt.error_string(rc))
        self.mqtt_on_disconnect(client, userdata, rc)

    def mqtt_on_disconnect(self, client, userdata, message):
        pass

    def _on_message(self, client, userdata, message):
        logger.debug("MQTT message on %s", message.topic)
        self.mqtt_on_message(client, userdata, message)

    def mqtt_on_message(self, client, userdata, message):
        pass

    def init(self, argparser, configparser):
        pass

    def start(self):
        self.mqtt_client.enable_logger()
        self.mqtt_client.will_set(self.config['topic_component'], payload='{"active": false}', retain=True)
        self.mqtt_client.connect(self.config['mqtt_host'])
        self.mqtt_client.loop_start()
        self.main()
    
    def main():
        pass
