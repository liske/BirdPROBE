from birdprobe.location import AbstractProvider

class NoneProvider(AbstractProvider):
    pass

def run(birdprobe):
    provider = NoneProvider(birdprobe)
    provider.run()
