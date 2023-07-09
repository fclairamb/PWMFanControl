#!/usr/bin/env python3
# Created by: Michael Klements
# https://github.com/mklements/PWMFanControl

import RPi.GPIO as IO          # Calling GPIO to allow use of the GPIO pins
import time                    # Calling time to allow delays to be used
import subprocess              # Calling subprocess to get the CPU temperature
import logging

MAX_TEMP=50.0
MIN_TEMP=70.0
MIN_DUTY_INCREMENT=5
MIN_DUTY_DECREMENT=10
PWM_FREQUENCY=100

logging.basicConfig(
  level='DEBUG'
)

IO.setwarnings(False)          # Do not show any GPIO warnings
IO.setmode (IO.BCM)            # BCM pin numbers - PIN8 as ‘GPIO14’
IO.setup(14,IO.OUT)            # Initialize GPIO14 as our fan output pin
fan = IO.PWM(14,PWM_FREQUENCY)           # Set GPIO14 as a PWM output, with 100Hz frequency (this should match your fans specified PWM frequency)
fan.start(0)                   # Generate a PWM signal with a 0% duty cycle (fan off)

def get_temp() -> float:                              
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read())/1000

last_duty_cycle = -1

while True:                                 
    time.sleep(5)
    temp = get_temp()                        
    logging.debug("Temp: %f", temp)
    duty_cycle = (temp - MIN_TEMP)/(MAX_TEMP-MIN_TEMP)*100
    logging.debug("Duty cycle: %f", duty_cycle)

    if duty_cycle < 10:
        duty_cycle = 0
    elif duty_cycle > 100:
        duty_cycle = 100
    
    if duty_cycle == last_duty_cycle:
        continue
    
    if duty_cycle > last_duty_cycle and duty_cycle != 100 and duty_cycle - MIN_DUTY_INCREMENT < last_duty_cycle:
        continue

    if duty_cycle < last_duty_cycle and duty_cycle != 0 and duty_cycle + MIN_DUTY_DECREMENT > last_duty_cycle:
        continue

    logging.info("Changing duty cycle from %f to %f", last_duty_cycle, duty_cycle)
    fan.ChangeDutyCycle(duty_cycle)
    last_duty_cycle=duty_cycle
