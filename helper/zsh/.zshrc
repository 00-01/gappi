## -------------------------------------------------------------------------------- MVPC

sudo chmod 666 /dev/ttyS0
#cd gappi && git reset --hard && git pull > ../log/git.log
#sudo chmod u+r+x command.sh && ./command.sh && cd

alias run="python3 main_v3.py"

## -------------------------------------------------------------------------------- ZSH

export python="python3"
# Path to oh-my-zsh installation.
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

## -------------------------------------------------------------------------------- ALIAS

## custom alias
alias sz="source ~/.zshrc"
alias z="nano ~/.zshrc"

alias i="sudo apt install"
alias u="sudo apt update && sudo apt upgrade"
alias a="sudo apt autoclean && sudo apt autoremove"
alias r="sudo dpkg -r"

alias rb="sudo reboot now"
alias sd="sudo shutdown now"

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

## sys
alias sz="source ~/.zshrc"
alias zz="sudo gedit ~/.oh-my-zsh/themes/max.zsh-theme "

alias n="nano"
alias sn="sudo nano"
alias g="gedit"
alias sg="sudo gedit"

alias rb="sudo reboot now"
alias sd="sudo shutdown now"

## pip
alias p="pip3 install"

## -------------------------------------------------------------------------------- DOWNLOAD ONCE

## ARGCOMPLETE
# pip3 install argcomplete
# activate-global-python-argcomplete
# autoload -U bashcompinit
# bashcompinit

## MANUAL
## zsh-autosuggestions
# git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

## zsh-syntax-highlighting
# git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

## --------------------------------------------------------------------------------
