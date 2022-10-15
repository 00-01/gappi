#!/bin/zsh

TMP_FILE=/tmp/connection

restart() {
    sudo shutdown -r +5 'NO CONNECTION'
}

if (($(cat $TMP_FILE) >= 9)) then
    echo 0 > $TMP_FILE && restart
else
    cat $TMP_FILE
fi


#if ping -c5 google.com; then
#    echo 1 > $TMP_FILE
#else
#    [[ `cat $TMP_FILE` == 0 ]] && no_connection || echo 0 > $TMP_FILE
#fi
