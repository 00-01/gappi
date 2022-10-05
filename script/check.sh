#!/bin/zsh

cd ~/gappi

git remote update

NOW=$(date +"%Y %m %d %T")

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
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
