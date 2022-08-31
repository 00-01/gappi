#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime
from glob import glob
from os import system
from time import sleep

from requests import post


def poster():
    parser = ArgumentParser()
    parser.add_argument("-l", "--loop", default=0, type=int, help="run loop")
    parser.add_argument("-s1", "--sleep1", default=0, type=int, help="loop sleep")
    parser.add_argument("-s2", "--sleep2", default=0, type=int, help="loop sleep")
    parser.add_argument("-d", "--delete", default=1, type=int, help="delete sent file")
    # parser.add_argument("-scp", "--scp", default=0, help="save to scp")
    args = parser.parse_args()

    print(f"loop is {args.loop}")
    print(f"sleep1 is {args.sleep1} seconds")
    print(f"sleep2 is {args.sleep2} seconds")

    with open('device_id.txt') as f:
        device_id = f.readline().rstrip()

    # with open('web_server_address.txt') as f:
    #     url = f.readline().rstrip()
    url = 'http://115.68.37.86:8180/api/data'
    # url = 'https://sbrt.mills.co.kr/api/data'

    # host = "192.168.0.5"
    # username = "z"
    # password = ""
    # save_dir = "~/data/gappi"

    def post_data(dir_name, det_data, ir_file, rgb_file):
        data = {"device_id": device_id,
                "predicted": det_data,
                }
        files = {"ir_image": (ir_file, open(ir_file, 'rb'), 'image/png'),
                 "rgb_image": (rgb_file, open(rgb_file, 'rb'), 'image/jpeg')
                 # "predicted": (det_file, open(det_file, 'rb'), 'text/plain'),
                 }
        r = post(url, data=data, files=files)

        # if r.status_code == 200:
        #     if args.delete:
        #         system(f"rm -rf {dir_name}")
        print(r.headers)

        return r.text


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
            ir = glob(f"{target}/*_IR.png")
            rgb = glob(f"{target}/*_RGB.jpg")

            try:
                det, ir, rgb = det[0], ir[0], rgb[0]
                print("[I] posting")
                with open(det, "r") as file:
                    det_data = file.readline().rstrip()
                ## post
                result = post_data(target, det_data, ir, rgb)
                print(result)
            except IndexError as e:
                print(f"[!] {e.args}")
                pass
            # system(f"rm -rf {target}")

        # if args["scp"]:  #     print("uploading to server")  #     os.system(f"sshpass -p {password} scp -r {im_dir}* {username}@{host}:{save_dir}")

        LOOP = args.loop
        sleep(args.sleep2)
