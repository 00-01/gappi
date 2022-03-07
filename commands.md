# TIMEZONE
    sudo cp -p /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# GIT
    git clone https://github.com/00-01/gappi.git

# CRON
    @reboot cd gappi && git pull && cd && python3 gappi/gap/restart.py

    ### SCHEDULING
    */1 9-17 * * 1-5 python3 gappi/main.py > log/main.log && python3 gappi/poster.py > log/poster.log
    #*/1 9-17 * * 1-5 python3 gappi/gap/low.py && python3 gappi/main.py > log/main.log && \
    #python3 gappi/poster.py > log/poster.log && gappi/gap/high.py
    ### */1 * * * 1-5 sudo chmod 666 /dev/ttyS0 && cd /home/pi/scripts/ && /usr$

    ### LOAD TEST
    #@reboot python3 gappi/main.py -l 1 -s 5 > log/main.log
    #@reboot python3 gappi/poster.py -l 1 -s1 10 -s2 5 > log/poster.log

### start cron
    sudo service cron start

#### every 20 seconds
    * * * * * sleep 20: python3 gappi/main.py > log/main.py && python3 gappi/poster.py > log/poster.log
    * * * * * sleep 40: python3 gappi/main.py > log/main.py && python3 gappi/poster.py > log/poster.log
    * * * * * sleep 60: python3 gappi/main.py > log/main.py && python3 gappi/poster.py > log/poster.log
#### old
    @reboot sudo chmod 666 /dev/ttyS0 && /usr/bin/python3 main.py
    @reboot /usr/bin/python3 post_requester.py

## zhsrc
    alias t="python3 gappi/main.py > log/main.log && python3 gappi/poster.py > log/poster.log"

## etc
### scp
     scp -r ~/data/* z@192.168.0.16:/media/z/e9503728-f419-4a14-9fc0-21e2947af50c/DATA/gappi
### scp with pw
     sudo sshpass -p 1234qwer scp ~/data/* z@192.168.0.16:/media/z/e9503728-f419-4a14-9fc0-21e2947af50c/DATA/gappi
### change_wifi
    sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

