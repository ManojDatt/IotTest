# Introduction

IoT Controllers/Gateways are computing devices (such as Raspberry Pi)  that collect data from sensors and relay it to the cloud. Let's say they collect data from a temperature sensor.

Being an IoT developer, it becomes extremely important for you to send the data to the server in the most robust and efficient way. You can choose to use either HTTP or MQTT for data transportation.

# Problem Statement:

Consider that an IoT device publishes data to your middleware software which is then published to the cloud.


While you are developing an IoT solution, you do not have access to all the physical sensors and therefore you decide to simulate all types of sensors that exist in a candy factory. A CSV is shared which contains simulated sensor data.

As an IoT developer, 

Edge Program - You have to write a forever executable python program to read sensor data and send it to the cloud server.
Server Program - A simple python HTTP server or MQTT broker to accept data(as per your convenience) and save it in a CSV file.
Goals:

Server Program - Expose a route on an HTTP server or a topic on MQTT broker which accepts data. It should randomly give success or failure for the received data. Each new data should append to a CSV file.
Edge Program
Each data point should be read after every 60-sec delay and publish to the cloud(live data)
If the server returns failure or server is stopped the data point is buffered locally(it now becomes buffered data). 
Publish all the buffered data after every 5 seconds. While cleaning the buffered data the live data should not be stopped, i.e. the program should be properly multithreaded.
Example: 1st & 2nd minute, 1st & 2nd data points published successfully, 3rd & 4th minute, 3rd & 4th data points failed and got buffered, 5th min 5th datapoint and all the buffered data published.
Edge Program - Expose a function to get the count of successfully transmitted and buffered data at any point in time.


# Setup
1. Clone the repository
2. Install `requirements.txt`
3. Install `sudo apt-get install libgpiod2`
4. Update the configuration details in `config.yml` files

# Server Uses
1. Open server terminal and run `python main.py`

# RasPi Uses
On RasPi Open 2 terminal (T1, T2)
   1. On T1 run celery job `celery -A queueing_job worker -l INFO`
   2. On T2 run edge program `python edge_program.py --help` & `python edge_program.py execute_sensor`

Once its setup & running you can monitor by logs.