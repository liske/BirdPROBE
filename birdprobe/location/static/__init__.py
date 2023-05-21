from birdprobe.location import AbstractProvider

class StaticProvider(AbstractProvider):
    def __init__(self, birdprobe):
        super().__init__(birdprobe)

        self.location = {
            'lat': birdprobe.config.getfloat('static_latitude'),
            'lon': birdprobe.config.getfloat('static_longitute'),
        }

def run(birdprobe):
    provider = StaticProvider(birdprobe)
    provider.run()
