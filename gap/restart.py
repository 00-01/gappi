#!/usr/bin/env python3
from time import sleep
import RPi.GPIO as GPIO

sd = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sd, GPIO.OUT)

print("HIGH")
GPIO.output(sd, GPIO.HIGH)

sleep(1)

print("LOW")
GPIO.output(sd, GPIO.LOW)
