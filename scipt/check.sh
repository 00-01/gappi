#!/bin/zsh

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "0: up to date"
elif [ $LOCAL = $BASE ]; then
    echo "1: need pull"
elif [ $REMOTE = $BASE ]; then
    echo "2: need push"
else
    echo "3: diverged"
fi
