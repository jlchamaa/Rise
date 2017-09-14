#!/bin/bash
/bin/date >> ~/Rise/scripts/log.txt
ping -c2 8.8.8.8 > /dev/null
if [ $? != 0 ] 
then
  /bin/date >> ~/Rise/scripts/log.txt
  /sbin/ifdown 'wlan0'
  sleep 5
  /sbin/ifup 'wlan0'
fi
