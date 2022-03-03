#!/usr/bin/env python3
import os
from picamera import PiCamera


rgb_file = f"test.png"

camera = PiCamera()
camera.start_preview()

camera.capture(rgb_file)

camera.stop_preview()

os.system(f"sshpass -p 1234qwer scp {rgb_file} z@192.168.0.16:~")
os.remove(rgb_file)

print("[I] captured rgb image")
