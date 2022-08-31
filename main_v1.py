# from argparse import ArgumentParser
import time

import schedule

import post
import take


# parser = ArgumentParser()
# parser.add_argument("-in", "--interval", default=30, type=int, help="interval")
# parser.add_argument("-sl", "--sleep", default=1, type=int, help="sleep")
# args = parser.parse_args()

# schedule.every(args.interval).seconds.do(take.taker)
# schedule.every(args.interval).seconds.do(post.poster)
schedule.every(20).seconds.do(take.taker)
schedule.every(20).seconds.do(post.poster)

while 1:
    schedule.run_pending()
    time.sleep(0.1)
    # time.sleep(args.sleep)
