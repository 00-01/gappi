#! /bin/zsh

NOW=$(date +"%Y %m %d %T")

case "$(pidof python3 | wc -w)" in
0)  echo "[RESTART] $NOW" >> ~/log/run.log

    cd ~/gappi
    git remote update

    UPSTREAM=${1:-'@{u}'}
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse "$UPSTREAM")
    BASE=$(git merge-base @ "$UPSTREAM")
    if [ $LOCAL = $REMOTE ]; then
        sdrs
        echo "0: PASS"
    #elif [ $LOCAL = $BASE ]; then
    #    echo "1: PULLING"
    #    cd ~/gappi && git reset --hard && echo "[PULL] $NOW" >> ~/log/git.log && git pull >> ~/log/git.log && cd
    #    crontab ~/gappi/script/cron
    #    cp -f ~/gappi/script/.zshrc ~/.zshrc
    #    sudo reboot now
    #elif [ $REMOTE = $BASE ]; then
    #    echo "2: PUSH NEED"
    else
        echo "1: PULLING"
        cd ~/gappi && git reset --hard && echo "\n[PULL] $NOW" >> ~/log/git.log && git pull >> ~/log/git.log && cd
        crontab ~/gappi/script/cron
        sudo cp -f ~/gappi/script/.zshrc ~/.zshrc
        sh ~/gappi/script/command.sh
        sudo cp -f ~/gappi/script/$srvc $s_path
        sdss
        sleep 2
        reb
    fi
    cd
    ;;
1)  # pass
    ;;
*)  echo "[REMOVE] $NOW" >> ~/log/run.log

    kill $(pidof python3 | awk '{print $1}')
    ;;
esac
