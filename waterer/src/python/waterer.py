from time import sleep
import datetime
import schedule
import RPi.GPIO as gpio


gpio.setmode(gpio.BCM)

TANK_LEVEL_FLOAT = 4 # The R.Pi pin which is connected to the float switch (monitors tank low level)
PUMP_1 = 16 # The pin the pump is controlled by

gpio.setup(TANK_TOPOFF_PUMP, gpio.OUT, initial=gpio.HIGH)

def water_plants():
    '''
    Function used to water plants on a set schedule using the aquarium water tank
    as the water source
    
    This function may be moved into the topoff program so that certain state 
    variables can be accessed and the water can be topped off between plants
    '''

    gpio.setup(TANK_LEVEL_FLOAT, gpio.IN, pull_up_down=gpio.PUD_UP)
    if gpio.input(TANK_LEVEL_FLOAT):
        print('{}:watering plants'.format(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')))
        gpio.output(TANK_TOPOFF_PUMP, gpio.LOW)
        sleep(60)
        gpio.output(TANK_TOPOFF_PUMP, gpio.HIGH)
        print('{}:finished watering'.format(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')))
    else:
        print('{}: No top off needed'.format(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')))
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

    spi.open(0, SPI_CHANNEL)
    if mode not in ['differential', 'single', 0, 1, '0', '1']:
        raise(ValueError)
    else:
        if mode in ['differential', 0, '0']:
            mode = 0
        else:
            mode = 1
    reading = spi.xfer2([1, ((mode << 3) + channel) << 4, 0], speed_hz=1350000)
    spi.close()
    return (((reading[1] & 0b11) << 8) + reading[2])

def check_water_tank():
    '''
    Uses the mcp3008 to read the water level from a float switch and then maps
    the values to a percentage full basis.
    The water tank is triggered to empty at 10% to ensure that the pump does not pump
    dry.
    '''

    water_level = interp(read_mcp3008(0, mode='single'), TOPOFF_LEVEL, BY_PERCENTAGE)
    print(water_level)
    try:
        if water_level < 5:
            water_tank_empty = True
        else:
            water_tank_empty = False
    except Exception as err:
        water_tank_empty = True
        raise(err)

schedule.every().day.at('02:30').do(water_plants)
while True:
    schedule.run_pending()
    sleep(1)
