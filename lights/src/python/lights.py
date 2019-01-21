#! /usr/bin/env python3

import schedule
from time import sleep
from skyfield import api
import RPi.GPIO as gpio
ts = api.load.timescale()
e = api.load('de421.bsp')
from skyfield import almanac
import datetime
from pytz import timezone

gpio.setmode(gpio.BCM)
LIGHT_SWITCH = 15 # The R.Pi pin which controls the relay to the lights

eastern = timezone('US/Eastern')
miami = api.Topos('25.7617 N', '80.1918 W')
gpio.setup(LIGHT_SWITCH, gpio.OUT, initial=gpio.HIGH)

def find_sunrise_sunset():
    try:
        times, phase = almanac.find_discrete(ts.utc(datetime.date.today()),
                                             ts.utc(datetime.date.today()+datetime.timedelta(days=1)),
                                             almanac.sunrise_sunset(e, miami))
        global sunrise, sunset
        sunrise, sunset = times.astimezone(eastern)
        print('sunrise is at: '+ str(sunrise))
        print('sunset is at: '+ str(sunset))
    except Exception as err:
        print('error in finding sunrise and sunset. Traceback:')
        print(err)

def turn_on_lights():
    gpio.output(LIGHT_SWITCH, gpio.LOW)
    print('lights on')

def turn_off_lights():
    gpio.output(LIGHT_SWITCH, gpio.HIGH)
    print('lights off')

def check_lights():
    current_time = datetime.datetime.now(eastern)
    global sunrise, sunset
    if sunrise < current_time < sunset:
        turn_on_lights()
    else:
        turn_off_lights()


schedule.every().day.at('03:00').do(find_sunrise_sunset) # why 3am? to avoid DLST
                                                     # bullshit and I'm not far
                                                     # north or south enough to
                                                     # ever worry about sunrise
                                                     # before 4AM
schedule.every().minute.do(check_lights)
global sunrise, sunset
find_sunrise_sunset()

while True:
    schedule.run_pending()
    sleep(30)
