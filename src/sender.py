#!/usr/bin/env python3

import logging

import RPi.GPIO as GPIO
from rpi_rf import RFDevice

import com

GPIO.setmode(GPIO.BCM)
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)


class RfDevice:

    def __init__(self):
        self.power_in_gpio = 13
        self.sending_gpio = 17
        self.protocol = None
        self.pulselength = None
        self.length = None
        self.rfdevice = None
        self.tx_repeat = 10

    def __enter__(self):
        self.rfdevice = RFDevice(self.sending_gpio)
        self.rfdevice.enable_tx()
        self.rfdevice.tx_repeat = self.tx_repeat
        GPIO.setup(self.power_in_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rfdevice.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup(self.power_in_gpio)

    def listen(self):
        while True:
            # wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
            if GPIO.wait_for_edge(self.power_in_gpio, GPIO.RISING, timeout=5000) is None:
                self.send_is_inactive()
            else:
                self.send_is_active()

    def send_is_active(self):
        self.rfdevice.tx_code(com.PUMP_IS_ACTIVE, self.protocol, self.pulselength, self.length)

    def send_is_inactive(self):
        self.rfdevice.tx_code(com.PUMP_IS_INACTIVE, self.protocol, self.pulselength, self.length)


if __name__ == '__main__':
    with RfDevice() as rf_device:
        rf_device.listen()
