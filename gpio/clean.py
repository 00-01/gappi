#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

a, b, c = 2, 3, 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(a, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.setup(c, GPIO.OUT)

GPIO.output(a, GPIO.HIGH)
GPIO.output(b, GPIO.HIGH)
GPIO.output(c, GPIO.HIGH)
