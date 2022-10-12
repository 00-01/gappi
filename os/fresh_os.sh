#### ---------------------------------------------------------------- SYSTEM
mkdir data log
cp -rf ~/gappi/os/log/* ~/log
cp -f ~/gappi/os/device_id.txt ~/device_id.txt
cp -f ~/gappi/os/max.zsh-theme ~/.oh-my-zsh/themes/max.zsh-theme
cp -f ~/gappi/network/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

crontab ~/gappi/script/cron

sudo cp -f ~/gappi/script/.zshrc ~/.zshrc
source .zshrc

source ~/gappi/script/command.sh

sudo cp -f ~/gappi/script/$srvc $s_path
sdss

#### ---------------------------------------------------------------- INSTALL
iy cmake net-tools nmap
iy build-essential cmake pkg-config protobuf-compiler python3-dev
iy libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 python3-pyqt5 libatlas-base-dev libjasper-dev libjpeg-dev libtiff5-dev libpng12-dev gfortran libc-ares-dev libeigen3-dev libopenblas-dev libblas-dev liblapack-dev libpq-dev
iy libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev

#python3 -m pip install -U pip3
p -U pip\
 setuptools wheel cython pybind11 h5py gdown pillow setuptools matplotlib opencv-python\
 tensorflow numpy==1.21.4

# pyserial picamera rpi.gpio

#### ---------------------------------------------------------------- ZSH
p argcomplete
activate-global-python-argcomplete
autoload -U bashcompinit
bashcompinit
git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

#### ---------------------------------------------------------------- RPI
#sudo lsof /dev/ttyS0
