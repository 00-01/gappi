# from argparse import ArgumentParser

# parser = ArgumentParser()
# parser.add_argument("-t", "--test", default=0, type=int, help="test")
# parser.add_argument("-n", "--number", default=0, type=int, help="gateway number")
# args = parser.parse_args()

'''
image size change from: 1650402076466~1650438017970(index:1100~1715)
'''

# import schedule as schedule


# def main():
with open('../trash/device_id.txt') as f:
    device_id = f.readline().rstrip()

op = ["01", "02", "03", "04", "05", "06", "07", "100"]
dev = []

if device_id in op:
    from version import op
else:
    from version import dev


# schedule.every(30).seconds.do(main())
# main()