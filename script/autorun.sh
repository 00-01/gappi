#! /bin/zsh

LOOP=1
while [LOOP == 1];
do
    NOW=$(date +"%Y %m %d %T")

    cd ~/gappi
    git remote update

    UPSTREAM=${1:-'@{u}'}
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse "$UPSTREAM")
    BASE=$(git merge-base @ "$UPSTREAM")

    if [ $LOCAL = $REMOTE ]; then
        echo "0: PASS"
    else
        echo "1: PULLING"
        cd ~/gappi && git reset --hard && echo "\n[PULL] $NOW" >> ~/log/git.log && git pull >> ~/log/git.log && cd
        crontab ~/gappi/script/cron
        sudo cp -f ~/gappi/script/.zshrc ~/.zshrc
        source ~/gappi/script/command.sh
        sudo cp -f ~/gappi/script/$svc1 $s_path
        sudo cp -f ~/gappi/script/$svc2 /etc/systemd/system/$svc2
        sdss1
        sdss2
        sleep 20
        reb
    fi
    cd

    case "$(pidof python3 | wc -w)" in
    0)  echo "[RESTART] $NOW" >> ~/log/run.log
        sdrf
        ;;
    1)  ;;
    2)  ;;
    *)  echo "[REMOVE] $NOW" >> ~/log/run.log
        kill $(pidof python3 | awk '{print $1}')
        ;;
    esac

    sleep 60
done
