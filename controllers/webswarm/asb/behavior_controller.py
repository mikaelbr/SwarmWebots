"""
    Controller for behavior layers with the subsumtion layer.
    The first layers added with add_layer() are the layers that
    are the least prioritised.
"""


class BehaviorController(object):

    def __init__(self, robot=None):
        self.robot = robot
        self.layers = []

    def add_layer(self, layer):
        """
            Adds a layer to the stack.
            Automaticly adds the robot to the layer.
            Lowest priority should be added first.
        """
        layer.robot = self.robot
        self.layers.append(layer)

    def step(self):
        """
            Run one time step of the robots movements
        """
        layer = self.do_all()
        print "Mode: %s" % layer.__class__.__name__
        self.robot.setSpeed(layer.left_wheel_speed, layer.right_wheel_speed)
        layer.reset()

    def do_all(self):
        """
            Execute all layers in proper (descending) order.
        """
        for i in range(len(self.layers) - 1, 0, -1):
            layer = self.layers[i]
            layer.do()

            if layer.reacted:
                return layer

        # No layers reacted. Do the lowest pri-ed one.
        self.layers[0].do()
        return self.layers[0]
