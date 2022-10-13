#!/bin/zsh

TMP_FILE=/tmp/connection

restart() {
    sudo shutdown -r now 'No internet.'
}

if cat $TMP_FILE` == 10; then
    echo 0 > $TMP_FILE && restart
fi

#if ping -c5 google.com; then
#    echo 1 > $TMP_FILE
#else
#    [[ `cat $TMP_FILE` == 0 ]] && no_connection || echo 0 > $TMP_FILE
#fi
