#!/bin/bash

#This should be taken from info.txt in home
#NODE_NAME=$(cat ~/info.txt)
NODE_NAME=$1
DATE=$2
LOC_DIR=images

#FTP_ADDR='115.68.41.211'
#FTP_USER='gappocb'
#FTP_PASS='gappocb!'

#DATE_PATH=$(date+"%Y%m%d")
FILE_NAME=$DATE\_$NODE_NAME\_RGB.jpg
echo $FILE_NAME
#fswebcam -F 30 -r 640x480 --no-banner $LOC_DIR/$FILE_NAME
# configure input 1 for CSI -> MEM (raw image capture)
v4l2-ctl --device /dev/video0 --set-input=0
# configure format
v4l2-ctl --device /dev/video0 --set-fmt-video=width=1280,height=980,pixelformat=MJPG
# capture 2nd frame
v4l2-ctl --device /dev/video0 --stream-mmap --stream-skip=10 --stream-to=$LOC_DIR/$FILE_NAME --stream-count=1

#ftp -n $SFTP_ADDR <<END_SCRIPT
#quote USER $SFTP_USER
#quote PASS $SFTP_PASS
#ftp -n $FTP_ADDR <<END_SCRIPT
#quote USER $FTP_USER
#quote PASS $FTP_PASS
#binary
#mkdir $NODE_NAME
#cd $NODE_NAME
#mkdir $DATE_PATH
#cd $DATE_PATH
#lcd $LOC_DIR
#put $FILE_NAME
#quit
#END_SCRIPT

# Removing image from disk 
#rm $LOC_DIR/$FILE_NAME

exit 0
