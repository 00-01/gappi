#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime
import errno
from functools import wraps
import logging
import os
import signal
import threading
import time
import traceback

import cv2
from numpy import asarray
import numpy as np
from picamera import PiCamera
from PIL import Image
from requests import post
import RPi.GPIO as GPIO
import serial
import tensorflow as tf


parser = ArgumentParser()
parser.add_argument("-i", "--inference", default=1, type=int, help="inference location")
parser.add_argument("-s", "--sleep", default=0, type=int, help="loop sleep")
parser.add_argument("-s1", "--sleep1", default=1, type=int, help="loop sleep")
parser.add_argument("-s2", "--sleep2", default=0, type=int, help="loop sleep")
parser.add_argument("-o", "--offset", default=0, type=int, help="offset")
parser.add_argument("-bb", "--bbox", default=0, type=int, help="draw bbox")
parser.add_argument("-b", "--begin", default=7, type=int, help="begin time")
parser.add_argument("-e", "--end", default=23, type=int, help="end time")
parser.add_argument("-in", "--interval", default=20, type=int, help="interval time")
parser.add_argument("-l", "--log", default=1, type=int, help="log_destination")
args = parser.parse_args()

## ---------------------------------------------------------------- BG
BG_LIST = []
BG_LENGTH = 32

## ---------------------------------------------------------------- INFERENCE
HOME = os.path.expanduser('~')
MODEL = f"{HOME}/gappi/model/v1.1.tflite"
THRESHOLD = 0.5

MIN, MAX = 0, 255
NORM_MIN, NORM_MAX = 0, 1
NORM = MAX/2

## ---------------------------------------------------------------- TAKE
SD = 27  # gap power
TR = 17  # ir trigger

W, H = 80, 80
SIZE = 1
IMG_SIZE = W*H*SIZE
DET_SIZE = 3+(30*12)
ROTATION = 180

## ---------------------------------------------------------------- POST
# with open('web_server_address.txt') as f:
#     url = f.readline().rstrip()
# url = 'https://sbrt.mills.co.kr/api/data'
url = 'http://115.68.37.86:8180/api/data'

## ---------------------------------------------------------------- ETC
LOG = args.log
with open(f"{HOME}/device_id.txt") as f:
    device_id = f.readline().rstrip()


class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, seconds)  # used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


def bg_remover(target):
    BG_LIST.insert(0, target)
    if len(BG_LIST) > BG_LENGTH:  BG_LIST.pop(-1)
    else:  pass

    bg = np.zeros([H, W], dtype=int)
    for i in BG_LIST:
        bg += i
    bg //= len(BG_LIST)

    img = target-bg

    # LOW-CUT FILTER
    low = 8
    img[img < low] = 0
    img -= img.min()

    # high = 255
    # img *= high//img.max()
    # img[img > high] = high

    # img = img1 * img
    # img[abs(img) < thresh] = img.min()
    # histogramer(img)

    # bg_img = cv2.cvtColor(bg_img)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2, 2))
    # bg_img = clahe.apply(bg_img)

    fg_img = img.astype(np.uint8)

    return fg_img


def inferencer(input, ):
    print(f"[I] PI INFERENCING", file=log)

    interpreter = tf.lite.Interpreter(model_path=MODEL)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # img = Image.open(input_path).convert('l')  # .resize((80,80))
    # img_arr = np.array(img)
    # img_arr = imread(input, IMREAD_GRAYSCALE)
    input_data = input.reshape(1, input.shape[0], input.shape[1], 1)
    # input_data = img.reshape(1, img.shape[0], img.shape[1], 1)

    ## uint8 to float32 + normalize(-1 to 1)
    if input_data.dtype != 'float32':
        input_data = (np.float32(input_data)-NORM)/NORM  # norm -1 to 1
        # input_data = np.float32(input_data)/MAX # norm 0 to 1

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    # function `get_tensor()` returns copy of tensor data. Use `tensor()`  to get pointer to tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])  # accuacy
    output_data1 = interpreter.get_tensor(output_details[1]['index'])  # location

    ## change output from float32 to uint8
    output_data4 = output_data1*79
    output_data4 = np.around(output_data4, decimals=0).astype(int).tolist()
    output_data4 = output_data4[0]

    flag = 0
    output = []

## ---------------------------------------------------------------- FIXXXXXX
    for outs in output_data:
        for i, out in enumerate(outs):
            if out > THRESHOLD:
                for corner in output_data4[i]:
                    if corner < 0 or corner > H:
                        flag = 1
                        break
                if flag == 0: output.append(output_data4[i])
                flag = 0

    with open(inf_path, 'w') as w:
        w.write(str(len(output)))
        for i in output:
            w.write(f',{i[1]}x{i[0]}x{i[3]}x{i[2]}')

