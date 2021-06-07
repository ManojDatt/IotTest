# -*- coding: utf-8 -*-
import time
import serial, pdb
from queueing_job import store_sensor_task, write_history, read_history
import pendulum
import plac, logging
TIME_ZONE="Asia/Kolkata"
logging.basicConfig(filename='edge_program.log', format="%(asctime)s;%(levelname)s;%(message)s", level=logging.INFO)  

def execute_sensor(debug=False):
    try:
        import board
        import adafruit_dht
        # Initial the dht device, with data pin connected to:
        dhtDevice = adafruit_dht.DHT22(board.D18)
        """
        If you're using a Raspberry Pi with a DHT22 (or an AM2302) sensor connected to Pin 4, change the following line from:
        dhtDevice = adafruit_dht.DHT22(board.D18)
        to
        dhtDevice = adafruit_dht.DHT22(board.D4)
        # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
        # This may be necessary on a Linux single board computer like the Raspberry Pi,
        # but it will not work in CircuitPython.
        # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
        """
        while True:
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = dhtDevice.humidity
                if debug:
                    print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format( temperature_f, temperature_c, humidity))
                payload = {"timestamp": pendulum.now(tz=TIME_ZONE).strftime('%Y-%m-%dT%H:%M:%S%z'),
                        "sensor": "Sensor-1",
                        "value": temperature_f}
                store_sensor_task.delay(payload)
                write_history(True)
            except RuntimeError as error:
                write_history(False)
                # Errors happen fairly often, DHT's are hard to read, just keep going
                logging.error(error)
                time.sleep(60)
                continue
            except Exception as error:
                write_history(False)
                dhtDevice.exit()
                logging.error(error)
            #Each data point should be read after every 60-sec delay and publish to the cloud(live data)
            time.sleep(60)
    except NotImplementedError as ex:
        print(ex)
    except KeyboardInterrupt as ex:
        print(ex)

def load_history(debug=False):
    #Load celery all jobs list
    data = read_history()
    print('Sensor Data Send Count:\n')
    for key, val in data.items():
        print(f"{key.upper()}: {val}")
    print()

@plac.pos('method', "Method name to run", choices=['load_history', 'execute_sensor'])
@plac.flg('debug', "Enable debug mode")
def main(method, debug=False):
    """A script for IoT sensor value store"""
    eval(method)(debug)
    # globals()[method](**{"debug": debug})

if __name__ =='__main__':
    plac.call(main)