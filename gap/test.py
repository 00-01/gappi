#!/usr/bin/env python3
from argparse import ArgumentParser
from time import sleep

import RPi.GPIO as GPIO


parser = ArgumentParser()
parser.add_argument("-s", "--sleep", default=10, type=int, help="loop sleep")
args = parser.parse_args()

sd = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

while(1):
    print("IN")
    GPIO.setup(sd, GPIO.IN)
    sleep(args.sleep)

    print("OUT")
    GPIO.setup(sd, GPIO.OUT)
    sleep(args.sleep)

