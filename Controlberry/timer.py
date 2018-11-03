'''
for pins it relatively easy because only what needs to be done on and of
for leds also needs to add brightness

How to construct Scheduler:
{'PinName_1_':{'ON':10:36','OFF':11:20},
'PinName_2_:{'ON':10:20','OFF':11:30},
'LedName_1_':{'ON':10:20','OFF':11:30,'Brigthness':50}
}
'''

from functools import partial
import pkg_resources
from pymongo import MongoClient
import schedule
import time
from threading import Thread

from .pins import get_on_pin, get_off_pin
from .LED import running, get_light, get_light_stop

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
Schedule = db.Schedule

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
        schedule.run_all()
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
        set_schedule(get_on_pin, time_on, [name, time_on], [name] )
        set_schedule(get_off_pin, time_off, [name, time_off], [name] )
    for item in leds:
        time_on = ScheduleJson[item]['On']
        time_off = ScheduleJson[item]['Off']
        brightness = ScheduleJson[item].get('Brightness', 100)
        def off_on(name, brightness):
            get_light_stop(name)
            get_light(name, brightness)
        set_schedule(off_on, time_on, [name, time_on], [name, brightness] )
        set_schedule(get_light_stop, time_off, [name, time_off], [name])
