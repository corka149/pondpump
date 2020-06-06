#!/usr/bin/env python3
import logging
from contextlib import suppress

import RPi.GPIO as GPIO
import requests

import com


class PowerListener:

    def __init__(self):
        self.power_in_gpio = 13
        self.listener_endpoint = 'http://:4000/v1/device/pond_pump_149'

    def listen(self):
        while True:
            # wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
            if GPIO.wait_for_edge(self.power_in_gpio, GPIO.RISING, timeout=5000) is None:
                logging.info('Enter inactivity')
                self.send_is_inactive()
            else:
                logging.info('Pond pump is active')
                self.send_is_active()

    def send_is_active(self):
        requests.get(
            self.listener_endpoint + '/active'
        )

    def send_is_inactive(self):
        requests.get(
            self.listener_endpoint + '/inactive'
        )


if __name__ == '__main__':
    com.prepare()
    with suppress(KeyboardInterrupt):
        power_listener = PowerListener()
        power_listener.listen()
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup(power_listener.power_in_gpio)
    print('Sender finished')