## ---------------------------------------------------------------- FIXXXXXX
    # for outs in output_data:
    #     for i, out in enumerate(outs):
    #         if out > THRESHOLD:
    #             for corner in output_data4[i]:
    #                 if corner < 0 or corner > H:
    #                     flag = 1
    #                     break
    #             if flag == 0:
    #                 if 0 not in output_data4[i]:
    #                     output.append(output_data4[i])
    #                     output.append(f',{output_data4[i,1]}x{output_data4[i,0]}x{output_data4[i,3]}x{output_data4[i,2]}')
    #             flag = 0
    # output.insert(0, str(len(output)))
## ---------------------------------------------------------------- FIXXXXXX
    # li = []
    # for i in output:
        # if 0 not in i:
        # li.append(f',{i[1]}x{i[0]}x{i[3]}x{i[2]}')
    # li.insert(0, str(len(li)))

    # with open(inf_path, 'w') as w:
    #     for i in output:  w.write(i)


@timeout(40)
def taker():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SD, GPIO.OUT)
    GPIO.output(SD, GPIO.LOW)

    GPIO.setup(TR, GPIO.IN)

    ser = serial.Serial(port='/dev/ttyS0',
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=5, )

    start = time.time()
    dt = DT.strftime("%Y/%m/%d__%H:%M:%S")
    print(f"{chr(10)}[START INFERENCE] {'-'*20} [{dt}]", file=log)

    print(f"[I] inference: {args.inference}, sleep: {args.sleep} sec", file=log)

    print(f"[I] GAP HIGH", file=log)
    time.sleep(1)
    GPIO.output(SD, GPIO.HIGH)
    time.sleep(1)

    print("[TX] TRIGGER", file=log)
    GPIO.setup(TR, GPIO.OUT)
    time.sleep(0.1)
    GPIO.setup(TR, GPIO.IN)

    camera = PiCamera()
    camera.start_preview()

    print("[S] CAPTURING RGB", file=log)
    camera.capture(rgb_path)
    camera.stop_preview()
    camera.close()
    # os.system(f"/bin/bash grubFrame.sh {device_id} {dtime}")

    ser.flush()
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    print(f"[TX] CALIBRATION: {args.offset}", file=log)
    # sleep(0.2)
    ser.write(args.offset.to_bytes(2, byteorder='little'))

    print("[RX] INFERENCE", file=log)
    # sleep(0.1)
    rx_det = ser.read()
    while len(rx_det) < (DET_SIZE):
        new_det = ser.read()
        rx_det += new_det

    print("[RX] IMAGE", file=log)
    # sleep(0.1)
    rx_img = ser.readline()
    while len(rx_img) < (IMG_SIZE):
        new_img = ser.read()
        rx_img += new_img

    # print("[RX] IMAGE_2")
    # # sleep(0.1)
    # rx_img = ser.readline()
    # while len(rx_img) < (IMG_SIZE):
    #     new_img = ser.read()
    #     rx_img += new_img

    # print("[TX] THRESHOLD")
    # ser.write(THRESHOLD.to_bytes(2, byteorder='little'))

    print("[I] GAP LOW", file=log)
    GPIO.output(SD, GPIO.LOW)

    print("[I] saving binary to image", file=log)
    ir = Image.frombuffer("L", (W, H), rx_img, 'raw', "L", 0, 1)
    ir.save(ir_path)

    # print(f"[I] rotating device: {device_id}")
    rgb_img = Image.open(rgb_path)
    rgb_img = rgb_img.rotate(ROTATION)

    print(f"[I] CROP RGB", file=log)
    rgb_arr = asarray(rgb_img, dtype='uint8')
    h_rgb, w_rgb, c = rgb_arr.shape
    h_cut, w_cut = 40, 160
    rgb_arr = rgb_arr[h_cut:h_rgb-h_cut, w_cut:w_rgb-w_cut, :]
    rgb_img = Image.fromarray(rgb_arr)
    rgb_img.save(rgb_path)

    ## ---------------------------------------------------------------- BG REMOVE
    print(f"[I] BACKGROUND REMOVE", file=log)
    # ir.save(ir_path)
    # irs = sorted(glob(f'gappi/BG/*.png', recursive=False))
    # os.system(f"rm -rf BG/{irs[0]}")

    ir_arr = asarray(ir)
    error1 = len(ir_arr[ir_arr > 237])
    error2 = len(ir_arr[ir_arr < 1])
    if error1 > 512 or error2 > 512:
        print(f"[!] white-{error1}, black-{error2}", file=log)
        fg_img = np.zeros([H, W], dtype=np.uint8)
    else:
        fg_img = bg_remover(ir_arr)
    cv2.imwrite(fg_path, fg_img)

    ## ---------------------------------------------------------------- INFERENCE
    if args.inference == 1:
        inferencer(fg_img)

    elif args.inference == 0:
        print("[I] gap inference to txt", file=log)
        det = ""
        det_str = rx_det.decode(encoding='UTF-8', errors='ignore')
        with open(inf_path, "w") as file:
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

    ## ----------------------------------------------------------------
    end = time.time()-start
    print(f"[STOP INFERENCE] {'-'*20} [runtime: {round(end, 2)} sec] {chr(10)}", file=log)

    time.sleep(args.sleep)


