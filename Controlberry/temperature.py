'''
To control ds18b20 sensors
'''
import json
import os
import glob
import time
import datetime
from pymongo import MongoClient

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
Temperature = db.Temperature

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

def read(device_file):
    '''
    reads file where are data stored
    '''
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def get_temperature(device_file):
    '''
    returns temperature in celsius as float from raw data
    '''
    lines = read(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temperature = float(temp_string) / 1000.0
        return temperature

def get_data():
	'''
	for each termosensor returns id and temperature
	'''
	result = {}
	[result.update({item.rsplit('/',1)[-1]:get_temperature(item + '/w1_slave')}) for item in device_folders]
	return result
        

def insert_into_database():
    '''
    insert data into database
    '''
    data = get_data()
    if data:
        Temperature.insert({'Timestamp': datetime.datetime.utcnow(), 'Temperature':data})

def run_every_interval(interval = 1):
    '''
    get data from insert_into_database and store them in collection loops in defined interval
    '''
    while True:
        insert_into_database()
        time.sleep(interval)

if __name__ == '__main__':
    run_every_interval()
