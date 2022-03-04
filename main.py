#!/usr/bin/env python3
# from cv2 import imwrite
import os
from struct import unpack
from argparse import ArgumentParser
from datetime import datetime
from time import sleep, time

import RPi.GPIO as GPIO
import numpy as np
import serial
from PIL import Image
from picamera import PiCamera

parser = ArgumentParser()
parser.add_argument("-l", "--loop", default=1, help="run loop")
parser.add_argument("-s", "--sleep", default=1, help="loop sleep")
args = parser.parse_args()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

po = 27  # power
GPIO.setup(po, GPIO.OUT)
GPIO.output(po, GPIO.LOW)

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

    print(f"[START] ---------------- [{dt}]")
    print(f"[I] loop is {args.loop}, sleep is {args.sleep} sec")

    camera.start_preview()

    base_dir = f"data/{dtime}/"
    det_file = f"{base_dir}{dtime}_{device_id}_DET.txt"
    ir_file = f"{base_dir}{dtime}_{device_id}_IR.bin"
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
    # prev_len = -1
    rx_img = ser.readline()
    while len(rx_img) < (img_size):
        new_img = ser.read()
        rx_img += new_img  # current_len = len(rx_img)  # if current_len == prev_len:    # data checker  #     break  # prev_len = current_len

    print("[TX] THRESHOLD")
    ser.write(threshold.to_bytes(4, byteorder='little'))

    print("[S] saving detection in txt")
    det = []
    det_str = rx_det.decode(encoding='UTF-8', errors='ignore')
    with open(det_file, "w") as file:
        det_str = det_str.split(";")
        st = 0
        for i in det_str:
            if "\00" not in i:
                if i is not None:
                    det.append(i)
                    if st != 0:
                        file.write(f",")
                    file.write(f"{i}")
                    st = 1

    print("[S] saving image in bin")
    im_int = unpack('<'+'B'*img_size, rx_img)
    with open(ir_file, "wb") as file:
        for val in im_int:
            file.write(val.to_bytes(2, byteorder='little', signed=1))
    # opening image and remove bytes
    ir_raw = np.fromfile(ir_file, dtype=np.uint16).astype(np.uint8)
    ir_image = np.reshape(ir_raw[:6400], (w, h))

    print("[S] saving image in png")
    im = Image.fromarray(ir_image)
    im.save(f"{ir_img_file}")
    # imwrite(f"{ir_file}.png", ir_image) #cv2

    # check image
    # im = Image.frombuffer('I;16', (w,h), rx_img, 'raw', 'L', 0, 1)

    end = time()-start
    print(f"[FINISH] ---------------- [runtime: {round(end, 2)} sec]", "\n"*2)

    LOOP = args.loop
    sleep(int(args.sleep))
