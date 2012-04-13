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


class Search(object):

    rand_double_left = 0
    rand_double_right = 0
    count_limit = 20
    rand_double_left = 0
    rand_double_right = 0
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
        [1, 1, 0, 1, 1, 0],
        [1, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 0, 1]
    ]

    def __init__(self, right_wheel_speed=0, left_wheel_speed=0):
        self.left_wheel_speed = left_wheel_speed
        self.right_wheel_speed = right_wheel_speed

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

            if threshold_list[0] == self.case_script[i][0]\
               and threshold_list[1] == self.case_script[i][1]\
               and threshold_list[2] == self.case_script[i][2]\
               and threshold_list[3] == self.case_script[i][3]:

                if self.counter == self.count_limit:
                    self.counter = 0
                    self.rand_double()

                if self.case_script[i][4] == self.case_script[i][5]:  # Free passage; Straight forward
                    self.left_wheel_speed = (self.rand_double_left * 500) + 500
                    self.right_wheel_speed = (self.rand_double_right * 500) + 500

                elif self.case_script[i][4] == 1 and self.case_script[i][5] == 0:  # Turn left
                    self.left_wheel_speed = -300
                    self.right_wheel_speed = 700

                else:  # Turn right
                    self.left_wheel_speed = 700
                    self.right_wheel_speed = -300

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


def main():
    """
        just for tests
    """
    s = Search()
    s.rand_double()
    sensor_value = [random() for i in range(8)]
    distance_threshold = [random() for i in range(16)]
    s.update_search_speed(sensor_value, distance_threshold)

if __name__ == "__main__":
    main()
