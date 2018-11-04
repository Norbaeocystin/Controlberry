'''
how to construct JSON to control Raspberry pi
{'Commands':<string>;
 'Duration':<string>;
 'Name':<string>;
 'Brightness':<int>;
 'State':<boolean>
 }
 
 How to construct Scheduler:
{'PinName_1_':{'On':10:36','Off':11:20},
'PinName_2_:{'On':10:20','Off':11:30},
'LedName_1_':{'On':10:20','Off':11:30,'Brigthness':50}
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
import schedule
import time
from threading import Thread

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
            logger.info('Changes to Schedule collection')
            setting_it_all(doc, schedule = schedule)
            

def run_threaded(func):
    '''
    run funcion in non blocking way
    '''
    job_thread = Thread(target = func)
    job_thread.start()

def set_schedule(func, time, tags, arguments):
    '''
    function to set schedule for every day
    
    ===========
    parameters:
    
    func: <function object>
    time: <string>  for example in shape '10:23' 'hh:mm'
    tags: <tuple> tuple of strings for example 'adafruit', '10:23'
    args: <tuple> tuple of arguments for feeding function
    '''
    f = partial(func, *arguments)
    s = schedule.every().day.at(time).do(run_threaded, f)
    s.tags = tags

def delete_schedule(tags):
    '''
    will delete scheduling functions by finding tags in schedule.jobs
    better to use name and time in tags tuple
    '''
    for item in schedule.jobs :
        if set(tags).issubset(item.tags):
            schedule.cancel_job(item)
            
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
            
def run_scheduler_forever():
    '''
    starts running scheduler
    '''
    run_threaded(run_scheduler)
    
            
def clear_schedule():
    '''
    clear all jobs in schedule class
    '''
    schedule.clear()
    
def setting_it_all(ScheduleJson):
    '''
    input is json, first scheduler will be cleared after that 
    setup happens
    '''
    clear_schedule()
    keys = list(ScheduleJson.keys())
    pins = [item for item in keys if 'PinName' in item]
    leds = [item for item in keys if 'LedName' in item]
    for item in pins:
        time_on = ScheduleJson[item]['On']
        time_off = ScheduleJson[item]['Off']
        set_schedule(get_on_pin, time_on, [item, time_on], [item] )
        set_schedule(get_off_pin, time_off, [item, time_off], [item] )
        logger.info('Schedule setup for {}'.format(item))
    for item in leds:
        time_on = ScheduleJson[item]['On']
        time_off = ScheduleJson[item]['Off']
        brightness = ScheduleJson[item].get('Brightness', 100)
        def off_on(item, brightness):
            get_light_stop(item)
            get_light(item, brightness)
        set_schedule(off_on, time_on, [item, time_on], [item, brightness] )
        set_schedule(get_light_stop, time_off, [item, time_off], [name])
        logger.info('Schedule setup for {}'.format(item))
        
def run():
    run_scheduler_forever()
    sched = Schedule.find_one({'_id':0})
    if sched:
        setting_it_all(sched)
    no_arg(watch_scheduling_collection)
    no_arg(watch_collection)
    no_arg(run_every_interval)
    no_arg(run_every_interval_adafruit)

if __name__ == '__main__':
    run_scheduler_forever()
    sched = Schedule.find_one({'_id':0})
    if sched:
        setting_it_all(sched)
    no_arg(watch_scheduling_collection)
    no_arg(watch_collection)
    no_arg(run_every_interval)
    no_arg(run_every_interval_adafruit)
