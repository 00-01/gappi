## -------------------------------------------------------------------------------- ALIAS

## ZSH
alias sz="source ~/.zshrc"
alias z="nano ~/.zshrc"
alias zz="sudo nano ~/.oh-my-zsh/themes/max.zsh-theme"

## APT
alias at="sudo apt"

alias i="at install"
alias iy="i -y"
alias u="at update && at upgrade"
alias a="at autoclean && at autoremove"
alias ua="u && a"
alias uy="u -y && sudo snap refresh"
alias ud="at dist-upgrade"
alias uf="at --fix-broken install"
alias r="sudo dpkg -r"
alias re="sudo dpkg --configure -a"

## SYS
alias reb="sudo reboot now"
alias shd="sudo shutdown now"


## PIP
alias p="pip3 install"

## SYSTEMD
srvc=mvpc.service
s_path="/etc/systemd/system/$srvc"
alias nsd="sudo nano $s_path"
alias sd="sudo systemctl"

alias sdrl="sd daemon-reload"
alias sdrf="sd reset-failed"
alias sde="sd enable $srvc"
alias sdd="sd disable $srvc"
alias sdt="sd start $srvc"
alias sdp="sd stop $srvc"
alias sds="sd status $srvc"
alias sdss="sdrl && sde && sdt"
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

## zsh-autosuggestions
# git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins$

## zsh-syntax-highlighting
# git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}$

## -------------------------------------------------------------------------------- NOT USED

# sudo chmod 666 /dev/ttyS0
