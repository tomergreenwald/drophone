# Copyright (c) 2011 Bastian Venthur
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""
This module provides access to the data provided by the AR.Drone.
"""

import select
import socket
import threading

import libardrone
import arvideo


import arvideo2

class VideoReadingThread(threading.Thread):

    def __init__(self, drone):
        threading.Thread.__init__(self)
        self.drone = drone
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.video_socket.connect(('192.168.1.1', libardrone.ARDRONE_VIDEO_PORT))
        video2 = arvideo2.ARVideo2(self.drone)
        while 1:
            try:
                data = self.video_socket.recv(55000)
                #print len(data)

                video2.write(data)
            except Exception:
                import traceback
                traceback.print_exc()



class NavReadingThread(threading.Thread):
    """ARDrone Network Process.

    This process collects data from the video and navdata port, converts the
    data and sends it to the IPCThread.
    """

    def __init__(self, drone):
        threading.Thread.__init__(self)
        self.drone = drone

    def run(self):
        nav_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        nav_socket.setblocking(0)
        nav_socket.bind(('', libardrone.ARDRONE_NAVDATA_PORT))
        nav_socket.sendto("\x01\x00\x00\x00", ('192.168.1.1', libardrone.ARDRONE_NAVDATA_PORT))

        stopping = False
        while not stopping:
            inputready, outputready, exceptready = select.select([nav_socket], [], [])
            for i in inputready:
                while 1:
                    try:
                        data = nav_socket.recv(65535)
                    except IOError:
                        # we consumed every packet from the socket and
                        # continue with the last one
                        break
                navdata = libardrone.decode_navdata(data)
                self.drone.navdata = navdata

        nav_socket.close()
