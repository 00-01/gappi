#!/bin/zsh

cd ~/gappi

git remote update

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "0: PASS"
#elif [ $LOCAL = $BASE ]; then
#    echo "1: PULLING"
#    cd ~/gappi && git reset --hard && echo "[PULL] $(date)" >> ~/log/git.log && git pull >> ~/log/git.log && cd
#    crontab ~/gappi/script/cron
#    cp -f ~/gappi/script/.zshrc ~/.zshrc
#    sudo reboot now
#elif [ $REMOTE = $BASE ]; then
#    echo "2: PUSH NEED"
else
    echo "1: PULLING"
    cd ~/gappi && git reset --hard && echo "\n[PULL] $(date)" >> ~/log/git.log && git pull >> ~/log/git.log && cd
    crontab ~/gappi/script/cron
    cp -f ~/gappi/script/.zshrc ~/.zshrc
    sh ~/gappi/script/command.sh
    rb
fi

cd
