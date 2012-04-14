
class BehaviorController(object):

    def __init__(self, robot):
        self.robot = robot
        self.layers = []

    def add_layer(self, layer):
        layer.robot = self.robot
        self.layers.append(layer)

    def step(self):
        layer = self.do_all()
        self.robot.drive_speed(layer.left_wheel_speed, layer.right_wheel_speed)
        layer.reset()

    def do_all(self):
        
        for i in range(len(self.layers)-1, -1, -1):
            layer = self.layers[i]
            layer.do()

            if layer.reacted:
                return layer

        # No layers reacted. Do the lowest pri-ed one.
        self.layers[0].do()
        return self.layers[0]


bc = BehaviorController(None)
bc.add_layer("search")
# bc.add_layer("retrieval")
# bc.add_layer("stagnation")
bc.do_all()