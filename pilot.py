import libardrone
import constants
import time
class Pilot():

    def __init__(self):
        """

        """
        self.drone = libardrone.ARDrone()

    def print_navdata(self):
        print "Navdata is: " + str(self.drone.navdata)

    def test_4(self):
        self.print_navdata()
        self._takeoff()
        time.sleep(6)
        print "Took off"
        self.print_navdata()
        self._change_altitude(1500)
        time.sleep(5)
        print "Finished turning"
        raw_input()
        self.drone.land();
        time.sleep(2)
        self.print_navdata()
        self.drone.halt()

    def test_3(self):
        self._takeoff()
        time.sleep(6)
        #old_speed = self.drone.speed
        #self.drone.set_speed(old_speed*2/3)
        print "Took off"
        self.print_navdata()
        print "Turning"
        #self._change_heading(300)
        print "Finished turning"
        self.print_navdata()
        raw_input()
        self._fly_straight(2)
        time.sleep(5)
        print "Finished turning"
        raw_input()
        self.drone.land();
        time.sleep(2)
        self.print_navdata()
        self.drone.halt()

    def test_2(self):
        self._takeoff()
        time.sleep(6)
        old_speed = self.drone.speed
        self.drone.set_speed(old_speed*4)
        print "Took off"
        self.print_navdata()
        print "Turning"
        self._change_heading(180)
        print "Finished turning"
        self.print_navdata()
        time.sleep(5)
        print "Finished turning"
        raw_input()
        self.drone.land();
        time.sleep(2)
        self.print_navdata()
        self.drone.halt()

    def test_1(self):
        """
            Initialize drone.
            Take off.
            Reach desired altitude.
            Rotate 90 degress.
            Land.
            Shutdown.

            Measure with wireshark packets after takeoff.
            Measure with wireshark what the drone thinks it location is.
            Measure with a compass.
        """
        time.sleep(0.5)

        self._takeoff()
        time.sleep(6)
        print "Took off"
        self.print_navdata()

        print "Turning"
        ##changes the heading to the correct one
        old_speed = self.drone.speed
        self.drone.set_speed(old_speed*4)
        #for i in xrange(40):
        self.drone.turn_left()
        #    time.sleep(0.05)
        #time.sleep(5)
        #for i in xrange(40):
        #    self.drone.turn_right()
        #    time.sleep(0.05)

        initial_angle = int(self.drone.navdata[0]['psi'])
        print "rotating"
        for i in xrange(3):
            self.print_navdata()
            time.sleep(0.3)
        print "halting"
        self.drone.hover()
        time.sleep(0.5)
        print "landing data"
        self.print_navdata()
        final_angle = int(self.drone.navdata[0]['psi'])
        print "rotated", abs(initial_angle-final_angle)

        raw_input()
        self.drone.land();

        time.sleep(2)
        self.print_navdata()
        self.drone.halt()

    def fly_to_station(self, station_number):
        """

        """

        # Suppose we are at the base station and our queue is empty
        #TODO: Add a queue

        #takes of and reachs the desired altitude
        self._takeoff()

        target_angle, target_time_to_fly = self._get_location_for_station(station_number)

        #changes the heading to the correct one
        self._change_heading(target_angle)

        self._fly_straight(target_time_to_fly)

        #._fix_on_qr()

        self._change_altitude(constants.PICTURE_ALTITUDE)

        self._take_photo()

        self._change_altitude(constants.FLYING_ALTITUDE)

        self._change_heading(self._fix_angle(target_angle - 180))

        self._fly_straight(target_time_to_fly) # Back to base

        self._change_heading(constants.BASE_HEADING)

        self._land()

    def _get_compass_angle(self):
        return (int(self.drone.navdata[0]['psi']))%360

    def _change_heading(self, to_angle):
        """
            Changes the plan's heading to a specified angle
        """
        current_angle = self._get_compass_angle()

        angle_diff = abs(current_angle - to_angle)

        # Start turning left
        if current_angle - to_angle > 0:
            self.drone.turn_left()
        else:
            self.drone.turn_right()

        while(angle_diff > constants.ANGLE_MAX_DEVIATION):
            self.print_navdata()
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

            while (current_deviation > constants.ALTITUDE_MAX_DEVIATION and current_altitude < target_altitude*1.05):
                self.print_navdata()
                time.sleep(0.05)
                current_altitude = self.drone.navdata[0]["altitude"]
                current_deviation = abs(target_altitude - current_altitude)

        self.drone.hover()

    def _get_location_for_station(self, station_name):
        """
            Gets the location for the
        """
        station = constants.STATIONS[station_name]
        target_angle = station["angle"]
        distance = station["distance"]
        time_to_fly = distance / constants.FLYING_SPEED_IN_MPS

        return target_angle, time_to_fly

    #self._take_photo()

    def _takeoff(self):
        """
            Takes off the plane.
        """
        self.drone.takeoff(constants.FLYING_ALTITUDE)
        time.sleep(6)
if __name__ == '__main__':
    p = Pilot()
    try:
        p.test_4()
    except Exception, e:
        print e
        p.drone.land()
        p.drone.halt()


