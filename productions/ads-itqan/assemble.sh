# التجميع: سراج (افتتاح) ← الإعلان ← فراغ 0.6 ث ← سراج (ختام)
set -e
O=$1; C=$2; OUT=$3
for f in $O $C itqan-ad.mp4; do ffmpeg -v error -y -i $f -vf "fps=24,scale=1280:720,format=yuv420p" -af "aresample=48000,loudnorm=I=-16:TP=-1.5" -ac 2 -c:v libx264 -crf 19 -c:a aac -b:a 160k /tmp/n-$(basename $f); done
ffmpeg -v error -y -f lavfi -i color=c=black:s=1280x720:r=24:d=0.6 -f lavfi -i anullsrc=r=48000:cl=stereo -t 0.6 -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 160k /tmp/gap.mp4
A=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/n-$(basename $O)); X=$(python3 -c "print($A-0.4)")
ffmpeg -v error -y -i /tmp/n-$(basename $O) -i /tmp/n-itqan-ad.mp4 -i /tmp/gap.mp4 -i /tmp/n-$(basename $C) -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.4:offset=$X[v1];[0:a][1:a]acrossfade=d=0.4[a1];[3:v]fade=t=in:st=0:d=0.4[c];[v1][a1][2:v][2:a][c][3:a]concat=n=3:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 20 -c:a aac -b:a 160k $OUT
ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT
