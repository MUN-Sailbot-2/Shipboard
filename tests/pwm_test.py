import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_I2C import Adafruit_I2C

import time

def setup():
    PWM.cleanup()
    GPIO.cleanup()

def fade_leds():
    for i in range(101):
        PWM.set_duty_cycle("P9_14", i)
        time.sleep(0.002)
    for i in range(100, -1, -1):
        PWM.set_duty_cycle("P9_14", i)
        time.sleep(0.002)

def main():
    PWM.start("P9_14", 50, 2000)
    for _ in range(10):
        fade_leds()


    PWM.stop("P9_14")

def cleanup():
    PWM.cleanup()


if __name__ == '__main__':
    setup()
    #import pdb
    #pdb.set_trace()
    main()
    cleanup()
