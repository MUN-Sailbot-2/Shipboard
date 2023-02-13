import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
#from Adafruit_I2C import Adafruit_I2C
import time

class StepperMotor():
    def __init__(self, dir_pin, step_pin, degrees_per_step):
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.degrees_per_step = degrees_per_step
        self.current_position = 0

        self.setup()

    def setup(self):
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)

    def step(self, direction):
        if direction: # bool
            GPIO.output(self.dir_pin, GPIO.HIGH)
            position_update_deg = self.degrees_per_step
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)
            position_update_deg = -1 * self.degrees_per_step
        
        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(0.003) # Assume 3 millisecond delay between steps for now.
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(0.003)
        # This isn't the most efficient way to keep track of the motor's
        # position, but it is the most simple because self.step() will likely
        # be called every time.
        self.current_position = self.current_position + position_update_deg
    
    def rotate_deg(self, direction, degrees):
        no_of_steps = int(degrees // self.degrees_per_step)
        for step_counter in range(no_of_steps):
            self.step(direction)
    
    def rotate_to_position(self, desired_position):
        # TODO add function to force desired position between 0 and 360.
        required_adjustment = desired_position - self.current_position
        direction = True
        if required_adjustment < 0:
            direction = False
            required_adjustment = abs(required_adjustment)
        self.rotate_deg(direction, required_adjustment)


def setup():
    PWM.cleanup()
    GPIO.cleanup()

    
def cleanup():
    PWM.cleanup()
    GPIO.cleanup()

def main():
    setup()
    try:
        rudder_motor = StepperMotor("P9_13", "P9_15", 1.8)
        for i in range(5):
            print "Rotating right..."
            rudder_motor.rotate_deg(True, 180)
            print "Rotating left..."
            rudder_motor.rotate_deg(False, 180)
        
        while True:
            new_position = float(input("Enter angle in degrees: "))
            start_position = rudder_motor.current_position
            start_time = time.time()
            rudder_motor.rotate_to_position(new_position)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print "Moved motor from {start_position} to {new_position} in {elapsed_time} s.".format(start_position=start_position, new_position=new_position, elapsed_time=elapsed_time)
            

    finally:
        cleanup()



if __name__ == '__main__':
    main()
