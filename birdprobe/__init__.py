__version__ = '0.0'

import argparse
import configparser
import socket

class BirdPROBE():
    def __init__(self, component, description):
        self.component = component
        self.configparser = configparser.ConfigParser()
        self.variables = {
            '{hostname}': socket.gethostname(),
            '{fqdn}': socket.getfqdn(),
            '{component}': component,
        }

        parser = argparse.ArgumentParser(
                        description=description)
        parser.add_argument('--version', action='version',
                            version='%(prog)s {version}'.format(version=__version__))
        parser.add_argument("-c", "--config", type=str,
                            default="/etc/birdprobe/config.ini", help="configuration properties filename")

        self.init(parser)

        self.args = parser.parse_args()
        self.configparser.read(self.args.config)

    def init(self, parser):
        pass

    def config_defaults(self, defaults):
        if not self.component in self.configparser:
            self.configparser[self.component] = defaults
        else:
            for setting, value in defaults.items():
                if not setting in self.configparser[self.component]:
                    self.configparser[self.component] = value

    def config_eval(text, variables={}):
        variables.update(self.variables)

        for pattern, value in variables.items():
            text = text.replace(pattern, value)

        return text

    def main():
        pass
