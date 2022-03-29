# [TIMEZONE]
    sudo cp -p /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# [GIT]
    git clone https://github.com/00-01/gappi.git

### hook
    cd /usr/share/git-core/templates/hooks
    sudo touch post-receive
    sudo chmod u+r+x post-receive

# [CRON]
    */2 9-17 * * 1-5 python3 gappi/main.py > log/main.log && python3 gappi/poster.py > log/poster.log

    ### LOAD TEST
    #@reboot python3 gappi/main.py -l 1 -s 5 > log/main.log
    #@reboot python3 gappi/poster.py -l 1 -s1 10 -s2 5 > log/poster.log

### start cron
    sudo service cron start

#### every 20 seconds
    * * * * * sleep 20: python3 gappi/main.py > log/main.py && python3 gappi/poster.py > log/poster.log
    * * * * * sleep 40: python3 gappi/main.py > log/main.py && python3 gappi/poster.py > log/poster.log
    * * * * * sleep 60: python3 gappi/main.py > log/main.py && python3 gappi/poster.py > log/poster.log

# [zhsrc]
    ## custom alias
    alias sz="source ~/.zshrc"
    alias z="sudo nano ~/.zshrc"
    
    alias i="sudo apt install"
    alias u="sudo apt update && sudo apt upgrade"
    alias a="sudo apt autoclean && sudo apt autoremove"
    alias r="sudo dpkg -r"
    
    alias rb="sudo reboot now"
    alias sd="sudo shutdown now"
    
    alias t="python3 main.py -l 0 -s 0 && python3 poster.py -l 0 -s 0 -d 1"


    ## custom command
    sudo chmod 666 /dev/ttyS0
    cd gappi && git reset --hard && git pull > ../log/git.log
    sudo chmod u+r+x command.sh && ./command.sh && cd

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
