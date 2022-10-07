## [TIMEZONE]
    sudo cp -p /usr/share/zoneinfo/Asia/Seoul /etc/localtime


## [GIT]
    git clone https://github.com/00-01/gappi.git

### hook
    cd /usr/share/git-core/templates/hooks
    sudo touch post-receive
    sudo chmod u+r+x post-receive


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
    scp -r data/* z@192.168.0.5:~/data

### scp with pw
    sshpass -p PWPWPW scp -r data/* z@192.168.0.5:~/data

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
