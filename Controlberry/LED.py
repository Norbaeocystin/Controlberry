'''
For control of LEDs, LED stripes

{'Command':'LED',
'Brightness':100,
'Name':<string>,
'State':<boolean>
}
'''
import json
from pymongo import MongoClient
import RPi.GPIO as GPIO
import time
from threading import Thread
from functools import partial

import pkg_resources

Config = pkg_resources.resource_filename('Controlberry', 'Config/config.json')
#loads config file
json_data= open(Config).read()
DATABASE = json.loads(json_data)
URI = DATABASE.get('URI')
DB = DATABASE.get('Database')

#if URI doesnt exits it will write data to config.json
if not URI:
    URI = input("Please write your connection MongoDB URI and press Enter: \n")
    DB = input("Please write name of your Database: \n")
    with open(Config, 'w') as outfile:
        json.dump({'URI':URI,'Database':DB}, outfile)

json_data= open(Config).read()
DATABASE = json.loads(json_data)
URI = DATABASE.get('URI')
DB = DATABASE.get('Database')
CONNECTION = MongoClient(URI, connect = False)
db = CONNECTION.get_database(DB)
Settings = db.Settings.find_one({"_id":0},{'_id':0})

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

running = {}


def get_pin(name):
    '''
    LedName_0_ returns pin
    '''
    pin = name.replace('Name', 'Pin')
    return int(Settings.get(pin))


def get_light(name, brightness = 100):
    '''
     pin number of GPIO pin, brightness = from 0 to 100
    '''
    if running.get(name):
        p = running.get(name)
        p.ChangeDutyCycle(brightness)
    else:
        pin = get_pin(name)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        p = GPIO.PWM(pin,124)
        running.update({name:p})
        partial_p = partial(p.start, brightness)
        t = Thread(target = partial_p)
        t.start()

def get_light_stop(name):
    if running.get(name):
        running.get(name).stop()
        del running[name]
