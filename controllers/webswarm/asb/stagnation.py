"""

stagnation.c Stagnation recovery behavior

Whenever the e-puck reason about his push behavior not being effective,
the stagnation behavior should trigger. This behavior will reposition the
robot, hopefully getting a spot which will result
 Created on: 23. mars 2011
     Author: jannik

"""


from random import random


IR_DIFF_THRESHOLD = 4
DISTANCE_DIFF_THRESHOLD = 10
REVERSE_LIMIT = 20
TURN_LIMIT = 10
FORWARD_LIMIT = 40
NEIGHBOR_LIMIT = 300

NEUTRAL = 3

ALIGN_STRAIGTH_THRESHOLD = 10 # If bigger, align straight
LOW_DIST_VALUE = 10 # if lower (and detecting IR), the sensor is close.

# Wheel speed variables
left_wheel_speed = 0
right_wheel_speed = 0

# Boolean variables
has_recovered = False
turn_left = NEUTRAL

# Green LED
green_LED_state = False # Visual feedback

# Counters
reverse_counter = 0
turn_counter = 0
forward_counter = 0
twice = 0
align_counter = 0


################################
# Internal functions
################################

def LED_blink(): 
    """
        Let it shine baby!
    """
    green_LED_state = not(green_LED_state)

def realign(distance_value):

    # Find the difference of the two front IR sensors
    dist_diff_front = distance_value[7] - distance_value[0]

    # Are we pushing straight? If not, maybe we should try. If we are, maybe we should
    # try pushing from another angle.
    if abs(dist_diff_front) > ALIGN_STRAIGTH_THRESHOLD : # True = we are not pushing straight
        # Lets push straight, but which way are we angled?
        if distance_value[0] < LOW_DIST_VALUE: # //True = turn little right

            right_wheel_speed = -500
            left_wheel_speed = 500

        elif distance_value[7] < LOW_DIST_VALUE: # // True = turn little left

            right_wheel_speed = 500
            left_wheel_speed = -500

        elif distance_value[1] < LOW_DIST_VALUE: # // True = turn right
        
            right_wheel_speed = -1000
            left_wheel_speed = 700
        
        elif distance_value[6] < LOW_DIST_VALUE: # // True = turn left
        
            right_wheel_speed = 700
            left_wheel_speed = -1000
        
    
    else: # We are standing straight, lets try pushing with another angle.
        
        # Roll a dice, left angle or right angle?
        ran = random()
        if ran > 0.5:

            right_wheel_speed = -500
            left_wheel_speed = 500

        else:

            right_wheel_speed = 500
            left_wheel_speed = -500


    has_recovered = True
    green_LED_state = False


####################################
# External functions
####################################


def find_new_spot(distance_value, DIST_THRESHOLD):
    if twice == 2: # Reverse, Turn, Forward, Turn(opposite), Forward.

        has_recovered = True
        green_LED_state = False
        align_counter = 0

    elif reverse_counter != REVERSE_LIMIT: # Make space by moving away from the box

        reverse_counter = reverse_counter +1;
        left_wheel_speed = -800
        right_wheel_speed = -800

    elif turn_counter != TURN_LIMIT: # Line up with one of the sides of the box

        turn_counter += 1
        forward_counter = 0

        if turn_left == NEUTRAL:
            # Roll a dice, left or right?
            if (random() > 0.5):
                turn_left = False
            else:
                turn_left = True

        if turn_left: # // Turn left
            left_wheel_speed = -300
            right_wheel_speed = 700

        else: # Turn right
            left_wheel_speed = 700
            right_wheel_speed = -300

    elif forward_counter != FORWARD_LIMIT:
        forward_counter += 1
        if forward_counter == FORWARD_LIMIT-1:
            twice += 1
            turn_counter = 0
            if turn_left:
                turn_left = False;
            else:
                turn_left = True;

        update_search_speed(distance_value, DIST_THRESHOLD)
        left_wheel_speed = get_search_left_wheel_speed()
        right_wheel_speed = get_search_right_wheel_speed()

        if left_wheel_speed > 0 and right_wheel_speed > 0 :
            right_wheel_speed = 1000
            left_wheel_speed = 1000


def reset_stagnation():
    has_recovered = False
    reverse_counter = 0
    turn_counter = 0
    forward_counter = 0
    turn_left = NEUTRAL
    twice = 0




def stagnation_recovery(distance_sensors_value, DIST_THRESHOLD):

    if align_counter < 2: # Align
        align_counter += 1
        realign(distance_sensors_value)

    elif align_counter > 0: # Reposition
        LED_blink()
        find_new_spot(distance_sensors_value, DIST_THRESHOLD)


def valuate_pushing(dist_value, prev_dist_value):
    """
        To keep pushing or not to keep pushing, that is the question
    """
    # Only assess this situation once
    # The front IR sensors pushing against the box

    dist_diff7 = prev_dist_value[7] - dist_value[7]
    dist_diff0 = prev_dist_value[0] - dist_value[0]

    # Validate if this works
    if (
            ((abs(dist_diff7) > DISTANCE_DIFF_THRESHOLD) and (abs(dist_diff0) > DISTANCE_DIFF_THRESHOLD))
            or
            ((dist_value[5] > NEIGHBOR_LIMIT) and (dist_value[2] > NEIGHBOR_LIMIT)) # Has any neighbors
            or 
            ( ((dist_value[5] > NEIGHBOR_LIMIT) or (dist_value[2] > NEIGHBOR_LIMIT)) and random() > 0.5)
        ):

        has_recovered = True # Keep pushing, it is working
        green_LED_state = False # No more recovery
        align_counter = 0



def get_stagnation_state():
    """
        Return the boolean value of whether or not to continue with this behavior
    """
    return has_recovered

def get_green_LED_state():
    """
        Returns the state (True/False) for green LED
    """
    return green_LED_state


def get_stagnation_left_wheel_speed():
    return left_wheel_speed


def get_stagnation_right_wheel_speed():
    return right_wheel_speed
