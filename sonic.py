import RPi.GPIO as GPIO
import time
import numpy as np
import pandas as pd
import math
from eat_sounds import dispense_wisdom
GPIO.setmode(GPIO.BCM)

'''
pin assignments
'''
TRIG = 26
ECHO = 19
MOTION_INPUT = 21
MAX_RESPONSE_DISTANCE = 60

'''
constants
'''
AVERAGING_WINDOW = 3
DISTANCE_SCANS_PER_MOTION = AVERAGING_WINDOW * 2


def measure_distance():
    '''
    measure distance using ultrasonic sensor
    returns: int representing centimeters
    '''
    GPIO.output(TRIG, False)
    time.sleep(.3)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance


def _measure_distances_cb(iterations, measurements):
    '''
    return an ndarray with measurements this run to be passed to the next run
    '''
    N = 0
    while N <= iterations:
        distance = measure_distance()
        measurements = np.append(measurements, distance)
        mavg = pd.Series(measurements).rolling(window = AVERAGING_WINDOW).mean().values[-1]
        #print("rolling prev %d avg %s \n current measure: %d"  % (AVERAGING_WINDOW, str(mavg), distance))
        N += 1
    return measurements, mavg


if __name__ == "__main__":
    GPIO.cleanup()
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(MOTION_INPUT, GPIO.IN)
    GPIO.add_event_detect( MOTION_INPUT, GPIO.RISING, bouncetime=100)
    measurements = np.array([measure_distance()])
    mavg = 0
    while True:
        if GPIO.input(MOTION_INPUT):
            measurements, mavg = _measure_distances_cb(DISTANCE_SCANS_PER_MOTION, measurements)
        if mavg >= 10 and mavg <= MAX_RESPONSE_DISTANCE:
            num_farts = int(math.floor(mavg/15))
        elif mavg < 10 and mavg > 0:
            num_farts = 1
        else:
            continue
        print("mavg: %d, num_farts: %d" % (mavg, num_farts))
        dispense_wisdom(num_farts)
        mavg = 0

        