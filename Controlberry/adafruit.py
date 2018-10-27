"""
to control adafruit  sensors for temperature and humidity
"""
import Adafruit_DHT
import pkg_resources

Config = pkg_resources.resource_filename('Controlberry', 'Config/config.json')

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

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

def get_adafruit_sensors(Settings):
	adafruitSensors = [item for item in Settings.keys() if 'AdafruitName']
	return adafruitSensors

def get_data(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return {"Humidity":humidity, "Temperature":temperature}

def get_data_for_sensors():
	Setting = db.Settings.find_one({"_id":0},{'_id':0})
	sensors = get_adafruit_sensors(Settings)
