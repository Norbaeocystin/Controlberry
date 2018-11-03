'''
how to construct JSON to control Raspberry pi

{'Commands':<string>;
 'Duration':<string>;
 'Name':<string>;
 'Brightness':<int>;
 'State':<boolean>
}
 
 
'''
import datetime
import json
import logging
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import RPi.GPIO as GPIO
from .adafruit import run_every_interval_adafruit
from .camera import get_image_as_bytes
from .temperature import run_every_interval
from .pins import get_on_pin, get_off_pin
import time
from threading import Thread
from .timer import setting_it_all, run_scheduler_forever

from .distance import distance
from .LED import running, get_light, get_light_stop
import pkg_resources

Config = pkg_resources.resource_filename('Controlberry', 'Config/config.json')

logging.basicConfig(level=logging.INFO,  format = '%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

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
Commands = db.Commands
Settings = db.Settings
Distance = db.Distance
Pictures = db.Pictures
Schedule = db.Schedule

for item in ['Commands','Temperature', 'Adafruit', 'Distance','Pictures']:
    try:
        if not db.command('collstats',item).get('capped', False):
            if item=='Pictures':
                db.command({"convertToCapped": item, "size": 100000000});
                logger.info('{} changed to capped collection'.format(item))
            else:
                db.command({"convertToCapped": item, "size": 30000000});
                logger.info('{} changed to capped collection'.format(item)) 
    except OperationFailure:
        pass

def no_arg(func, instances = 1):
    '''
    no_arg will start function func which is function without arguments on threads 
    where number of threads equals instances
    '''
    for i in range(instances):
        t = Thread(target=func)
        t.start()

def watch_collection():
    '''
    checking collection if there will be inserted document which have LED in it it will light up,
    '''
    logger.info('Starting watching Commands collection')
    watcher = Commands.watch()
    for item in watcher:
        doc = item.get('fullDocument')
        if doc:
            _id = doc.get('_id')
            if doc.get('Command') == 'LED':
                logger.info('Led command received')
                if doc.get('State'):
                    name = doc.get('Name')
                    brightness = doc.get('Brightness',100)
                    logger.info('Brightness set to {}'.format(brightness))
                    get_light(name, brightness)
                else:
                    name = doc.get('Name')
                    get_light_stop(name)
            if doc.get('Command') == 'PIN':
                logger.info('Pin command received')
                if doc.get('State'):
                    name = doc.get('Name')
                    logger.info('Turning on {}'.format(name))
                    get_on_pin(name)
                else:
                    name = doc.get('Name')
                    logger.info('Turning off {}'.format(name))
                    get_off_pin(name)
            if doc.get('Command') == 'DISTANCE':
                logger.info('Distance command received')
                dist = distance(doc.get('Name'))
                logger.info('Distance: {} for _id:{}'.format(dist, _id))
                Distance.insert({'_id':_id,'DISTANCE':dist})
            if doc.get('Command') == 'CAMERA':
                logger.info('Camera command received')
                picture_bytes = get_image_as_bytes()
                logger.info('Picture taken for _id:{}'.format(_id))
                Pictures.insert({'_id':_id,'PICTURE':picture_bytes, 'Timestamp':datetime.datetime.now()})
                
def watch_scheduling_collection():
    '''
    checking collection if there will be inserted document which have LED in it it will light up,
    '''
    logger.info('Starting watching Schedule collection')
    watcher = Schedule.watch()
    for item in watcher:
        doc = item.get('fullDocument')
        if doc:
            setting_it_all(doc)


def run():
    sched = Schedule.find_one()
    if sched:
        setting_it_all(sched)
    run_scheduler_forever()
    no_arg(watch_collection)
    no_arg(watch_scheduling_collection)
    no_arg(run_every_interval)
    no_arg(run_every_interval_adafruit)

if __name__ == '__main__':
    sched = Schedule.find_one()
    if sched:
        setting_it_all(sched)
    run_scheduler_forever()
    no_arg(watch_scheduling_collection)
    no_arg(watch_collection)
    no_arg(run_every_interval)
    no_arg(run_every_interval_adafruit)
