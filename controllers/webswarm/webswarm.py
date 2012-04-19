
from controller import *
from asb.behavior_controller import *
from asb.behavior_module import *
from asb.search import *
from asb.retrieval import *
from asb.stagnation import *


class Webswarm(DifferentialWheels):

    # max_wheel_speed = 1051

    num_dist_sensors = 8
    num_leds = 8
    num_light_sensors = 8

    encoder_resolution = 159.23  # for wheel encoders
    wheel_diameter = 4.1  # centimeters
    axle_length = 5.3  # centimeters

    tempo = 1.0

    dist_value = [0] * 8

    def __init__(self, bc=None):
        super(Webswarm, self).__init__()

        if bc:
            self.bc = bc
            self.bc.robot = self

        self.basic_setup()

    def basic_setup(self):
        self.timestep = 64

        # IR Receiver setup
        # self.receiver = self.getReceiver('receiver')
        # self.receiver.enable(self.timestep)

        self.distance_threshold = [100, 200, 200, 100]

        # Activate encoders for the weels
        self.enableEncoders(self.timestep)

        self._activate_distance()
        self._activate_leds()
        self._activate_IR()

    def _activate_distance(self):
        """
            Distance sensor setup.
        """
        self.dist_sensors = [self.getDistanceSensor('ps' + str(x)) for x in range(self.num_dist_sensors)]  # distance sensors
        map((lambda s: s.enable(self.timestep)), self.dist_sensors)  # Enable all distance sensors

    def _activate_leds(self):
        """
            Activate and retrieve the LEDs.
        """
        self.leds = [self.getLED('led' + str(i)) for i in range(self.num_leds)]
        self.green_led = self.getLED('led8')
        self.front_led = self.getLED('led9')
        self.front_led.set(1)

    def _activate_IR(self):
        """
            Activate the IR sensors (light sensor)
        """
        self.IR_threshold = 2000

        self.IR_sensors = [self.getLightSensor('ls' + str(i)) for i in range(self.num_light_sensors)]
        map((lambda s: s.enable(self.timestep)), self.IR_sensors)  # Enable all distance sensors

    def get_proximities(self):
        self.dist_value = [x.getValue() for x in self.dist_sensors]
        return self.dist_value

    def get_IR(self):
        return [x.getValue() for x in self.IR_sensors]

    def update_LED(self, LED):
        for i in range(self.num_leds):
            self.leds[i].set(int(LED[i]))

    def update_green_LED(self, val):
        self.green_led.set(int(val))

    def run(self):

        while self.step(self.timestep) != -1:  # main loop
            self.bc.step()

bc = BehaviorController()
ws = Webswarm(bc)

search = Search()
retrieval = Retrieval()
bc.add_layer(search)
bc.add_layer(retrieval)

stagnation = Stagnation()
stagnation.search_layer = search
stagnation.retrieval_layer = retrieval
bc.add_layer(stagnation)


ws.run()