def poster():
    global r
    start = time.time()
    dt = DT.strftime("%Y/%m/%d__%H:%M:%S")
    print(f"[START POST] {'-'*20} [{dt}]", file=log)

    dtime = DT.strftime("%Y/%m/%d-%H:%M:%S")

    # targets = glob(f'data/*')
    # if len(targets) > 0:
    #     for target in targets:

    with open(inf_path, "r") as file:
        det_data = file.readline().rstrip()
    # with open(log_path, "r") as file:
    #     log_data = file.readline().rstrip()
    log.close()
    data = {"device_id": device_id,
            "predicted": det_data,
            # "log": log,
            }
    files = {"ir_image": open(fg_path, 'rb'),
    # files = {"ir_image": (ir_path, open(ir_path, 'rb'), 'image/png'),
             "rgb_image": open(rgb_path, 'rb'),
             # "fg_image": (fg_path, open(fg_path, 'rb'), 'image/png'),
             "log": open(log_path, 'rb'),
             }
#     log = open(log_path, 'w')
    r = post(url, data=data, files=files)
    # print(r.headers, file=log)
    print(r.text, file=log)

    end = time.time()-start
    print(f"[STOP POST] {'-'*20} [runtime: {round(end, 2)} sec] {chr(10)}", file=log)


def main():
    global DT, base_dir, inf_path, log_path, log, ir_path, rgb_path, fg_path

    hS = 3600
    mS = 60

    START_SEC = args.begin*hS  ## 9:00:00
    END_SEC = args.end*hS  ## 23:00:00
    TOTAL_SEC = 24*hS  ## 24:00:00

    # trd_taker = threading.Thread(target=taker, args=(1,))
    # trd_poster = threading.Thread(target=poster, args=(1,))

    while 1:
        DT = datetime.now()
        H = int(DT.strftime("%H"))
        M = int(DT.strftime("%M"))
        S = int(DT.strftime("%S"))
        W = int(DT.strftime("%w"))
        # H, M, S, W = 23, 59, 59, 6

        dtime = DT.strftime("%Y%m%d-%H%M%S")
        base_dir = f"data/{dtime}/"
        inf_path = f"{base_dir}{dtime}_{device_id}_DET.txt"
        log_path = f"{base_dir}{dtime}_{device_id}_LOG.txt"
        ir_path = f"{base_dir}{dtime}_{device_id}_IR.png"
        rgb_path = f"{base_dir}{dtime}_{device_id}_RGB.jpg"
        fg_path = f"{base_dir}{dtime}_{device_id}_FG.png"

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        if LOG == 1:  log = open(log_path, 'w')
        elif LOG == 0:  log = None
            
        print(f"{r}", file=log)

        D = 0
        if W == 0:  D = TOTAL_SEC
        elif W == 6:  D = TOTAL_SEC*2

        NOW_SEC = (H*hS)+(M*mS)+(S)
        print(f"{chr(10)} {'-'*8} [NOW_TIME: {H}:{M}:{S}, NOW_SEC: {NOW_SEC}] {'-'*8}", file=log)

        D_SEC = NOW_SEC+D
        # print(f'D_SEC: {D_SEC}')

        if START_SEC < D_SEC and D_SEC < END_SEC:
            try:
                # trd_taker.start()
                taker()
            except Exception as e:
                trace_back = traceback.format_exc()
                print(f'[!taker!] {e}{chr(10)}{trace_back}', file=log)
                pass

            try:
                # trd_poster.start()
                poster()
            except Exception as e:
                trace_back = traceback.format_exc()
                print(f'[!poster!] {e}{chr(10)}{trace_back}', file=log)
                pass

            time.sleep(args.interval)

        elif D_SEC < START_SEC or END_SEC < D_SEC:
            sleep_time = TOTAL_SEC-NOW_SEC+START_SEC+D
            print(f'sleep_time: {sleep_time}{chr(10)}', file=log)
            os.system(f"sudo rm -rf data/*")
            time.sleep(sleep_time)

        if LOG == 1:  log.close()
        else:  pass


main()

