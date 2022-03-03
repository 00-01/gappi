#!/usr/bin/env python3
# from cv2 import imwrite
import argparse
import os
import struct
import time
from datetime import datetime
from glob import glob
from PIL import Image

import RPi.GPIO as GPIO
import numpy as np
import serial
from picamera import PiCamera
import requests


# true == 1, false == 0
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--loop", default=1, help="run loop")
parser.add_argument("-s", "--sleep", default=1, help="loop sleep")
parser.add_argument("-d", "--delete", default=1, help="delete sent file")
args = parser.parse_args()


def post_data(dir_name, det_data, ir_file, rgb_file):
    data = {"device_id": device_id,
            "predicted": det_data,
            }
    files = {"ir_image": (ir_file, open(ir_file, 'rb'), 'image/png'),
             "rgb_image": (rgb_file, open(rgb_file, 'rb'), 'image/jpeg')
             # "predicted": (det_file, open(det_file, 'rb'), 'text/plain'),
             }
    r = requests.post(url, data=data, files=files)

    if r.status_code == 200:
        if args.delete:
            os.system(f"rm -rf {dir_name}")
    print(r.headers)

    return r.text

with open('../device_id.txt') as f:
    device_id = f.readline().rstrip()

im_dir = "../data/"

url = 'http://115.68.37.86:8180/api/data'

# set rpi
ser = serial.Serial(port='/dev/ttyS0',
                    baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=None, )

# trigger ir
tr = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(tr, GPIO.OUT)
GPIO.output(tr, GPIO.LOW)
camera = PiCamera()

# set inputs
w, h = 80, 80
size = 1
img_size = w * h * size
det_size = 3 + (30 * 12)
threshold = 40

LOOP = 1
while LOOP:
    now = datetime.now()
    dtime = now.strftime("%Y-%m-%d %H:%M:%S")
    print([dtime])

    print(f"loop is {args.loop}")
    print(f"sleep is {args.sleep} seconds")

    print("-" * 6, "START", "-" * 24)

    camera.start_preview()

    base_dir = f"{im_dir}{dtime}/"
    det_file = f"{base_dir}{dtime}_{device_id}_DET.txt"
    ir_file = f"{base_dir}{dtime}_{device_id}_IR.bin"
    ir_img_file = f"{base_dir}{dtime}_{device_id}_IR.png"
    rgb_file = f"{base_dir}{dtime}_{device_id}_RGB.jpg"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    ser.flush()
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    print("[TX] start signal")
    GPIO.output(tr, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(tr, GPIO.LOW)

    print("[S] capturing rgb image")
    camera.capture(rgb_file)
    camera.stop_preview()
    # os.system(f"/bin/bash grubFrame.sh {device_id} {dtime}")

    print("[RX] detection")
    # rx_det = ser.read(det_size)
    rx_det = ser.read()
    while len(rx_det) < (det_size):
        new_det = ser.read()
        rx_det = rx_det + new_det

    print("[RX] image")
    # rx_img = ser.read(img_size)
    rx_img = ser.read()
    while len(rx_img) < (img_size):
        new_img = ser.read()
        rx_img = rx_img + new_img

    print("[TX] threshold")
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
    im_int = struct.unpack('<' + 'B' * img_size, rx_img)
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

    targets = glob(f'{im_dir}/*')
    if len(targets) < 1:
        break
    for target in targets:
        det = glob(f"{target}/*_DET.txt")
        ir = glob(f"{target}/*_IR.png")
        rgb = glob(f"{target}/*_RGB.jpg")

        try:
            with open(det[0], "r") as file:
                det_data = file.readline().rstrip()
        except IndexError:
            pass

        if len(det) > 0:
            result = post_data(target, det_data, ir[0], rgb[0])
            print(result)

    print("-" * 24, "FINISH", "-" * 6, "\n" * 2)

    time.sleep(int(args.sleep))
    LOOP = args.loop