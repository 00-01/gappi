#!/usr/bin/env python3
import serial


ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=10, )

cal = 39612

ser.write(cal.to_bytes(4, byteorder='little'))
