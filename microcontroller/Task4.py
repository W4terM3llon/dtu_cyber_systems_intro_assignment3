from machine import I2C, PWM

from PinDefinitions import rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, sda_pin, scl_pin, red_pwm, green_pwm, blue_pwm
from Task3 import Task3, convert_to_celcius


class Task4(Task3):
    def __init__(self):
        super().__init__()
        self.MAX_DUTY = 2**10-1
        
        self.red_pwm = red_pwm
        self.green_pwm = green_pwm
        self.blue_pwm = blue_pwm

    def run_iteration(self):
        data = bytearray(2)
        self.i2c.readfrom_mem_into(24,5,data)
        temp = convert_to_celcius(data)

        green_orange_threshold = 28
        orange_red_threshold = 31
        
        if temp < green_orange_threshold:
            self.red_pwm.duty(0)
            self.green_pwm.duty(self.MAX_DUTY)
            self.blue_pwm.duty(0)
        elif temp >= green_orange_threshold and temp <= orange_red_threshold:
            self.red_pwm.duty(self.MAX_DUTY)
            self.green_pwm.duty(self.MAX_DUTY)
            self.blue_pwm.duty(0)
        elif temp > orange_red_threshold:
            self.red_pwm.duty(self.MAX_DUTY)
            self.green_pwm.duty(0)
            self.blue_pwm.duty(0)

        print(f"Task4; Temperature: {temp}")
    
    def end_task(self):
        self.red_pwm.duty(0)
        self.green_pwm.duty(0)
        self.blue_pwm.duty(0)