#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime
from glob import glob
import os
from time import sleep, time

from cv2 import imread, IMREAD_GRAYSCALE
from numpy import asarray
import numpy as np
from picamera import PiCamera
from PIL import Image
import RPi.GPIO as GPIO
import serial
import tensorflow as tf
# from cv2 import Canny, cvtColor, imread, imwrite, resize, warpPerspective, COLOR_BGR2RGB


def taker():
    parser = ArgumentParser()
    parser.add_argument("-l", "--loop", default=0, type=int, help="run loop")
    parser.add_argument("-s", "--sleep", default=0, type=int, help="loop sleep")
    parser.add_argument("-o", "--offset", default=0, type=int, help="offset")
    parser.add_argument("-b", "--box", default=0, type=int, help="draw box")
    parser.add_argument("-i", "--inference", default=1, type=int, help="inference location")
    # parser.add_argument("-t", "--transform", default=0, type=int, help="transform")
    # parser.add_argument("-min", "--min", default=0, type=int, help="min")
    # parser.add_argument("-max", "--max", default=255, type=int, help="max")
    args = parser.parse_args()

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

    W, H = 80, 80
    SIZE = 1
    IMG_SIZE = W*H*SIZE
    DET_SIZE = 3+(30*12)
    THRESHOLD = 0.5
    ROTATION = 180

    print(f"{chr(10)*2}[I] gap HIGH")
    sleep(1)
    GPIO.output(sd, GPIO.HIGH)
    sleep(1)

    with open('trash/device_id.txt') as f:
        device_id = f.readline().rstrip()


    LOOP = 1
    while LOOP:
        print("[TX] TRIGGER")
        GPIO.setup(tr, GPIO.OUT)
        sleep(0.1)
        GPIO.setup(tr, GPIO.IN)

        start = time()
        date = datetime.now()
        dt = date.strftime("%Y/%m/%d__%H:%M:%S")
        dtime = date.strftime("%Y%m%d-%H%M%S")
        print(f"[START] {'-'*20} [{dt}]")
        print(f"[I] inference: {args.inference}, loop: {args.loop}, sleep: {args.sleep} sec")

        camera = PiCamera()
        camera.start_preview()

        base_dir = f"data/{dtime}/"
        det_file = f"{base_dir}{dtime}_{device_id}_DET.txt"
        ir_file = f"{base_dir}{dtime}_{device_id}_IR.png"
        rgb_file = f"{base_dir}{dtime}_{device_id}_RGB.jpg"
        ir_path = f"gappi/BG/{date}.png"
        # boxed_file = f"{base_dir}{dtime}_{device_id}_BOX.png"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        print("[S] CAPTURING RGB")
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

        print("[RX] INFERENCE")
        # sleep(0.1)
        rx_det = ser.read()
        while len(rx_det) < (DET_SIZE):
            new_det = ser.read()
            rx_det += new_det

        print("[RX] IMAGE")
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

        print("[I] gap LOW")
        GPIO.output(sd, GPIO.LOW)

        print("[I] saving binary to image")
        img = Image.frombuffer("L", (W, H), rx_img, 'raw', "L", 0, 1)
        img.save(ir_file)

        # print(f"[I] rotating device: {device_id}")
        rgb_img = Image.open(rgb_file)
        rgb_img = rgb_img.rotate(ROTATION)

        print(f"[I] CROP RGB")
        rgb_arr = asarray(rgb_img, dtype='uint8')
        h_rgb, w_rgb, c = rgb_arr.shape
        h_cut, w_cut = 40, 160
        rgb_arr = rgb_arr[h_cut:h_rgb-h_cut, w_cut:w_rgb-w_cut, :]
        rgb_img = Image.fromarray(rgb_arr)
        rgb_img.save(rgb_file)

        # ir_img = Image.open(ir_file)
        # ir_img = ir_img.rotate(ROTATION)
        # ir_img.save(ir_file)

        ## ---------------------------------------------------------------- BG REMOVE

        # print(f"[I] BACKGROUND REMOVE")
        # img.save(ir_path)
        # irs = sorted(glob(f'gappi/BG/*.png', recursive=False))
        # os.system(f"rm -rf BG/{irs[0]}")
        #
        # error1 = len(img[img > 237])
        # error2 = len(img[img < 1])
        # if error1 > 512 or error2 > 256:
        #     log(f"{i}: white-{error1}, black-{error2}")
        #     return 0
        # else:
        #     # log(f"{i}: white-{error1}, black-{error2}")
        #     bgq.insert(0, img)
        #     if len(bgq) > bgq_length:  bgq.pop(-1)
        #     else:  pass
        #     bg = bg_filter(img)
        #     return 1, bg
        #
        #
        # irs = irs[:32]

        ## ---------------------------------------------------------------- INFERENCE

        if args.inference == 1:
            print(f"[I] PI INFERENCING")
            model_path = "gappi/model/v1.1.tflite"

            MIN, MAX = 0, 255
            NORM_MIN, NORM_MAX = 0, 1
            NORM = MAX/2

            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()

            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # img = Image.open(input_path).convert('l')  # .resize((80,80))
            img_arr = imread(ir_file, IMREAD_GRAYSCALE)
            # img_arr = np.array(img)
            input_data = img_arr.reshape(1, img_arr.shape[0], img_arr.shape[1], 1)
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
            for outs in output_data:
                for i, out in enumerate(outs):
                    if out > THRESHOLD:
                        for corner in output_data4[i]:
                            if corner < 0 or corner > H:
                                flag = 1
                                break
                        if flag == 0: output.append(output_data4[i])
                        flag = 0

            with open(det_file, 'w') as w:
                w.write(str(len(output)))
                for i in output:
                    w.write(f',{i[1]}x{i[0]}x{i[3]}x{i[2]}')

        elif args.inference == 0:
            print("[I] gap inference to txt")
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

        ## ----------------------------------------------------------------

        end = time()-start
        print(f"[FINISH] {'-'*20} [runtime: {round(end, 2)} sec] {chr(10)}")

        LOOP = args.loop
        sleep(args.sleep)

