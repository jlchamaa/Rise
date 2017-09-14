import subprocess 
import curses

def main(stdscr):
    process = subprocess.Popen(["mopidy"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    stdscr.addstr(5,5,"Press 'q' to exit")
    g='b'
    while g != 'q':
        g= stdscr.getch()
        process.stdout.flush()
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            out = output.strip()
        stdscr.addstr(6,6,str(out))
curses.wrapper(main)
