#!/usr/bin/python3

from os import path
import math
import re
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst


GObject.threads_init()
Gst.init(None)
filename = path.join(path.dirname(path.abspath(__file__)), 'MVI_5751.MOV')


class AudioEncoder(Gst.Bin):
    def __init__(self):
        super().__init__()

        # Create elements
        q1 = Gst.ElementFactory.make('queue', None)
        resample = Gst.ElementFactory.make('audioresample', None)
        convert = Gst.ElementFactory.make('audioconvert', None)
        rate = Gst.ElementFactory.make('audiorate', None)
        enc = Gst.ElementFactory.make('vorbisenc', None)
        q2 = Gst.ElementFactory.make('queue', None)

        # Add elements to Bin
        self.add(q1)
        self.add(resample)
        self.add(convert)
        self.add(rate)
        self.add(enc)
        self.add(q2)
        
        # Link elements
        q1.link(resample)
        resample.link(convert)
        convert.link(rate)
        rate.link(enc)
        enc.link(q2)

        # Add Ghost Pads
        self.add_pad(
            Gst.GhostPad.new('sink', q1.get_static_pad('sink'))
        )
        self.add_pad(
            Gst.GhostPad.new('src', q2.get_static_pad('src'))
        )


class VideoEncoder(Gst.Bin):
    def __init__(self):
        super().__init__()

        # Create elements
        q1 = Gst.ElementFactory.make('queue', None)
        convert = Gst.ElementFactory.make('videoconvert', None)
        scale = Gst.ElementFactory.make('videoscale', None)
        enc = Gst.ElementFactory.make('theoraenc', None)
        q2 = Gst.ElementFactory.make('queue', None)

        # Add elements to Bin
        self.add(q1)
        self.add(convert)
        self.add(scale)
        self.add(enc)
        self.add(q2)

        # Set properties
        scale.set_property('method', 3)  # lanczos, highest quality scaling

        # Link elements
        q1.link(convert)
        convert.link(scale)
        scale.link_filtered(enc,
            # Scale to 960x540, and for fun use 4:4:4 color
            Gst.caps_from_string('video/x-raw, width=960, height=540, format=Y444')
        )
        enc.link(q2)

        # Add Ghost Pads
        self.add_pad(
            Gst.GhostPad.new('sink', q1.get_static_pad('sink'))
        )
        self.add_pad(
            Gst.GhostPad.new('src', q2.get_static_pad('src'))
        )


class Example:
    def __init__(self,freq):        
        self.freq = freq
        self.mainloop = GObject.MainLoop()
        self.pipeline = Gst.Pipeline()
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_eos)

        # Create elements
        self.src = Gst.ElementFactory.make('audiotestsrc', None)
        self.spec = Gst.ElementFactory.make('spectrum', None)
        self.sink =  Gst.ElementFactory.make('autoaudiosink', None)

        # Add elements to pipeline      
        self.pipeline.add(self.src)
        self.pipeline.add(self.spec)
        self.pipeline.add(self.sink)

        # Set properties
        self.src.set_property('freq', self.freq)
        self.spec.set_property('bands',256)

        self.src.link(self.spec)
        self.spec.link(self.sink)

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.mainloop.run()

    def kill(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.mainloop.quit()

    def on_eos(self, bus, msg):
        if msg.type ==Gst.MessageType.ELEMENT:
            s=msg.get_structure()
            if s.get_name()=='spectrum':
                mystring = s.to_string()
                rawspec=re.findall('\-\d{1,2}',mystring,0)
                print(rawspec)
                self.kill()
for i in range (1,200):
    frequency = i * 100
    print("frequency:"+str(frequency))
    example = Example(frequency)
    example.run()
