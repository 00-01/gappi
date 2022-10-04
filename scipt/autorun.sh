#! /bin/zsh

case "$(pidof python3 | wc -w)" in
0)  echo "[RESTART] $(date)" >> ~/log/run.log
    python3 gappi/main_v3.py >> ~/log/main.log
    ;;
1)  # pass
    ;;
*)  echo "[REMOVE] $(date)" >> ~/log/run.log
    kill $(pidof python3 | awk '{print $1}')
    ;;
esac
