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
parser.add_argument("-o", "--offset", default=0, type=int, help="offset")
parser.add_argument("-b", "--box", default=0, type=int, help="draw box")
parser.add_argument("-min", "--min", default=0, type=int, help="min")
parser.add_argument("-max", "--max", default=255, type=int, help="max")
# parser.add_argument("-scp", "--scp", default=0, help="save to scp")
args = parser.parse_args()

# host = "192.168.0.5"
# username = "z"
# password = ""
# save_dir = "/home/z/MVPC10/DATA/"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sd = 27  # gap power
GPIO.setup(sd, GPIO.OUT)
GPIO.output(sd, GPIO.LOW)

tr = 17  # ir trigger
GPIO.setup(tr, GPIO.IN)

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
rotation = 270

print("[I] GAP HIGH")
sleep(1)
GPIO.output(sd, GPIO.HIGH)
sleep(2)

with open('device_id.txt') as f:
    device_id = f.readline().rstrip()

LOOP = 1
while LOOP:
    print("[TX] TRIGGER")
    GPIO.setup(tr, GPIO.OUT)
    sleep(0.1)
    GPIO.setup(tr, GPIO.IN)

    start = time()
    now = datetime.now()
    dt = now.strftime("%Y/%m/%d__%H:%M:%S")
    dtime = now.strftime("%Y%m%d-%H%M%S")
    print(f"[START] {'-'*20} [{dt}]")
    print(f"[I] loop: {args.loop}, sleep: {args.sleep} sec")

    camera = PiCamera()
    camera.start_preview()

    base_dir = f"data/{dtime}/"
    det_file = f"{base_dir}{dtime}_{device_id}_DET.txt"
    ir_file = f"{base_dir}{dtime}_{device_id}_IR.png"
    rgb_file = f"{base_dir}{dtime}_{device_id}_RGB.jpg"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    print("[S] capturing rgb image")
    camera.capture(rgb_file)
    camera.stop_preview()
    camera.close()
    # os.system(f"/bin/bash grubFrame.sh {device_id} {dtime}")

    ser.flush()
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    print(f"[TX] CALIBRATION: {args.offset}")
    # sleep(0.2)
    ser.write(args.offset.to_bytes(2, byteorder='little'))

    print("[RX] DETECTION")
    # sleep(0.1)
    rx_det = ser.read()
    while len(rx_det) < (det_size):
        new_det = ser.read()
        rx_det += new_det
        # print(len(rx_det))

    print("[RX] IMAGE_1")
    # sleep(0.1)
    rx_img = ser.readline()
    while len(rx_img) < (img_size):
        new_img = ser.read()
        rx_img += new_img
        # print(len(rx_img))

    # print("[RX] IMAGE_2")
    # # sleep(0.1)
    # rx_img = ser.readline()
    # while len(rx_img) < (img_size):
    #     new_img = ser.read()
    #     rx_img += new_img

    # print("[TX] THRESHOLD")
    # ser.write(threshold.to_bytes(2, byteorder='little'))

    print("[I] GAP LOW")
    GPIO.output(sd, GPIO.LOW)

    print("[I] saving detection to txt")
    det = ""
    det_str = rx_det.decode(encoding='UTF-8', errors='ignore')
    with open(det_file, "w") as file:
        det_str = det_str.split(";")
        st = 0
        for i in det_str:
            if 0 < len(i) < 12 and "\00" not in i:
                if st != 0:
                    file.write(f",")
                    det += ","
                file.write(f"{i}")
                det += i
                st = 1
            else: break

    print("[I] saving binary to image")
    img = Image.frombuffer("L", (w, h), rx_img, 'raw', "L", 0, 1)
    img.save(ir_file)

    if args.box == 1:
        print("[I] draw bbox")
        from matplotlib import cm
        from matplotlib.patches import Rectangle
        from matplotlib.pyplot import subplots
        from io import BytesIO
        from numpy import asarray
        with open(det_file, "r") as file:
            det_data = file.readline().rstrip()
        if len(det_data) > 2:
            img = Image.open(ir_file)
            box = det_data.split(",")
            box = box[1:]
            fig, ax = subplots()
            ax.imshow(img, cmap=cm.magma, vmin=args.min, vmax=args.max,)
            for i in box:
                i = i.split('x')
                rect = Rectangle((int(i[0]), int(i[1])), int(i[2]), int(i[3]), edgecolor='w', facecolor="none")
                ax.add_patch(rect)
                ax.axis('off')
            img_buf = BytesIO()
            fig.savefig(img_buf, format='png')
            im = Image.open(img_buf)
            arr = asarray(im, dtype='uint8')
            w1, h1, c1 = arr.shape
            w2, h2 = 60, 140
            arr = arr[w2:w1-w2, h2:h1-h2, :]
            im = Image.fromarray(arr)
            im.save(ir_file)

    print(f"[I] rotating device: {device_id}")
    rgb_img = Image.open(rgb_file)
    rgb_img = rgb_img.rotate(rotation)
    rgb_img.save(rgb_file)

    ir_img = Image.open(ir_file)
    ir_img = ir_img.rotate(rotation)
    ir_img.save(ir_file)

    rotated_det = ""
    det = det.split(",")
    rotated_det += f"{det[0]},"
    for i in det[1:]:
        i = i.split("x")
        i[0], i[1] = int(i[0]), int(i[1])
        # x, y = w-1-int(i[0]), h-1-int(i[1])
        rotated_det += f"{w-1-i[1]}x{i[0]}x{i[2]}x{i[3]},"
    with open(det_file, "w") as file:
        file.write(rotated_det[:-1])

    end = time()-start
    print(f"[FINISH] {'-'*20} [runtime: {round(end, 2)} sec]", "\n"*2)

    # if args["scp"]:
    #     print("uploading to server")
    #     os.system(f"sshpass -p {password} scp -r {im_dir}* {username}@{host}:{save_dir}")

    LOOP = args.loop
    sleep(args.sleep)
