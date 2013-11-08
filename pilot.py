import libardrone
import constants
import time
class Pilot():

    def __init__(self):
        """

        """
        self.drone = libardrone.ARDrone()

    def fly_to_station(self, station_number):
        """

        """

        # Suppose we are at the base station and our queue is empty
        #TODO: Add a queue
        self._init_ardrone_()

        self._takeoff()

        target_angle, target_time_distance = self._get_location_for_station(station_number)

        self._change_heading(target_angle)

        self._fly_straight(target_time_distance)

        self._fix_on_qr()

        self._change_altitude(constants.PICTURE_ALTITUDE)

        self._take_photo()

        self._change_altitude(constants.FLYING_ALTITUDE)

        self._change_heading(self._fix_angle(target_angle - 360))

        self._fly_straight(target_time_distance) # Back to base

        self._change_heading(constants.BASE_HEADING)

        self._land()

    def _change_heading(self, to_angle):
        """
            Changes the plan's heading to a specified angle
        """
        current_angle = self._get_compass_angle()

        angle_diff = abs(current_angle - to_angle)

        # Start turning left
        self.drone.turn_left()

        while(angle_diff > constants.ANGLE_MAX_DEVIATION):
            current_angle = self._get_compass_angle()
            angle_diff = abs(current_angle - to_angle)
            time.sleep(constants.SAMPLE_ANGLE_CHANGE_TIME)

        # TODO: Stop also after X number of loops, turn right/left as needed instead of just left
        # Stop turning
        self.drone.hover()

    def _fly_straight(self, seconds_to_fly):
        """
            Flies at a straight line for X seconds.
        """
        self.drone.move_forward()
        time.sleep(seconds_to_fly)
        self.drone.hover()

    def _change_altitude(self, target_altitude):
        """
            Lowers the plane's altitude to a specified level
        """
        # Frame with tag-id 0 is the one with the position data
        current_altitude = self.drone.navdata[0]["altitude"]
        current_deviation = abs(target_altitude - current_altitude)

        if (current_deviation > constants.ALTITUDE_MAX_DEVIATION):
            if (target_altitude - current_altitude > 0):
                # We need to go up
                self.drone.move_up()
            else:
                # We need to go down
                self.drone.move_down()

            while (current_deviation > constants.ALTITUDE_MAX_DEVIATION):
                time.sleep(0.2)
                current_altitude = self.drone.navdata[0]["altitude"]
                current_deviation = abs(target_altitude - current_altitude)

        self.drone.hover()

    def _get_location_for_station(self, station_name):
        """
            Gets the location for the
        """
        station = [x for x in constants.STATIONS if x["station_name"] == station_name][0]
        target_angle = station["angle_from_base"]
        target_time_distance = station[constants.FLYING_SPEED / "distance_from_base"]

        return target_angle, target_time_distance

    def _takeoff(self):
        """
            Takes off the plane.
        """
        self.drone.takeoff(constants.FLYING_ALTITUDE)



