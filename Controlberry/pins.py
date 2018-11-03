'''
For control of LEDs, LED stripes
{'Command':'PIN',
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

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

running = []


def get_pin(name):
    '''
    PinName_0_ returns pin
    '''
    Settings = db.Settings.find_one({"_id":0},{'_id':0})
    pin = name.replace('Name', 'Pin')
    return int(Settings.get(pin))


def get_on_pin(name):
    '''
     get pin number from name and turn on the pin
     and append his name to running list
    '''
    if name in running:
        pass
    else:
        pin = get_pin(name)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.HIGH)
        running.append(name)

def get_pin_off(name):
    '''
    turn off pin if name is in running
    '''
    if name in running:
        pin = get_pin(name)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
        del running[running.index(name)]
