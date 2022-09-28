## [TIMEZONE]
    sudo cp -p /usr/share/zoneinfo/Asia/Seoul /etc/localtime

## [GIT]
    git clone https://github.com/00-01/gappi.git

### hook
    cd /usr/share/git-core/templates/hooks
    sudo touch post-receive
    sudo chmod u+r+x post-receive

## [CRON]
    @reboot sudo chmod 666 /dev/ttyS0
    @reboot cd gappi && git reset --hard && git pull > ../log/git.log && sudo chmod u+r+x command.sh && cd
    
    @reboot python3 gappi/main_v3.py > log/main.log
    
    30 18 * * 1-5 sudo shutdown now -r
    
    0 19 * * 1-5 sudo rm -rf data/*
    @daily sudo rm -rf data/*

### start cron
    sudo service cron start

## [ZSHRC]
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

## [TENSORFLOW]

## swap memory
### swap size check
    free -h

### stop swap service && open config file
    sudo /etc/init.d/dphys-swapfile stop
    sudo nano /etc/dphys-swapfile
    
    ## change size
    # CONF_SWAPSIZE=2048

### start swap service
    sudo /etc/init.d/dphys-swapfile start

### INSTALL
    sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 \
    libatlas-base-dev libjasper-dev gfortran libc-ares-dev libeigen3-dev libopenblas-dev libblas-dev liblapack-dev \
    cython protobuf-compiler python3-dev libpq-dev

    python3 -m pip install -U pip3
    pip3 install -U setuptools pip
    pip3 install pybind11 h5py gdown matplotlib pillow opencv-contrib-python protobuf==3.20.0 tensorflow

## [ETC]

### scp
    scp -r data/*/*_BG.png z@192.168.0.5:~/data

### scp with pw
    sudo sshpass -p 1234qwer scp ~/data/* z@192.168.0.16:/media/z/0/DATA/gappi

### change_wifi
    sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

## [SLEEP]
    ## wake up tomorrow at 08:55
    sudo rtcwake -m disk
    sudo rtcwake -m no -l -t $(date +%s -d 'tomorrow 08:55')

### help
    rtcwake [options] [-d device] [-m standby_mode] {-s seconds|-t time_t}

### switch to local time
    sudo timedatectl set-local-rtc 1



## [MAC ADDRESS]

## temporary
### show ip & mac address
    ip address show
### change mac address
    sudo ip link set dev <wlan0> down
    sudo ip link set dev <wlan0> address <00:00:00:00:00:01>
    sudo ip link set dev <wlan0> up

## permanent
    sudo apt install macchanger
    
### random
    sudo macchanger -r <wlan0>
### specific
    sudo macchanger -m <00:00:00:00:00:01> <wlan0>





