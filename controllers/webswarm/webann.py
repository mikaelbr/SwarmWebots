## This uses the EpuckBasic code as the interface to webots, and the epuck2 code to connect an ANN
# to webots.

import epuck_basic as epb
from imagepro import *
#from ann.ann import Ann
#from ann.parser import AnnParser

# The webann is a descendent of the webot "controller" class, and it has the ANN as an attribute.
class WebAnn(epb.EpuckBasic):

    def __init__(self, ann, tempo = 1.0):
        epb.EpuckBasic.__init__(self)

        self.basic_setup() # defined for EpuckBasic 

        self.ann = ann
        self.ann.init_nodes()
        self.ann.set_testing_mode()

        self.tempo = tempo

    def drive_speed(self, left=0, right=0):
        """
            Drive with speed X and Y for left wheel (X) and right wheel (Y)
        """
        ms = self.tempo * 1000
        self.setSpeed(int(left * ms), int(right * ms))

    def run(self):

        while True: # main loop
            dist = [max(-1, (1 - (i / 600))) for i in self.get_proximities()]
            cam = process_snapshot(self.snapshot(),color="green")
            inputs = dist + cam

            # print "Distance"
            # print dist

            # print "Camera"
            # print cam

            wheels = self.ann.recall(inputs)
            
            # print "Drive Speed:"
            # print wheels

            self.drive_speed(*wheels)

            if self.step(self.timestep) == -1: break

class BackProp(WebAnn):
    """
        Off-line training of robot with back propagation.
        Reading from a file with targets.
    """

    def __init__(self, ann, tempo = 1.0, training_file = 'data/learning.txt', epochs=5000):

        super(BackProp, self).__init__(ann, tempo)

        self.ann.set_learning_mode()
        self.get_data(training_file)
        self.do_prop(epochs)
        self.ann.set_testing_mode()

    def get_data(self, training_file):
        self.data = []

        with open(training_file, 'r') as f:
            for line in f.readlines():
                self.data.append(eval(line))


    def do_prop(self, epochs=1):        
        print "Training robot using back propagation"

        for i in range(epochs):
            inputs, target = self.data[i % len(self.data)]
            # Do prop
            self.ann.backprop(inputs, target)

        print "Done using back propagation\nRun robot! Run!"


#ann = AnnParser("ann/scripts/ann.ini").create_ann()

# controller = WebAnn(ann)
#controller = BackProp(ann)

for i in ann.output_nodes:
    for j in i.incomming:
        print j.current_weight
controller.run()
