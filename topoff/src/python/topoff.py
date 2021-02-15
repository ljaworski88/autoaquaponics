#! /usr/bin/env python3
from time import sleep
from pytz import timezone
import datetime
import schedule
import RPi.GPIO as gpio
import spidev
from numpy import interp


eastern = timezone('US/Eastern')
gpio.setmode(gpio.BCM)
spi = spidev.SpiDev()

SPI_CHANNEL = 0 # The hardware spi channel that the mcp3008 is attached to
TANK_LEVEL_FLOAT = 4 # The R.Pi pin which is connected to the float switch (monitors tank low level)
TANK_TOPOFF_PUMP = 14 # The R.Pi pin which controls the relay to the top off pump
MIN_WATER_READING = 582 # The reading of the water gauge when empty
MAX_WATER_READING = 952 # The reading of the water gauge when full
BY_PERCENTAGE = [0, 100] # Used in interp mapping
TOPOFF_LEVEL = [MIN_WATER_READING, MAX_WATER_READING] # Used in interp mapping

gpio.setup(TANK_TOPOFF_PUMP, gpio.OUT, initial=gpio.HIGH)
global water_tank_empty
water_tank_empty = False # state variable of the water tank

def top_off():
    '''
    Function used to top off the aquarium water.
    The operational flow of the function is as follows:
    1) Turn on the sense in and switch on the pull-up resistance
    2) Check to see if the water level is low
        a) Also make sure the water tank is not empty
    3) Top off the aquarium
        a) check every 5 seconds to see if we're done
    4) Turn off the pull-up resistance
    '''

    global water_tank_empty
    fill_error = False
    check_water_tank()
    gpio.setup(TANK_LEVEL_FLOAT, gpio.IN, pull_up_down=gpio.PUD_UP)

    # setting up for topoff and checking the water tank
    if not gpio.input(TANK_LEVEL_FLOAT) and not water_tank_empty:
        print('{}:top off started'.format(datetime.datetime.now(eastern).strftime('%Y/%m/%d-%H:%M:%S')))
        start_time = datetime.datetime.now(eastern)
        run_pump_timer = datetime.datetime.now(eastern)
        gpio.output(TANK_TOPOFF_PUMP, gpio.LOW)

        # the topping off portion of the code
        while not gpio.input(TANK_LEVEL_FLOAT):
            sleep(5)

            # run the pump for one minute with 15 second breaks in between, just in case the motor is running dry
            if (datetime.datetime.now(eastern) - run_pump_timer) > datetime.timedelta(seconds=60):
                gpio.output(TANK_TOPOFF_PUMP, gpio.HIGH)
                sleep(15)
                gpio.output(TANK_TOPOFF_PUMP, gpio.LOW)
                run_pump_timer = datetime.datetime.now(eastern)

            # if the entire topoff is taking longer than an hour, then something is wrong
            if (datetime.datetime.now(eastern) - start_time) > datetime.timedelta(hours=1):
                print('topoff taking too long check pump system')
                fill_error = True
                break

        # make sure to turn off the pump
        gpio.output(TANK_TOPOFF_PUMP, gpio.HIGH)

        # log what happened
        if fill_error:
            print('{}:top off interuppted, check error logs'.format(datetime.datetime.now(eastern).strftime('%Y/%m/%d-%H:%M:%S')))

        else:
            print('{}:top off finished'.format(datetime.datetime.now(eastern).strftime('%Y/%m/%d-%H:%M:%S')))

    elif water_tank_empty:
        print('{}:top off skipped, water tank too low'.format(datetime.datetime.now(eastern).strftime('%Y/%m/%d-%H:%M:%S')))

    else:
        print('{}: no top off needed'.format(datetime.datetime.now(eastern).strftime('%Y/%m/%d-%H:%M:%S')))
    gpio.setup(TANK_LEVEL_FLOAT, gpio.IN, pull_up_down=gpio.PUD_OFF)

def read_mcp3008(channel, mode='differential'):
    '''
    we need to do some bit shifting to align the data properly for the MCP3008
    the first byte needs to be 1 to tell the MCP3008 to return a value. Next we
    make the next byte which has the mode in the MSB imediately followed by the
    desired channel to read from, this value is bit shifted so the proper values
    are in the MSB. We need to send one more bit to the MCP because it needs a
    transfer in to transfer out the data and the value here is unimportant. The
    result is also bit shifted to be properly reconstructed.
    '''

    spi.open(0, channel)
    if mode not in ['differential', 'single', 0, 1, '0', '1']:
        raise(ValueError)
    else:
        if mode in ['differential', 0, '0']:
            mode = 0
        else:
            mode = 1
    spi.max_speed_hz = 1350000
    reading = spi.xfer2([1, ((mode << 3) + channel) << 4, 0])
    spi.close()
    return (((reading[1] & 0b11) << 8) + reading[2])

def check_water_tank():
    '''
    Uses the mcp3008 to read the water level from a float switch and then maps
    the values to a percentage full basis.
    The water tank is triggered to empty at 10% to ensure that the pump does not pump
    dry.
    '''

    water_level = interp(read_mcp3008(SPI_CHANNEL, mode='single'), TOPOFF_LEVEL, BY_PERCENTAGE)
    print('water level is: ' + str(water_level))
    global water_tank_empty
    try:
        if water_level < 30:
            water_tank_empty = True
            print('water tank empty')
        else:
            water_tank_empty = False
    except Exception as err:
        water_tank_empty = True
        print(err)

schedule.every().day.at('01:30').do(top_off)
# schedule.every().second.do(check_water_tank)
schedule.every().hour.do(check_water_tank)
while True:
    schedule.run_pending()
    sleep(3600)
