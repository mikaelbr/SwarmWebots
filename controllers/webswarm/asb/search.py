"""

search.c - Search and Avoid behavior.

 Made to calculate the speed from distance sensors input.
 By getting sensor input from the four front distance sensors on the e-puck
 it will be determined the speed of the left and right wheel according to
 the case script and a threshold. If nothing is in your way - search.

 case script: the four first int's are the sensor input, while the last two are speed
 Created on: 17. mars 2011
     Author: jannik

"""
from random import random
from behavior_module import *


class Search(BehaviorModule):

    rand_double_left = 0
    rand_double_right = 0
    count_limit = 20
    counter = 0

    case_script = [
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1],
        [0, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 1],
        [1, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 0, 0]
    ]

    def __init__(self):
        super(Search, self).__init__()

    def rand_double(self):
        """
            Generates random double for left and right search speed
        """
        self.rand_double_left = random()
        self.rand_double_right = random()

    def calculate_search_speed(self, threshold_list):
        """
            Given the input compared to the case script; where do we want to go?
        """
        self.counter += 1

        for i in range(16):

            if threshold_list == self.case_script[i][:4]:

                if self.counter == self.count_limit:
                    self.counter = 0
                    self.rand_double()

                if self.case_script[i][4] == self.case_script[i][5]:

                    if self.case_script[i][4]:
                        self.left_wheel_speed = (self.rand_double_left * 500) + 500
                        self.right_wheel_speed = (self.rand_double_right * 500) + 500
                    else:

                        # if random() > 0.5:
                            self.left_wheel_speed = -300
                            self.right_wheel_speed = 700
                        # else:
                        #     self.left_wheel_speed = 700
                        #     self.right_wheel_speed = -300

                elif self.case_script[i][4] == 1 and self.case_script[i][5] == 0:  # Turn left
                    self.left_wheel_speed = -300
                    self.right_wheel_speed = 700

                    # Make so the robot tries a new direction next time
                    self.counter = 10
                    self.rand_double_left = 0.3
                    self.rand_double_right = 0.7

                else:  # Turn right
                    self.left_wheel_speed = 700
                    self.right_wheel_speed = -300

                    # Make so the robot tries a new direction next time
                    self.counter = 10
                    self.rand_double_left = 0.7
                    self.rand_double_right = 0.3

                return

    def calculate_threshold(self, sensors, distance_threshold):
        """
            Calculate if there is an obstacle or not, depending on the threshold
        """
        threshold_list = []
        for i in range(4):
            if sensors[i] > distance_threshold[i]:
                threshold_list.append(1)  # obstacle
            else:
                threshold_list.append(0)  # Free passage

        self.calculate_search_speed(threshold_list)

    def update_search_speed(self, sensor_value, distance_threshold):
        """
            Given the sensor input and threshold, calculates the speed for survival
        """
        sensors = [sensor_value[6], sensor_value[7], sensor_value[0], sensor_value[1]]
        self.calculate_threshold(sensors, distance_threshold)

    def do(self):
        self.update_search_speed(self.robot.get_proximities(), self.robot.distance_threshold)
