cd ~/Rise
bright=( 0 1 2 3 4 5 7 9 12 15 18 22 27 32 38 44 51 58 67 76 86 96 108 120 134 148 163 180 197 216 235 255 )
delay=60
step=1
mpc clear
mpc volume 0
mpc load "Mopidy (by 1218989400)"
mpc shuffle
mpc repeat
mpc play
while [ $step -lt 32 ];
do
mpc volume $[3*step]
bash apply.sh ${bright[step]}
sleep $delay
step=$[$step+1]
done
mpc clear
bash apply.sh 0
times=0
while [ $times -lt 3 ];
do
bash flash.sh
times=$[$times+1]
done
