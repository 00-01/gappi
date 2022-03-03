## cron
### crontab [website](https://crontab.guru/)
#### old
    @reboot sudo chmod 666 /dev/ttyS0 && /usr/bin/python3 main.py
    @reboot /usr/bin/python3 post_requester.py

#### every 5 minutes from 9 to 16
    */5 9-17 * * * python3 main.py >> log/main.log && python3 poster.py >> log/poster.log 2>&1
    
#### every 20 seconds
    * * * * * sleep 20: python3 main.py > log/main.py && python3 poster.py > log/poster.log
    * * * * * sleep 40: python3 main.py > log/main.py && python3 poster.py > log/poster.log
    * * * * * sleep 60: python3 main.py > log/main.py && python3 poster.py > log/poster.log

#### on every reboot
    @reboot python3 main.py > log/main.log
    @reboot python3 poster.py > log/poster.log

### start cron
    sudo service cron start

## timezone
    sudo cp -p /usr/share/zoneinfo/Asia/Seoul /etc/localtime

## zhsrc
    alias t="python3 main.py >> log/main.log && python3 poster.py >> log/poster.log"


## etc
### scp
     scp -r ~/data/* z@192.168.0.16:/media/z/e9503728-f419-4a14-9fc0-21e2947af50c/DATA/gappi
### scp with pw
     sudo sshpass -p 1234qwer scp ~/data/* z@192.168.0.16:/media/z/e9503728-f419-4a14-9fc0-21e2947af50c/DATA/gappi

### change wifi
    sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

