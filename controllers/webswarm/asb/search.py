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



COUNTLIMIT = 20

# Case scenarios for for navigation 
case_script= [
    [0,0,0,0,1,1],
    [0,0,0,1,1,0],
    [0,0,1,0,1,0],
    [0,0,1,1,1,0],
    [0,1,0,0,0,1],
    [0,1,0,1,1,0],
    [0,1,1,0,0,1],
    [0,1,1,1,1,0],
    [1,0,0,0,0,1],
    [1,0,0,1,1,0],
    [1,0,1,0,0,1],
    [1,0,1,1,1,0],
    [1,1,0,0,0,1],
    [1,1,0,1,1,0],
    [1,1,1,0,0,1],
    [1,1,1,1,0,1]
]


# Wheel speed variables
left_wheel_speed = 0 # default 0
right_wheel_speed = 0

# Random search speed
rand_double_left = 0
rand_double_right = 0

# Counter
counter = 0


###########################
# Internal functions
###########################

def randdouble():
    """
        Generates random double for left and right search speed
    """
    rand_double_left =  random()
    rand_double_right = random()


def calculate_search_speed(threshold_list):
    """
        Given the input compared to the case script; where do we want to go?
    """
    
    counter += 1;

    for i in range(16):

        if threshold_list[0] == case_script[i][0] \
            and threshold_list[1] == case_script[i][1] \
            and threshold_list[2] == case_script[i][2] \
            and threshold_list[3] == case_script[i][3]:

            if counter == COUNTLIMIT:
                counter = 0
                randdouble()

            if case_script[i][4] == case_script[i][5]: # Free passage; Straight forward
                left_wheel_speed = (rand_double_left*500) + 500
                right_wheel_speed = (rand_double_right*500) + 500

            elif case_script[i][4] == 1 and case_script[i][5] == 0: # Turn left
                left_wheel_speed = -300
                right_wheel_speed = 700

            else: # Turn right
                left_wheel_speed = 700
                right_wheel_speed = -300


            return
        

def calculate_treshold(sensors, distance_threshold):
    """
        Calculate if there is an obstacle or not, depending on the threshold
    """
    threshold_list = []
    for i in range (4):
        if sensors[i] > distance_threshold:
            threshold_list[i] = 1 # obstacle
        else:
            threshold_list[i] = 0 # Free passage

    calculate_search_speed(threshold_list)



#########################
# External functions
#########################

def update_search_speed(sensor_value, distance_threshold):
    """
        Given the sensor input and threshold, calculates the speed for survival
    """
    sensors = [sensor_value[6], sensor_value[7], sensor_value[0], sensor_value[1]]
    calculate_treshold(sensors, distance_threshold)


def get_search_left_wheel_speed():
    return left_wheel_speed

def get_search_right_wheel_speed():
    return right_wheel_speed





