## This uses the EpuckBasic code as the interface to webots, and the epuck2 code to connect an ANN
# to webots.

import epuck_basic as epb
from imagepro import *
#from ann.ann import Ann
#from ann.parser import AnnParser

# The webann is a descendent of the webot "controller" class, and it has the ANN as an attribute.


class Webswarm(epb.EpuckBasic):

    def __init__(self, tempo=1.0):
        epb.EpuckBasic.__init__(self)

        self.basic_setup()  # defined for EpuckBasic
        self.tempo = tempo

    def drive_speed(self, left=0, right=0):
        """
            Drive with speed X and Y for left wheel (X) and right wheel (Y)
        """
        ms = self.tempo * 1000
        self.setSpeed(int(left * ms), int(right * ms))

    def run(self):

        while True:  # main loop

            print self.get_proximities()

            self.spin_angle(-.1)
            self.wait(0.3)

            if self.step(self.timestep) == -1:
                break


ws = Webswarm()
ws.run()
