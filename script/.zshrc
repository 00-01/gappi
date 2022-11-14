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
alias sd="sudo systemctl"

alias sdrl="sd daemon-reload"
alias sdrf="sd reset-failed"

alias sde="sd enable"
alias sdd="sd disable"
alias sdt="sd start"
alias sdp="sd stop"
alias sds="sd status"

alias sdl="sudo journalctl -u"
alias sdl_d="sudo journalctl --rotate --vacuum-time=1s"

export svc1=mvpc.service
export svc2=update.service
export s_path="/etc/systemd/system/$svc1"
alias sde1="sd enable $svc1"
alias sdd1="sd disable $svc1"
alias sdt1="sd start $svc1"
alias sdp1="sd stop $svc1"
alias sds1="sd status $svc1"
alias sdl1="sudo journalctl -u $srvc -b"

alias sdss1="sdrl && sde $svc1 && sdt $svc1"
alias sdss2="sdrl && sde $svc2 && sdt $svc2"

alias nsd="sudo nano $s_path"

## -------------------------------------------------------------------------------- ZSH

export PATH="$HOME/.local/bin:$PATH"
export python="python3"
export ZSH=$HOME/.oh-my-zsh

ZSH_THEME="max"

plugins=(git zsh-autosuggestions zsh-syntax-highlighting sudo web-search copypath copyfile)

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

## -------------------------------------------------------------------------------- PLUGINS

# git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions
# git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
# git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
# pip3 install argcomplete
# activate-global-python-argcomplete
# autoload -U bashcompinit
# bashcompinit

## -------------------------------------------------------------------------------- NOT USED

# sudo chmod 666 /dev/ttyS0

