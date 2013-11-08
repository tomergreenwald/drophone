import rpyc
import pilot

class FlyService(rpyc.Service):
    def __init__(self):
        self.pilot = pilot.Pilot()

    def exposed_fly_to_station(self, station_num):
        self.pilot.fly_to_station(station_num)