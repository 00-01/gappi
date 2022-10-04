#!/bin/zsh

git remote update

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "0: up to date"
elif [ $LOCAL = $BASE ]; then
    echo "1: need pull"
    cd ~/gappi && git reset --hard && git pull >> ~/log/git.log && echo "$(date)" >> ~/log/git.log && cd
    rb
#elif [ $REMOTE = $BASE ]; then
#    echo "2: need push"
else
    echo "2: etc"
#    echo "3: diverged"
fi
