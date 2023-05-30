from birdprobe.location import AbstractProvider
import gpsd
from time import sleep

class GpsdProvider(AbstractProvider):
    def __init__(self, birdprobe):
        super().__init__(birdprobe)

        gpsd.connect(
            host=birdprobe.config.get('gpsd_host', '127.0.0.1'),
            port=birdprobe.config.getint('gpsd_port', 2947))

    def run(self):

        while True:
            packet = gpsd.get_current()
            try:
                position = packet.position()
            except gpsd.NoFixError:
                sleep(20)
                continue

            self.location = {
                'lat': position[0],
                'lon': position[1],
            }
            self.publish()

            sleep(60)

def run(birdprobe):
    provider = GpsdProvider(birdprobe)
    provider.run()
