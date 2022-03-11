#!/usr/bin/env python3
from argparse import ArgumentParser
from time import sleep

import RPi.GPIO as GPIO


parser = ArgumentParser()
parser.add_argument("-s", "--sleep", default=0, type=int, help="loop sleep")
args = parser.parse_args()

sd = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sd, GPIO.OUT)

print("HIGH")
GPIO.output(sd, GPIO.HIGH)

sleep(args.sleep)
