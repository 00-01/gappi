#! /bin/zsh

case "$(pidof python3 | wc -w)" in
0)  echo "Restarting python3: $(date)" >> log/run.log
    python3 gappi/main_v3.py >> log/main.log
    ;;
1)  # all ok
    ;;
*)  echo "Removed double python3: $(date)" >> log/run.log
    kill $(pidof python3 | awk '{print $1}')
    ;;
esac
