
class BehaviorModule(object):

    def __init__(self):
        self.reacted = False
        self.robot = None
        self._left_wheel_speed = 0
        self._right_wheel_speed = 0

    def reset(self):
        self._left_wheel_speed = 0
        self._right_wheel_speed = 0

    @property
    def left_wheel_speed(self):
        return self._left_wheel_speed

    @left_wheel_speed.setter
    def left_wheel_speed(self, value):
        self.reacted = True
        self._left_wheel_speed = value

    @property
    def right_wheel_speed(self):
        return self._right_wheel_speed

    @right_wheel_speed.setter
    def right_wheel_speed(self, value):
        self.reacted = True
        self._right_wheel_speed = value

