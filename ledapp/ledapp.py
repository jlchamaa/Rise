import serial, time, datetime
from datetime import timedelta
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
@app.route("/")
def hello():
    global hardware
    hardware=1
    global on
    on=False
    if 'ser' not in locals():
        global ser
        ser = serial.Serial('/dev/ttyUSB0', 38400)
        return render_template('ui.html')
@app.route("/apply")
def application():
    hardware=0
    red=int(request.args.get('r'))
    green=int(request.args.get('g'))
    blue=int(request.args.get('b'))
    sendbit=int(request.args.get('s'))
    ba=bytearray()
    ba[0:3]=[red,green,blue,sendbit]
    for index,value in enumerate(ba):
        ba[index]=min(255,value+1)
    ser.write(ba)
    ser.write('\0')
    return('')
@app.route("/supply")
def supplication():
    new=0
    r=0
    g=0
    b=0
    if(ser.in_waiting >= 4):
        ba=bytearray()
        ba[0:4]=[90,90,90,90,90]
        i=0
        x='w'
        while(x != '\0'):
            x=ser.read()
            ba[i]=x
            i=i+1
        r=ba[0]-1
        g=ba[1]-1
        b=ba[2]-1
        new=1
    return jsonify(red=r,green=g,blue=b,info=new)
if __name__ == "__main__":
    app.run(processes=2)
