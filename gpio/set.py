#!/usr/bin/env python3
import argparse
import RPi.GPIO as GPIO

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pin", default=1, type=int, help="pin number")
parser.add_argument("-s", "--state", default="LOW", help="HIGH or LOW")
args = parser.parse_args()

state = GPIO.LOW if args.state == "LOW" else GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pin, GPIO.OUT)

GPIO.output(args.pin, state)
