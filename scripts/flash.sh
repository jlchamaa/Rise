#!/bin/bash
bright=( 0 1 2 3 4 5 7 9 12 15 18 22 27 32 38 44 51 58 67 76 86 96 108 120 134 148 163 180 197 216 235 255 )
cd ~/Rise/scripts
intensity=0
while [ $intensity -lt 32 ];
do
bash apply.sh ${bright[intensity]}
sleep 0.05
intensity=$[$intensity+1]
done
while [ $intensity -ge 0 ];
do
bash apply.sh ${bright[intensity]}
sleep 0.05
intensity=$[$intensity-1]
done

