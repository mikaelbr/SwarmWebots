"""
    A module used by the behavior controller. This is the base
    layer ment to be extended by different implementations.

    All layers must implement their own do() method.

    When either left or right wheel speed is set/altered,
    the reacted flag will be set, and the controller know
    that this layer has been executed (reacted).
"""


class BehaviorModule(object):

    def __init__(self):
        self.reacted = False
        self.robot = None
        self._left_wheel_speed = 0
        self._right_wheel_speed = 0

    def reset(self):
        self._left_wheel_speed = 0
        self._right_wheel_speed = 0
        self.reacted = False

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

    def do(self):
        """
            Implementation method. Abstract in this case,
            but must be implementet by the sub classes.
        """
        pass
