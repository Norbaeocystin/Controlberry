"""
to control adafruit  sensors for temperature and humidity
"""
import Adafruit_DHT


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

def get_data(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return {"Humidity":humidity, "Temperature":temperature}
