import logging

import RPi.GPIO as GPIO


PUMP_IS_ACTIVE = 111111111
PUMP_IS_INACTIVE = 111


def prepare():
    GPIO.setmode(GPIO.BCM)
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )
