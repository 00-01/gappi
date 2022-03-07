#!/usr/bin/env python3
import RPi.GPIO as GPIO


sd = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sd, GPIO.OUT)

print("LOW")
GPIO.output(sd, GPIO.LOW)
