#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

sd = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sd, GPIO.OUT)

print("HIGH")
GPIO.output(sd, GPIO.HIGH)

time.sleep(2)

print("LOW")
GPIO.output(sd, GPIO.LOW)
