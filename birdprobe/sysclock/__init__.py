#!/usr/bin/env python3

from birdprobe import BirdPROBE
from datetime import datetime, timedelta, timezone
import gpsd
import time

class SysClock(BirdPROBE):
    def init(self, argparser, configparser):
        configparser[self.component] = {
            'gpsd_host': '127.0.0.1',
            'gpsd_port': 2947,
        }

    def main(self):
        gpsd.connect(
            host=self.config['gpsd_host'],
            port=self.config.getint('gpsd_port'))

        while True:
            packet = gpsd.get_current()
            now = datetime.now(timezone.utc)
            try:
                dt = packet.get_time(local_time=True)

                if abs(dt-now) >= timedelta(seconds=5):
                    time.clock_settime(time.CLOCK_REALTIME, dt.timestamp())
                    print("Set system clock since it has deviated more than 5s from gpsd time.")

                time.sleep(3600)
            except gpsd.NoFixError:
                time.sleep(20)

def main():
    sysclock = SysClock(__package__, 'approximate system time from gpsd')
    sysclock.start()

if __name__ == "__main__":
    main()
