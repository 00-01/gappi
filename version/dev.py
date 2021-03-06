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
parser.add_argument("-s", "--sleep", default=0, type=int, help="loop sleep")
parser.add_argument("-r", "--rotation", default=0, type=int, help="ratate image")
parser.add_argument("-c", "--calibration", default=0, type=int, help="calibration")
args = parser.parse_args()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sd = 27 # gap ON/OFF
GPIO.setup(sd, GPIO.OUT)
GPIO.output(sd, GPIO.LOW)

tr = 17  # ir trigger
GPIO.setup(tr, GPIO.IN)

cal = 18  # ir calibration
GPIO.setup(cal, GPIO.OUT)
GPIO.output(cal, GPIO.LOW)

ser = serial.Serial(port='/dev/ttyS0',
                    baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=5, )

w, h = 80, 80
size = 1
img_size = w*h*size
det_size = 3+(30*12)
threshold = 40
rotate_device_list = ["02"]
rotation = 270

print("[I] GAP HIGH")
sleep(1)
GPIO.output(sd, GPIO.HIGH)
sleep(3)

with open('device_id.txt') as f:
    device_id = f.readline().rstrip()

LOOP = 1
while LOOP:
    camera = PiCamera()
    start = time()
    now = datetime.now()
    dt = now.strftime("%Y/%m/%d__%H:%M:%S")
    dtime = now.strftime("%Y%m%d-%H%M%S")

    print(f"[START] {'-'*20} [{dt}]")
    print(f"[I] loop is {args.loop}, sleep is {args.sleep} sec")

    camera.start_preview()

    base_dir = f"data/{dtime}/"
    det_file = f"{base_dir}{dtime}_{device_id}_DET.txt"
    ir_file = f"{base_dir}{dtime}_{device_id}_IR.png"
    rgb_file = f"{base_dir}{dtime}_{device_id}_RGB.jpg"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    ser.flush()
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    print("[TX] TRIGGER")
    GPIO.setup(tr, GPIO.OUT)
    sleep(0.1)
    GPIO.setup(tr, GPIO.IN)

    print("[TX] CALIBRATION")
    ser.write(args.calibration.to_bytes(1, byteorder='little'))

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

    print("[I] GAP LOW")
    GPIO.output(sd, GPIO.LOW)

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
    img.save(ir_file)

    if device_id in rotate_device_list:
        print(f"[I] rotating device: {device_id}")
        rgb_img = Image.open(rgb_file)
        rgb_img = rgb_img.rotate(rotation)
        rgb_img.save(rgb_file)

        ir_img = Image.open(ir_file)
        ir_img = ir_img.rotate(rotation)
        ir_img.save(ir_file)

    end = time()-start
    print(f"[FINISH] {'-'*20} [runtime: {round(end, 2)} sec]", "\n"*2)


    LOOP = args.loop
    sleep(args.sleep)
