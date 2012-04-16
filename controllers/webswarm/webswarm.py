## This uses the EpuckBasic code as the interface to webots, and the epuck2 code to connect an ANN
# to webots.

import epuck_basic as epb
#from imagepro import *
#from ann.ann import Ann
#from ann.parser import AnnParser

# The webann is a descendent of the webot "controller" class, and it has the ANN as an attribute.


class Webswarm(epb.EpuckBasic):

    def __init__(self, tempo=1.0):
        epb.EpuckBasic.__init__(self)

        self.basic_setup()  # defined for EpuckBasic
        self.tempo = tempo
        self.receiver = self.getReceiver('receiver')
        self.timestep = 64
        self.receiver.enable(self.timestep)

    def drive_speed(self, left=0, right=0):
        """
            Drive with speed X and Y for left wheel (X) and right wheel (Y)
        """
        ms = self.tempo * 1000
        self.setSpeed(int(left * ms), int(right * ms))

    def read_receiver(self):
        print "Queue Length: ", self.receiver.getQueueLength()
        # print "Emitter dir", self.receiver.getEmitterDirection()
        print "Channel", self.receiver.getChannel()
        print "Signal Strength", self.receiver.getSignalStrength()

        while self.receiver.getQueueLength() > 0:
            print "Heeer"
            message = self.receiver.getData()
            self.receiver.nextPacket()

            print message

            if message == "FOOD":
                print "Found some food up in hea'"

    def run(self):

        while True:  # main loop

            # self.read_receiver()

            # print self.get_proximities()

            # self.spin_angle(-.1)
            # self.wait(0.3)
            print "Her"

            if self.step(self.timestep) == -1:
                break


ws = Webswarm()
ws.run()


"""

public myFoodController() {
    super();
    
    emitter = getEmitter("emitter");
  }
  public void run() {
    do {
      
      emitter.send(message);
    } while (step(64) != -1);
  }
epuck:
epuck controller:
 while(receiver.getQueueLength()>0){
        byte[] message = receiver.getData();
        //System.out.println("Found message of length "+message.length);
        if(message[0]==FOOD){
          //System.out.println("Close to food!");
          foundFood = true;
        }
        receiver.nextPacket();
      }

"""