#!/usr/bin/env python3
import os
from argparse import ArgumentParser
from datetime import datetime
from time import sleep, time

import RPi.GPIO as GPIO
import serial
from picamera import PiCamera
from PIL import Image


parser = ArgumentParser()
parser.add_argument("-l", "--loop", default=0, type=int, help="run loop")
parser.add_argument("-gs1", "--gap_sleep1", default=1, type=int, help="gap sleep1")
parser.add_argument("-gs2", "--gap_sleep2", default=3, type=int, help="gap sleep2")
parser.add_argument("-s", "--sleep", default=0, type=int, help="loop sleep")
args = parser.parse_args()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sd = 27
GPIO.setup(sd, GPIO.OUT)

print("[I] GAP HIGH")
GPIO.output(sd, GPIO.LOW)
sleep(args.gap_sleep1)
GPIO.output(sd, GPIO.HIGH)
sleep(args.gap_sleep2)

tr = 17  # trigger ir
GPIO.setup(tr, GPIO.OUT)
GPIO.output(tr, GPIO.LOW)

ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=10, )

w, h = 80, 80
size = 1
img_size = w*h*size
det_size = 3+(30*12)
threshold = 40

with open('device_id.txt') as f:
    device_id = f.readline().rstrip()

LOOP = 1
while LOOP:
    camera = PiCamera()
    start = time()
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d  %H:%M:%S")
    dtime = now.strftime("%Y%m%d-%H%M%S")

    print(f"[START] {'-'*20} [{dt}]")
    print(f"[I] loop is {args.loop}, sleep is {args.sleep} sec")

    camera.start_preview()

    base_dir = f"data/{dtime}/"
    det_file = f"{base_dir}{dtime}_{device_id}_DET.txt"
    ir_img_file = f"{base_dir}{dtime}_{device_id}_IR.png"
    rgb_file = f"{base_dir}{dtime}_{device_id}_RGB.jpg"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    ser.flush()
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    print("[TX] TRIGGER")
    GPIO.output(tr, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(tr, GPIO.LOW)

    print("[S] capturing rgb image")
    camera.capture(rgb_file)
    camera.stop_preview()
    camera.close()
    # os.system(f"/bin/bash grubFrame.sh {device_id} {dtime}")

    print("[RX] DETECTION")
    rx_det = ser.read()
    while len(rx_det) < (det_size):
        new_det = ser.read()
        rx_det += new_det

    print("[RX] IMAGE")
    rx_img = ser.readline()
    while len(rx_img) < (img_size):
        new_img = ser.read()
        rx_img += new_img

    print("[TX] THRESHOLD")
    ser.write(threshold.to_bytes(4, byteorder='little'))

    print("[S] saving detection to txt")
    det = ""
    det_str = rx_det.decode(encoding='UTF-8', errors='ignore')
    with open(det_file, "w") as file:
        det_str = det_str.split(";")
        st = 0
        for i in det_str:
            if "\00" not in i:
                if i is not None:
                    det += i
                    if st != 0:
                        file.write(f",")
                    file.write(f"{i}")
                    st = 1

    print("[S] saving binary to image")
    img = Image.frombuffer("L", (w, h), rx_img, 'raw', "L", 0, 1)
    img.save(ir_img_file)

    print("[I] GAP LOW")
    GPIO.output(sd, GPIO.LOW)

    end = time()-start
    print(f"[FINISH] {'-'*20} [runtime: {round(end, 2)} sec]", "\n"*2)


    LOOP = args.loop
    sleep(args.sleep)
