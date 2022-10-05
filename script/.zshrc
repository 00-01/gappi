## -------------------------------------------------------------------------------- ALIAS

## ALIAS

alias sz="source ~/.zshrc"
alias z="nano ~/.zshrc"
alias zz="sudo nano ~/.oh-my-zsh/themes/max.zsh-theme "


## APT

alias i="sudo apt install"
alias iy="sudo apt install -y"

alias ua="sudo apt update && sudo apt upgrade && sudo apt autoclean && sudo apt autoremove"
alias u="sudo apt update && sudo apt upgrade"
alias uy="sudo apt update && sudo apt upgrade -y && sudo snap refresh"
alias ud="sudo apt dist-upgrade"
alias uf="sudo apt --fix-broken install"

alias a="sudo apt autoclean && sudo apt autoremove"
alias r="sudo dpkg -r"
alias re="sudo dpkg --configure -a"


## SYS

alias i="sudo apt install"
alias u="sudo apt update && sudo apt upgrade"
alias a="sudo apt autoclean && sudo apt autoremove"
alias r="sudo dpkg -r"

alias reb="sudo reboot now"
alias shd="sudo shutdown now"


## PIP

alias p="pip3 install"


## SYSTEMD

srvc=mvpc.service
s_path="/etc/systemd/system/$srvc"

alias nsd="sudo nano $s_path"

alias sd="sudo systemctl"

alias sdr="sd daemon-reload"
alias sde="sd enable $srvc"
alias sdd="sd disable $srvc"
alias sdt="sd start $srvc"
alias sdp="sd stop $srvc"
alias sds="sd status $srvc"

alias sdss="sdr && sde && sdt"

alias sdl="sudo journalctl -u $srvc -b"
alias sdl_d="sudo journalctl --rotate --vacuum-time=1s"

## -------------------------------------------------------------------------------- ZSH

export python="python3"
export ZSH="/home/$USER/.oh-my-zsh"

ZSH_THEME="max"

plugins=(git zsh-autosuggestions sudo web-search copypath copyfile zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

## UPDATE
DISABLE_UPDATE_PROMPT="true"
export UPDATE_ZSH_DAYS=30
# DISABLE_AUTO_UPDATE="true"

## COMPLETION
ENABLE_CORRECTION="true"
# CASE_SENSITIVE="true"
# make _ and - same : CASE_SENSITIVE must be off
# HYPHEN_INSENSITIVE="true"

## -------------------------------------------------------------------------------- DOWNLOAD ONCE

## ARGCOMPLETE
# pip3 install argcomplete
# activate-global-python-argcomplete
# autoload -U bashcompinit
# bashcompinit

## MANUAL
## zsh-autosuggestions
# git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins$

## zsh-syntax-highlighting
# git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}$


## -------------------------------------------------------------------------------- NOT USED

# sudo chmod 666 /dev/ttyS0
