#!/bin/python3
"""Dirty script for reading a PM sensor

Stream PM25 and PM10 readings from a nova SDS011 into a csv file.
This script is only tested on Linux and is made for python 3.
"""
import serial, struct, time, os
from datetime import datetime as dt


def read(s):
    # we need the current and last byte to find the message start
    byte, lastbyte = b'\x00', b'\x00'

    # loop until message is found
    while True:
        lastbyte = byte
        byte = s.read(1)

        # start byte found?
        if lastbyte == b'\xAA' and byte == b'\xC0':
            # read the whole block
            block = s.read(8)

            # decode
            # little endian low byte to high byte
            msg = struct.unpack('<hhxxcc', block)

            # get the values
            pm25 = msg[0] / 10.
            pm10 = msg[1] / 10.

            return pm10, pm25


def start(dev, baud=9600, fname='pm.csv', step_sec=15, to_file=True,
          verbose=True):
    try:
        s = serial.Serial(dev, baud)
    except serial.SerialException:
        raise ValueError('Device %s not found.' % dev)

    # check if file already exists
    if not os.path.exists(fname):
        with open(fname, 'w') as csv:
            csv.write('time,PM10,PM25\n')

    while True:
        # get the reading
        pm10, pm25 = read(s)

        # save to file
        if to_file:
            with open(fname, 'a') as csv:
                t = '%s,%.1f,%.1f\n' % (
                    dt.strftime(dt.utcnow(), '%Y-%m-%d %H:%M:%S'),
                    pm10, pm25
                )
                csv.write(t)

        # and print
        if verbose:
            print('PM10: {} ug/cm3\t\tPM25: {}ug/cm3'.format(pm10, pm25))

        # sleep
        time.sleep(step_sec)


if __name__=='__main__':
    # Setup an Argument Parser
    import argparse
    p = argparse.ArgumentParser(
        description="Command line tool for saving particulate-matter "
                    "measurements from a nova SDS011 into a CSV file."
    )
    p.add_argument('device_path', type=str,
                   help="Device path of the sensor. Typically 'COM1' on "
                        "Windows or '/dev/ttyUSB0' on Linux.")
    p.add_argument('-b', '--baudrate', type=int,
                   help="Device baudrate for serial communication. Typical "
                        "values are 9600 or 57600. Defaults to 9600.")
    p.add_argument('-o', '--output', type=str,
                   help="Output file name. The new readings will be appended "
                        "to this file in CSV format. Defaults to 'pm.csv'.")
    p.add_argument('-s', '--step', type=int,
                   help="Step width for the measurements in seconds. It is "
                        "not recommended to use values smaller than 3 "
                        "seconds. Defaults to 15 [secs].")
    p.add_argument('-q', '--quiet', action='store_false',
                   help="Suppress printing values to the screen.")

    # parse give arguments
    args = p.parse_args()

    # start monitoring
    start(
        dev=args.device_path,
        baud=args.baudrate,
        fname=args.output,
        step_sec=args.step,
        verbose=args.quiet
    )
