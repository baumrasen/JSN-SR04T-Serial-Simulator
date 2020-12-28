#!/usr/bin/env python3
import time
import serial

# create serial 
ser = serial.Serial(
        port='/dev/ttyAMA1', #Replace ttyAMA1 for your needs
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.05
)
# edit here for your needs
value = 200
value_max = 8000 
value_reset = 200
stepsize = 10
sleep_seconds = 1

# for ever do this
while 1:
    
    # look for a character from serial port - will wait for up to 50ms (specified above in timeout)
    data = ser.read(size=1) 

    # check for the right trigger --> 0x55
    if (data == b'\x55'):

        # small waiting time
        time.sleep(0.05)

        ### comment out to set a value
        # value  = 1953

        # print current value to console
        print('current value: ' + str(value))

        # startbit
        b0 = 0xFF

        # the upper 8 bits of the value        
        b1 = (value >> 8) & 0xff

        # the lower 8 bits of the value        
        b2 = value & 0xff        

        # checksum (only low 8 bit)        
        b3 = (b0 + b1 + b2) & 0xFF
    
        # arr = bytearray([0xFF, 0x07, 0xA1, 0xA7]) # should return 1953
        arr = bytearray(4)

        # set the right values to the byte array
        arr[0] = b0
        arr[1] = b1
        arr[2] = b2
        arr[3] = b3
        
        print('bytearray to send: ' + str(b0) + ' ' + str(b1) + ' ' + str(b2) + ' ' + str(b3))        

        # send the array to the serial port
        ser.write(arr)
        
        # empty line
        print()

        value += stepsize
        if (value > value_max):
            # restart from reset value
            value = value_reset

        # wait a bit
        time.sleep(sleep_seconds)
