#!/usr/bin/env python3
from argparse import ArgumentParser
from time import sleep

import RPi.GPIO as GPIO


parser = ArgumentParser()
parser.add_argument("-s", "--sleep", default=3, type=int, help="loop sleep")
args = parser.parse_args()

sd = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

while(1):
    print("OUT")
    GPIO.setup(sd, GPIO.OUT)
    sleep(args.sleep)

    print("HIGH")
    GPIO.output(sd, GPIO.HIGH)
    sleep(args.sleep)

    print("LOW")
    GPIO.output(sd, GPIO.LOW)
    sleep(args.sleep)

    print("IN")
    GPIO.setup(sd, GPIO.IN)
    sleep(args.sleep)

    print("HIGH")
    GPIO.output(sd, GPIO.HIGH)
    sleep(args.sleep)

    print("LOW")
    GPIO.output(sd, GPIO.LOW)
    sleep(args.sleep)
