#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime
from glob import glob
from os import system
from time import sleep

from matplotlib import image, patches, pyplot
from requests import post


parser = ArgumentParser()
parser.add_argument("-l", "--loop", default=0, type=int, help="run loop")
parser.add_argument("-s1", "--sleep1", default=0, type=int, help="loop sleep")
parser.add_argument("-s2", "--sleep2", default=0, type=int, help="loop sleep")
parser.add_argument("-d", "--delete", default=1, type=int, help="delete sent file")
parser.add_argument("-b", "--box", default=0, type=int, help="draw box")
# parser.add_argument("-scp", "--scp", default=0, help="save to scp")
args = parser.parse_args()

print(f"loop is {args.loop}")
print(f"sleep1 is {args.sleep1} seconds")
print(f"sleep2 is {args.sleep2} seconds")

with open('device_id.txt') as f:
    device_id = f.readline().rstrip()

url = 'http://115.68.37.86:8180/api/data'


# host = "192.168.0.5"
# username = "z"
# password = ""
# save_dir = "~/DATA/gappi"

def post_data(dir_name, det_data, ir_file, rgb_file):
    data = {"device_id": device_id,
            "predicted": det_data,
            }
    files = {"ir_image": (ir_file, open(ir_file, 'rb'), 'image/png'),
             "rgb_image": (rgb_file, open(rgb_file, 'rb'), 'image/jpeg')# "predicted": (det_file, open(det_file, 'rb'), 'text/plain'),
             }
    r = post(url, data=data, files=files)

    if r.status_code == 200:
        if args.delete:
            system(f"rm -rf {dir_name}")
    print(r.headers)

    return r.text


LOOP = 1
while LOOP:
    now = datetime.now()
    dtime = now.strftime("%Y%m%d-%H%M%S")
    print([dtime])

    targets = glob(f'data/*')
    if len(targets) < 1:
        print("[!] NO DATA TO SEND")
        sleep(args.sleep1)
        pass

    for target in targets:
        det = glob(f"{target}/*_DET.txt")
        ir = glob(f"{target}/*_IR.png")
        rgb = glob(f"{target}/*_RGB.jpg")
        det, ir, rgb = det[0], ir[0], rgb[0]

        try:
            print("[I] posting")
            with open(det, "r") as file:
                det_data = file.readline().rstrip()
        # # bbox
        #     if args.box==1:
        #         if len(det_data)>2:
        #             img = image.imread(ir)
        #             box = det_data.split(",")
        #             box = box[1:]
        #             fig, ax = pyplot.subplots()
        #             ax.imshow(img)
        #             for i in box:
        #                 i = i.split('x')
        #                 rect = patches.Rectangle((int(i[0]), int(i[1])), int(i[2]), int(i[3]), edgecolor='w', facecolor="none")
        #                 ax.add_patch(rect)
        #                 # print(rect)
        #             fig.savefig(ir)
            # post
            result = post_data(target, det_data, ir, rgb)
            print(result)
        except IndexError as e:
            print(f"[!] {e.args}")
            pass

        # if args["scp"]:  #     print("uploading to server")  #     os.system(f"sshpass -p {password} scp -r {im_dir}* {username}@{host}:{save_dir}")

    LOOP = args.loop
    sleep(args.sleep2)
