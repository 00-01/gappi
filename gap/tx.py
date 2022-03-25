#!/usr/bin/env python3

import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
)

threshold = 40

print("TX: threshold")
ser.write(threshold.to_bytes(4, byteorder='little'))
ser.flush()
ser.reset_output_buffer()
