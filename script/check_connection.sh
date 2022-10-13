#!/bin/zsh

TMP_FILE=/tmp/connection

restart() {
    sudo shutdown -r +1 'NO CONNECTION'
}

if (($(cat /tmp/connection) == 10)) then
    echo 0 > $TMP_FILE && restart
else
    :
fi


#if ping -c5 google.com; then
#    echo 1 > $TMP_FILE
#else
#    [[ `cat $TMP_FILE` == 0 ]] && no_connection || echo 0 > $TMP_FILE
#fi
