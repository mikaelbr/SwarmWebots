"""
retrieval.c - Follow and push behavior.

Made to make the e-puck converge and push the box.
Created on: 17. mars 2011
    Author: jannik
"""


num_leds = 8
push_threshold = 500
left_wheel_speed = 0
right_wheel_speed = 0
LED = []


def update_speed(IR_number):

    if IR_number == 0:
        left_wheel_speed = left_wheel_speed + 700
    elif IR_number == 7:
        right_wheel_speed = right_wheel_speed + 700
    elif IR_number == 1:
        left_wheel_speed = left_wheel_speed + 350
    elif IR_number == 6:
        right_wheel_speed = right_wheel_speed + 350
    elif IR_number == 2:
        left_wheel_speed = left_wheel_speed + 550
        right_wheel_speed = right_wheel_speed - 300
    elif IR_number == 5:
        right_wheel_speed = right_wheel_speed + 550
        left_wheel_speed = left_wheel_speed - 300
    elif IR_number == 3:
        left_wheel_speed = left_wheel_speed + 500
    elif IR_number == 4:
        right_wheel_speed = right_wheel_speed + 500



def converge_to_box(IR_sensor_value, IR_threshold):
    """
        The movement for converging to the box
    """
    left_wheel_speed = 0
    right_wheel_speed = 0

    for i in range(num_leds):

        if IR_sensor_value[i] < IR_threshold:
            LED[i] = True
            update_speed(i)
        else:
            LED[i] = False



def push_box(IR_sensor_value, IR_threshold):
    """
        The behavior when pushing the box
    """
    left_wheel_speed = 0
    right_wheel_speed = 0

    # Blink for visual pushing feedback
    for i in range(num_leds):

        if(LED[i]):
            LED[i] = False
        else:
            LED[i] = True

        if IR_sensor_value[i] < IR_threshold:
            update_speed(i)
    
    if (IR_sensor_value[0] < IR_threshold) and (IR_sensor_value[7]<IR_threshold):
        left_wheel_speed = 1000
        right_wheel_speed = 1000
    
def select_behavior(IR_sensor_value):
    """
        Selects the behavior push or converge
    """

    push = False
    converge = True
    for i in range(num_leds):
        if IR_sensor_value[i] < push_threshold:
            push = True
            break


####################################
# External functions               #
####################################

def swarm_retrieval(IR_sensor_value, IR_threshold):
    """
        Converge, push, and stagnation recovery
    """
    select_behavior(IR_sensor_value)

    if(push):
        push_box(IR_sensor_value, IR_threshold)

    else: # converge
        converge_to_box(IR_sensor_value, IR_threshold)
}


def get_retrieval_left_wheel_speed():
    return left_wheel_speed

def get_retrieval_right_wheel_speed():
    return right_wheel_speed

int get_LED_state(LED_num)
    """
        Returns the state (True/False) of the given LED number
    """
    return LED[LED_num]
