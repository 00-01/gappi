from datetime import datetime
import time

import post
import take


hS = 3600
mS = 60

INTERVAL = 20

START_SEC = 9*hS  ## 9:00:00
END_SEC = 18*hS  ## 18:00:00
TOTAL_SEC = 24*hS  ## 24:00:00


while 1:
    DT = datetime.now()
    H = int(DT.strftime("%H"))
    M = int(DT.strftime("%M"))
    S = int(DT.strftime("%S"))
    W = int(DT.strftime("%w"))
    # H, M, S, W = 23, 59, 59, 6

    D = 0
    if W == 0:  D = TOTAL_SEC
    elif W == 6:  D = TOTAL_SEC*2

    NOW_SEC = (H*hS) +(M*mS) +(S)
    print(f'NOW_SEC: {NOW_SEC}')

    D_SEC = NOW_SEC + D
    # print(f'D_SEC: {D_SEC}')

    if START_SEC < D_SEC and D_SEC < END_SEC:
        take.taker()
        post.poster()

        time.sleep(INTERVAL)

    elif D_SEC < START_SEC or END_SEC < D_SEC:
        sleep_time = TOTAL_SEC -NOW_SEC +START_SEC +D
        print(f'sleep_time: {sleep_time}{chr(10)}')
        time.sleep(sleep_time)

