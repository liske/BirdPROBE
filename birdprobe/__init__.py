__version__ = '0.0'

import argparse
import configparser
import paho.mqtt.client as mqtt
import socket

class BirdPROBE():
    def __init__(self, component, description, mqtt_persist=False):
        self.component = component
        self.configparser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.configparser['DEFAULT'] = {
            'hostname': socket.gethostname(),
            'fqdn': socket.getfqdn(),
            'component': component,

            'birdnet_input': '',

            'mqtt_host': 'localhost',
            'mqtt_client_id': '${fqdn}_${component}',
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

        self.init(parser, self.configparser)

        self.args = parser.parse_args()
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
        self.mqtt_client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        client.publish(self.config['topic_component'], payload='{"active": true}', retain=True)
        self.mqtt_on_connect(client, userdata, flags, rc)

    def mqtt_on_connect(self, client, userdata, flags, rc):
        pass

    def _on_message(self, client, userdata, message):
        self.mqtt_on_message(client, userdata, message)

    def mqtt_on_message(self, client, userdata, message):
        pass

    def init(self, argparser, configparser):
        pass

    def start(self):
        self.mqtt_client.will_set(self.config['topic_component'], payload='{"active": false}', retain=True)
        self.mqtt_client.connect(self.config['mqtt_host'])
        self.mqtt_client.loop_start()
        self.main()
    
    def main():
        pass
