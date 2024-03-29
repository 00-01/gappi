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
# print(f"loop is {args.loop}")
# print(f"sleep1 is {args.sleep1} seconds")
# print(f"sleep2 is {args.sleep2} seconds")

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
    print(f"{chr(10)}posting_time: {dtime}")

    targets = glob(f'data/*')
    if len(targets) < 1:
        os.system(f'echo "$(($(cat /tmp/connection)+1))" > /tmp/connection')
        print("[!] NO DATA. Connection += 1")
        sleep(args.sleep1)
        pass

    for target in targets:
        det = glob(f"{target}/*_DET.txt")
        log = glob(f"{target}/*_LOG.txt")
        ir = glob(f"{target}/*_IR.png")
        fg = glob(f"{target}/*_FG.png")
        rgb = glob(f"{target}/*_RGB.jpg")
        print(det, log, ir, fg, rgb)

        d, l, i, f, r = len(det), len(log), len(ir), len(fg), len(rgb)

        try:
            with open(det[0], "r") as file:
                det_data = file.readline().rstrip()
            data = {"device_id": device_id,
                    "predicted": det_data,
                    }
            files = {"ir_image": open(fg[0], 'rb'),
                     "raw_image": open(ir[0], 'rb'),
                     "rgb_image": open(rgb[0], 'rb'),
                     "log": open(log[0], 'rb'),
                     # "predicted": open(det_data, 'rb'),
                     }
            r = post(url, data=data, files=files)

            if r.status_code == 200:
                os.system(f"echo 0 > /tmp/connection")
                os.system(f"sudo shutdown -c")
                if args.delete:
                    os.system(f"rm -rf {target}")
            # else: pass
            # print(r.headers)
            print(r.text)

        except Exception as e:
            # base_dir = f"{HOME}/data/{dtime}/"
            # if not os.path.exists(base_dir):  os.makedirs(base_dir)
            os.system(f"mv -f {target} {HOME}/data_backup/")
            trace_back = traceback.format_exc()
            # os.system(f'echo "$(($(cat /tmp/connection)+1))" > /tmp/connection')
            print(f'[!!!] {e} {trace_back}')
            pass

    LOOP = args.loop
    sleep(args.sleep2)
