#!/usr/bin/python
import sys
import os
import curses
import subprocess
import time
import re

proc = subprocess.Popen(
            "/home/jlc/.virtualenvs/mopidy/bin/mopidy --config /home/jlc/.config/mopidy/spectrum.conf",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
def main(stdscr,proc):
    specWin=curses.newwin(20,50,5,5)
    while True:
        for line in iter(proc.stderr.readline,""):
            rawspectrum=re.findall('\-\d{1,2}',line,0)
            if len(rawspectrum) > 2:
                for i in range(0,15):
                    size=int(rawspectrum[i])+50
                    specWin.addstr(i,0,size*'X' +(50-size)*' ')
                specWin.refresh()
curses.wrapper(main,proc)
