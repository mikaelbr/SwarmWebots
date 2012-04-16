

from controller import *


class IR_Emitters(Robot):

    num_emitters = 12

    def basic_setup(self):
        self.timestep = int(self.getBasicTimeStep())  # Fetched from WorldInfo.basicTimeStep (in the Webots world)
        # self.emitter = self.getEmitter("emitter")
        # self.emitter.setChannel(1)

    def broadcast(self):

        while self.step(64) != -1:
            pass
            # print "Emitter", self.emitter
            # print "Channel", self.emitter.getChannel()

            # print "Did send", self.emitter.send("FOOD MOTHERFUCKS 2000")

ir = IR_Emitters()
ir.basic_setup()
ir.broadcast()
