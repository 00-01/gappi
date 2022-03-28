

with open("Calibration.bin", "rb") as cal:
    r = cal.read()

print(r)



# import struct
#
# data = open("Calibration.bin", "rb").read()
# d1 = struct.unpack("H", data)
# print(d1)