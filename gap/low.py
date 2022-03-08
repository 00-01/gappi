#!/usr/bin/env python3
from argparse import ArgumentParser
from time import sleep

import RPi.GPIO as GPIO


parser = ArgumentParser()
parser.add_argument("-s", "--sleep", default=0, help="loop sleep")
args = parser.parse_args()

sd = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sd, GPIO.OUT)

print("LOW")
GPIO.output(sd, GPIO.LOW)

sleep(args.sleep)
