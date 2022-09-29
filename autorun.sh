#!/bin/zsh

PID=$(prgep main_v3.py)
if [ -z "$PID" ]
then
  cd gappi/
  nohup python3 main_v3.py >> ~/log.main.py 2>&1 &
fi
