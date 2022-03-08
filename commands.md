# [TIMEZONE]
    sudo cp -p /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# [GIT]
    git clone https://github.com/00-01/gappi.git

# [CRON]
    @reboot python3 gappi/gap/restart.py

    ### SCHEDULING
    # */1 9-17 * * 1-5 python3 gappi/main.py > log/main.log && python3 gappi/poster.py > log/poster.log
    
    */10 9-17 * * 1-5  python3 gappi/gap/low.py && python3 gappi/main.py > log/main.log && \
    python3 gappi/poster.py > log/poster.log && python3 gappi/gap/high.py

    ### */1 * * * 1-5 sudo chmod 666 /dev/ttyS0 && cd /home/pi/scripts/ && /usr$

    ### LOAD TEST
    #@reboot python3 gappi/main.py -l 1 -s 5 > log/main.log
    #@reboot python3 gappi/poster.py -l 1 -s1 10 -s2 5 > log/poster.log

    ### GAP POWER
    5 18 * * * python3 gappi/gap/high.py
    55 8 * * * python3 gappi/gap/low.py


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
    ## custom alias
    alias sz="source ~/.zshrc"
    alias z="sudo nano ~/.zshrc"
    
    alias i="sudo apt install"
    alias u="sudo apt update && sudo apt upgrade && sudo snap refresh"
    alias a="sudo apt autoclean && sudo apt autoremove"
    alias r="sudo dpkg -r"
    
    alias n="sudo nano"
    
    alias rb="sudo reboot now"
    alias sd="sudo shutdown now"
    
    alias t="python3 main.py -l 0 -s 0 && python3 poster.py -l 0 -s 0 -d 1"


    ## custom command
    sudo chmod 666 /dev/ttyS0
    cd gappi && git pull && cd

## etc
### scp
     scp -r ~/data/* z@192.168.0.16:/media/z/e9503728-f419-4a14-9fc0-21e2947af50c/DATA/gappi
### scp with pw
     sudo sshpass -p 1234qwer scp ~/data/* z@192.168.0.16:/media/z/e9503728-f419-4a14-9fc0-21e2947af50c/DATA/gappi
### change_wifi
    sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# [SLEEP]
    ## wake up tomorrow at 08:55
    sudo rtcwake -m disk
    sudo rtcwake -m no -l -t $(date +%s -d 'tomorrow 08:55')

### help
    rtcwake [options] [-d device] [-m standby_mode] {-s seconds|-t time_t}

### switch to local time
    sudo timedatectl set-local-rtc 1

    