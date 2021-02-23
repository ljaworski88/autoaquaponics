from time import sleep
import datetime
import schedule
import RPi.GPIO as gpio


gpio.setmode(gpio.BCM)

TANK_LEVEL_FLOAT = 4 # The R.Pi pin which is connected to the float switch (monitors tank low level)
PUMP_1 = 16 # The pin the pump is controlled by

gpio.setup(PUMP_1, gpio.OUT, initial=gpio.HIGH)

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
        gpio.output(PUMP_1, gpio.LOW)
        sleep(60)
        gpio.output(PUMP_1, gpio.HIGH)
        print('{}:finished watering'.format(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')))
    else:
        print('{}: No top off needed'.format(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')))
    gpio.setup(TANK_LEVEL_FLOAT, gpio.IN, pull_up_down=gpio.PUD_OFF)

def read_soil_moisture(channel, mode='differential'):
    '''
    This function reads the soil moisture sensor and returns what the current
    moisture level of the soil by the probe is
    '''
    pass

def check_water_tank():
    '''
    Uses the mcp3008 to read the water level from a float switch and then maps
    the values to a percentage full basis.
    The water tank is triggered to empty at 10% to ensure that the pump does not pump
    dry.
    '''
    pass

schedule.every().day.at('02:30').do(water_plants)
while True:
    schedule.run_pending()
    sleep(1)
