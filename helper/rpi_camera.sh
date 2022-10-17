#### STILL IMAGES

# Take a picture
raspistill -o pic.jpg

# Take picture after a lag
raspistill -t 10000 -o pic1.jpg

# Watch the camera feed
raspistill -p -o

# apply vertical flip to the capture
raspistill -vf -o pic2.jpg

# apply horizntal flip
raspistill -vh -o pic3.jpg

# specify resolution
raspistill -o pic5.jpg -w 640 -h 480

# specify format
raspistill -o pic6.png -e png

##### VIDEO
# record a 5seconds video
raspivid -o video.h264

# record a specific length video
raspivid -o video3.h264 -t 15000

# convert h264 to mp4
sudo apt-get install -y gpac
MP4Box -add pivideo.h264 pivideo.mp4

# split video
sudo apt-get install ffmpeg
ffmpeg -ss 00:00:00 -t 00:30:00 -i input.avi -vcodec copy -acodec copy output1.avi

# faster and more accurate split
ffmpeg -ss 00:01:00 -i input.mp4 -to 00:02:00 -c copy output.mp4

# compress (but mantain a lot of quality)
ffmpeg -i input.mp4 -vcodec libx265 -crf 24 output.mp4

# Resize
# si input size es 1920x1080, usar multiplos de 16x9 mantiene la relacion de aspecto
# 960x540 (reduccion a 1/4)
# 320x180 (reduccion a 1/36)
# 640x360 (reduccion a 1/9)
# 800x450 (reduccion a 1/5)
ffmpeg -i input.mp4 -s 640x480 -vcodec libx265 -crf 24 output.mp4

# faster video (less frames)!
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4

# resize image to width 25, keeping aspect ratio
convert -geometry 25x src/image1.png out/image1.png

# resize image to height 25, keeping aspect ratio
convert -geometry x25 src/image1.png out/image1.png

# concatenate images horizontally
convert +append src/image1.png src/image2.png out/image12horiz.png

# concatenate images vertically
convert -append src/image1.png src/image2.png out/image12vert.png

# crop image starting at x: 50, y: 100, cropped region of size W: 640, H: 480
$ convert foo.png -crop 640x480+50+100 out.png
