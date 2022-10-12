#### ---------------------------------------------------------------- PIP
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl zsh cmake net-tools nmap
sudo apt install -y build-essential cmake pkg-config protobuf-compiler python3-dev
sudo apt install -y libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 python3-pyqt5 libatlas-base-dev libjasper-dev libjpeg-dev libtiff5-dev libpng12-dev gfortran libc-ares-dev libeigen3-dev libopenblas-dev libblas-dev liblapack-dev libpq-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev

python3 -m pip install -U pip3

pip3 install -U pip3\
 setuptools wheel cython pybind11 h5py gdown pillow setuptools matplotlib opencv-python\
 tensorflow numpy==1.21.4

#### ---------------------------------------------------------------- ZSH

sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
pip3 install argcomplete
activate-global-python-argcomplete
autoload -U bashcompinit
bashcompinit

#### ----------------------------------------------------------------

rm -rf *
mkdir data log
cp -r ~/gappi/os/log/* ~/log
cp -f ~/gappi/os/device_id.txt ~/device_id.txt
source .zshrc
