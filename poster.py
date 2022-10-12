#!/usr/bin/env python3
import os
import traceback
from argparse import ArgumentParser
from datetime import datetime
from glob import glob
from time import sleep

from requests import post


parser = ArgumentParser()
parser.add_argument("-l", "--loop", default=0, type=int, help="run loop")
parser.add_argument("-s1", "--sleep1", default=0, type=int, help="loop sleep")
parser.add_argument("-s2", "--sleep2", default=0, type=int, help="loop sleep")
parser.add_argument("-d", "--delete", default=1, type=int, help="delete sent file")
args = parser.parse_args()
print(f"loop is {args.loop}")
print(f"sleep1 is {args.sleep1} seconds")
print(f"sleep2 is {args.sleep2} seconds")

HOME = os.path.expanduser('~')

with open(f"{HOME}/device_id.txt") as f:
    device_id = f.readline().rstrip()

server_address = f"{HOME}/gappi/network/server_address.txt"
with open(server_address) as f:
    url = f.readline().rstrip()

LOOP = 1
while LOOP:
    now = datetime.now()
    dtime = now.strftime("%Y/%m/%d-%H:%M:%S")
    print(f"posting_time: {dtime}")

    targets = glob(f'data/*')
    if len(targets) < 1:
        print("[!] NO data TO SEND")
        sleep(args.sleep1)
        pass

    for target in targets:
        det = glob(f"{target}/*_DET.txt")
        log = glob(f"{target}/*_LOG.txt")
        ir = glob(f"{target}/*_IR.png")
        fg = glob(f"{target}/*_FG.png")
        rgb = glob(f"{target}/*_RGB.jpg")
        print(det, log, ir, fg, rgb)

        try:
            det, log, ir, fg, rgb = det[0], log[0], ir[0], fg[0], rgb[0]
            print("[I] posting")
            with open(det, "r") as file:
                det_data = file.readline().rstrip()
            data = {"device_id": device_id,
                    "predicted": det_data,
                    }
            files = {"ir_image": open(fg, 'rb'),
                     "raw_image": open(ir, 'rb'),
                     "rgb_image": open(rgb, 'rb'),
                     "log": open(log, 'rb'),
                     # "predicted": open(det_data, 'rb'),
                     }
            r = post(url, data=data, files=files)

            if r.status_code == 200:
                if args.delete:
                    os.system(f"rm -rf {target}")
            # print(r.headers)
            print(r.text)

        except Exception as e:
            trace_back = traceback.format_exc()
            print(f'[!!!] {e}{chr(10)}{trace_back}')
            pass
        os.system(f"rm -rf {target}")

    LOOP = args.loop
    sleep(args.sleep2)
