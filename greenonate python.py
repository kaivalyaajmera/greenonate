from microbit import *
import math

def midiNoteOn(chan, n, vel):
    MIDI_NOTE_ON = 0x90
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_ON | chan, n, vel])
    uart.write(msg)

def midiNoteOff(chan, n, vel):
    MIDI_NOTE_OFF = 0x80
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_OFF | chan, n, vel])
    uart.write(msg)

def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15:
        return
    if n > 127:
        return
    if value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)

def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

Start()
lastA = False
lastB = False
lastC = False
BUTTON_A_NOTE = 36
BUTTON_B_NOTE = 39
BUTTON_C_NOTE = 43
last_tilt = 0
while True:

    a = button_a.is_pressed()
    b = button_b.is_pressed()
    c = pin1.is_touched()
    if a is True and lastA is False:
        midiNoteOn(0, BUTTON_A_NOTE, 127)
    if b is True and lastB is False:
        midiNoteOn(0, BUTTON_B_NOTE, 127)
    if c is True and lastC is False:
        midiNoteOn(0, BUTTON_C_NOTE, 127)

    lastA = a
    lastB = b
    lastC = c
    current_tilt = accelerometer.get_y()
    if current_tilt != last_tilt:
        mod_y = math.floor(math.fabs(((current_tilt + 1024) / 2048 * 127)))
        midiControlChange(0, 22, mod_y)
        last_tilt = current_tilt
    sleep(10)
