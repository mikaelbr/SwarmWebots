"""
retrieval.c - Follow and push behavior.

Made to make the e-puck converge and push the box.
Created on: 17. mars 2011
    Author: jannik

"""
from behavior_module import *


class Retrieval(BehaviorModule):

    num_leds = 8
    push_threshold = 500

    LED = [False] * 8

    def update_speed(self, IR_number):

        if not IR_number:
            self.left_wheel_speed += 700
        elif IR_number == 7:
            self.right_wheel_speed += 700
        elif IR_number == 1:
            self.left_wheel_speed += 350
        elif IR_number == 6:
            self.right_wheel_speed += 350
        elif IR_number == 2:
            self.left_wheel_speed += 550
            self.right_wheel_speed -= 300
        elif IR_number == 5:
            self.right_wheel_speed += 550
            self.left_wheel_speed -= 300
        elif IR_number == 3:
            self.left_wheel_speed += 500
        elif IR_number == 4:
            self.right_wheel_speed += 500

    def converge_to_box(self, IR_sensor_value, IR_threshold):
        """
            The movement for converging to the box
        """
        self._left_wheel_speed = 0
        self._right_wheel_speed = 0
        for i in range(self.num_leds):

            if IR_sensor_value[i] < IR_threshold:
                self.LED[i] = True
                self.update_speed(i)
            else:
                self.LED[i] = False

    def push_box(self, IR_sensor_value, IR_threshold):
        """
            The behavior when pushing the box
        """
        self._left_wheel_speed = 0
        self._right_wheel_speed = 0

        # Blink for visual pushing feedback
        for i in range(self.num_leds):

            self.LED[i] = not self.LED[i]

            if IR_sensor_value[i] < IR_threshold:
                self.update_speed(i)

        if IR_sensor_value[0] < IR_threshold > IR_sensor_value[7]:
            self.left_wheel_speed = 1000
            self.right_wheel_speed = 1000

    def select_behavior(self, IR_sensor_value):
        """
            Selects the behavior push or converge
        """

        self.push = False
        self.converge = True
        for i in range(self.num_leds):
            if IR_sensor_value[i] < self.push_threshold:
                self.push = True
                break

    ####################################
    # External functions               #
    ####################################

    def swarm_retrieval(self, IR_sensor_value, IR_threshold):
        """
            Converge, push, and stagnation recovery
        """
        self.select_behavior(IR_sensor_value)

        if self.push:
            self.push_box(IR_sensor_value, IR_threshold)

        else:  # converge
            print "Converge"
            self.converge_to_box(IR_sensor_value, IR_threshold)

    def do(self):
        self.swarm_retrieval(self.robot.get_IR(), self.robot.IR_threshold)
        self.robot.update_LED(self.LED)  # Update LEDs

"""
print left_wheel_speed
update_speed(0)
print left_wheel_speed
"""
