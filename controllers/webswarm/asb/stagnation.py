"""

stagnation.c Stagnation recovery behavior

Whenever the e-puck reason about his push behavior not being effective,
the stagnation behavior should trigger. This behavior will reposition the
robot, hopefully getting a spot which will result
 Created on: 23. mars 2011
     Author: jannik

"""
from random import random
from behavior_module import *


class Stagnation(BehaviorModule):

    IR_DIFF_THRESHOLD = 4
    DISTANCE_DIFF_THRESHOLD = 10
    REVERSE_LIMIT = 20
    TURN_LIMIT = 10
    FORWARD_LIMIT = 40
    NEIGHBOR_LIMIT = 300

    NEUTRAL = 3

    ALIGN_STRAIGTH_THRESHOLD = 10  # If bigger, align straight
    LOW_DIST_VALUE = 10  # if lower (and detecting IR), the sensor is close.

    # Boolean variables
    has_recovered = False
    turn_left = NEUTRAL

    # Green LED
    green_LED_state = False  # Visual feedback

    # Counters
    reverse_counter = 0
    turn_counter = 0
    forward_counter = 0
    twice = 0
    align_counter = 0

    ################################
    # Internal functions
    ################################

    def __init__(self):
        super(Stagnation, self).__init__()

    def LED_blink(self):
        """
            Let it shine baby!
        """
        self.green_LED_state = not(self.green_LED_state)

    def realign(self, distance_value):

        # Find the difference of the two front IR sensors
        dist_diff_front = distance_value[7] - distance_value[0]

        # Are we pushing straight? If not, maybe we should try. If we are, maybe we should
        # try pushing from another angle.
        if abs(dist_diff_front) > self.ALIGN_STRAIGTH_THRESHOLD:  # True = we are not pushing straight
            # Lets push straight, but which way are we angled?
            if distance_value[0] < self.LOW_DIST_VALUE:  # //True = turn little right

                self.right_wheel_speed = -500
                self.left_wheel_speed = 500

            elif distance_value[7] < self.LOW_DIST_VALUE:  # // True = turn little left

                self.right_wheel_speed = 500
                self.left_wheel_speed = -500

            elif distance_value[1] < self.LOW_DIST_VALUE:  # // True = turn right

                self.right_wheel_speed = -1000
                self.left_wheel_speed = 700

            elif distance_value[6] < self.LOW_DIST_VALUE:  # // True = turn left

                self.right_wheel_speed = 700
                self.left_wheel_speed = -1000

        else:  # We are standing straight, lets try pushing with another angle.

            # Roll a dice, left angle or right angle?
            if random() > 0.5:

                self.right_wheel_speed = -500
                self.left_wheel_speed = 500

            else:

                self.right_wheel_speed = 500
                self.left_wheel_speed = -500

        self.has_recovered = True
        self.green_LED_state = False

    ####################################
    # External functions
    ####################################

    def find_new_spot(self, distance_value, DIST_THRESHOLD):
        if self.twice == 2:  # Reverse, Turn, Forward, Turn(opposite), Forward.

            self.has_recovered = True
            self.green_LED_state = False
            self.align_counter = 0

        elif self.reverse_counter != self.REVERSE_LIMIT:  # Make space by moving away from the box

            self.reverse_counter += +1
            self.left_wheel_speed = -800
            self.right_wheel_speed = -800

        elif self.turn_counter != self.TURN_LIMIT:  # Line up with one of the sides of the box

            self.turn_counter += 1
            self.forward_counter = 0

            if self.turn_left == self.NEUTRAL:
                # Roll a dice, left or right?
                self.turn_left = (random() > 0.5)

            if self.turn_left:  # Turn left
                self.left_wheel_speed = -300
                self.right_wheel_speed = 700

            else:  # Turn right
                self.left_wheel_speed = 700
                self.right_wheel_speed = -300

        elif self.forward_counter != self.FORWARD_LIMIT:
            self.forward_counter += 1
            if self.forward_counter == self.FORWARD_LIMIT - 1:
                self.twice += 1
                self.turn_counter = 0
                self.turn_left = not(self.turn_left)

            self.update_search_speed(distance_value, DIST_THRESHOLD)
            self.left_wheel_speed = self.get_search_left_wheel_speed()
            self.right_wheel_speed = self.get_search_right_wheel_speed()

            if self.left_wheel_speed > 0 and self.right_wheel_speed > 0:
                self.left_wheel_speed = 1000
                self.left_wheel_speed = 1000

    def reset_stagnation(self):
        self.has_recovered = False
        self.reverse_counter = 0
        self.turn_counter = 0
        self.forward_counter = 0
        self.turn_left = self.NEUTRAL
        self.twice = 0

    def stagnation_recovery(self, distance_sensors_value, DIST_THRESHOLD):

        if self.align_counter < 2:  # Align
            self.align_counter += 1
            self.realign(distance_sensors_value)

        elif self.align_counter > 0:  # Reposition
            self.LED_blink()
            self.find_new_spot(distance_sensors_value, DIST_THRESHOLD)

    def valuate_pushing(self, dist_value, prev_dist_value):
        """
            To keep pushing or not to keep pushing, that is the question
        """
        # Only assess this situation once
        # The front IR sensors pushing against the box

        dist_diff7 = prev_dist_value[7] - dist_value[7]
        dist_diff0 = prev_dist_value[0] - dist_value[0]

        # Validate if this works
        if (
                ((abs(dist_diff7) > self.DISTANCE_DIFF_THRESHOLD) and (abs(dist_diff0) > self.DISTANCE_DIFF_THRESHOLD))
                or
                ((dist_value[5] > self.NEIGHBOR_LIMIT) and (dist_value[2] > self.NEIGHBOR_LIMIT))  # Has any neighbors
                or
                (((dist_value[5] > self.NEIGHBOR_LIMIT) or (dist_value[2] > self.NEIGHBOR_LIMIT)) and random() > 0.5)
            ):

            self.has_recovered = True  # Keep pushing, it is working
            self.green_LED_state = False  # No more recovery
            self.align_counter = 0

    def get_stagnation_state(self):
        """
            Return the boolean value of whether or not to continue with this behavior
        """
        return self.has_recovered

    def get_green_LED_state(self):
        """
            Returns the state (True/False) for green LED
        """
        return self.green_LED_state

    def get_stagnation_left_wheel_speed(self):
        return self.left_wheel_speed

    def get_stagnation_right_wheel_speed(self):
        return self.right_wheel_speed


stag = Stagnation()
print stag.get_stagnation_left_wheel_speed()
stag.realign([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])
print stag.get_stagnation_left_wheel_speed()
