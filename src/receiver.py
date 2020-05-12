#!/usr/bin/env python3

import signal
import sys
import time
import logging

from rpi_rf import RFDevice
import RPi.GPIO as GPIO

import com

GPIO.setmode(GPIO.BCM)
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )


class RfDevice:

    def __init__(self):
        self.listing_gpio = 27
        self.light_gpio = 5
        self.rf_device = None

    def __enter__(self):
        self.rf_device = RFDevice(self.listing_gpio)
        self.rf_device.enable_rx()
        signal.signal(signal.SIGINT, self.exit_handler)
        GPIO.setup(self.light_gpio, GPIO.OUT, initial=GPIO.HIGH)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rf_device.cleanup()
        GPIO.cleanup(self.light_gpio)

    def exit_handler(self, _signal, _frame):
        self.rf_device.cleanup()
        sys.exit(0)

    @property
    def rx_code(self):
        return self.rf_device.rx_code

    def listen(self):
        timestamp = None
        logging.info("Listening for codes on GPIO " + str(self.listing_gpio))
        while True:
            time.sleep(0.01)
            if self.rf_device.rx_code_timestamp != timestamp:
                timestamp = self.rf_device.rx_code_timestamp

                if self.rx_code == com.PUMP_IS_ACTIVE:
                    self.turn_light_on()
                elif self.rx_code == com.PUMP_IS_INACTIVE:
                    self.turn_light_off()
                else:
                    logging.info("Unknown code:" + str(self.rx_code) +
                                 " [pulselength " + str(self.rf_device.rx_pulselength) +
                                 ", protocol " + str(self.rf_device.rx_proto) + "]")

    def turn_light_on(self):
        logging.info('Pump is running')
        GPIO.output(self.light_gpio, GPIO.HIGH)

    def turn_light_off(self):
        logging.info('Pump is inactive')
        GPIO.output(self.light_gpio, GPIO.LOW)


if __name__ == '__main__':
    with RfDevice() as rf_device:
        rf_device.listen()
