#! /bin/zsh

NOW=$(date +"%Y %m %d %T")

case "$(pidof python3 | wc -w)" in
0)  echo "[RESTART] $NOW" >> ~/log/run.log
    python3 ~/gappi/main_v3.py >> ~/log/main.log
    ;;
1)  # pass
    ;;
*)  echo "[REMOVE] $NOW" >> ~/log/run.log
    kill $(pidof python3 | awk '{print $1}')
    ;;
esac
