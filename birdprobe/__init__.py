__version__ = '0.0'

import argparse
import configparser
import sys

def birdprobe_argparser(component, description):
    parser = argparse.ArgumentParser(
                    description=description)

    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument("-c", "--config", type=str,
                        default="/etc/birdprobe/config.ini", help="configuration properties filename")

    return parser

def birdprobe_load_config(config_filename, component):
    config = configparser.ConfigParser()
    config.read(config_filename)

    if component in config:
        return config[component]
    else:
        return {}
