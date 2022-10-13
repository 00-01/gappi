#!/bin/zsh

TMP_FILE=/tmp/check

no_connection() {
    shutdown -r +1 'No internet.'
#    sudo reboot now
}

if ping -c5 google.com; then
    echo 1 > $TMP_FILE
else
    [[ `cat $TMP_FILE` == 0 ]] && no_connection || echo 0 > $TMP_FILE
fi