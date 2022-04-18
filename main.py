# from argparse import ArgumentParser


# parser = ArgumentParser()
# parser.add_argument("-t", "--test", default=0, type=int, help="test")
# parser.add_argument("-n", "--number", default=0, type=int, help="gateway number")
# args = parser.parse_args()

with open('device_id.txt') as f:
    device_id = f.readline().rstrip()

op = ["01", "02", "03", "05"]
dev = ["04", "06", "07"]

if device_id in op:
    from version import op
else:
    from version import dev

'''
TODO: change 04 and 05
'''