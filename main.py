from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-t", "--test", default=0, type=int, help="test")
parser.add_argument("-n", "--number", default=0, type=int, help="gateway number")
args = parser.parse_args()

with open('device_id.txt') as f:
    device_id = f.readline().rstrip()

v1 = ["04", "05", "06"]
v2 = ["01", "02", "03", "07"]

# if device_id in operation:
#     os.system(f"/etc/wpa_supplicant/wpa_supplicant.conf gappi/network/SBRT000{args.num}")
# else:
#     os.system(f"/etc/wpa_supplicant/wpa_supplicant.conf gappi/network/test")

if device_id in v1:
    from version import v1
else:
    from version import v2
