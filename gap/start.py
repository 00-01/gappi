#!/usr/bin/env python3
import argparse
import time

import RPi.GPIO as GPIO

gp = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gp, GPIO.OUT)
GPIO.output(gp, GPIO.LOW)

print("TX: start signal")
GPIO.output(gp, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(gp, GPIO.LOW)
