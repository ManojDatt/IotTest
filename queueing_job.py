# -*- coding: utf-8 -*-
from celery import Celery
import pendulum, yaml, os, logging, json
from http_helper import HttpClient
logging.basicConfig(filename='celery_execution.log', format="%(asctime)s;%(levelname)s;%(message)s", level=logging.INFO)  
with open('config.yml', 'r') as stream:
    settings = yaml.load(stream, yaml.SafeLoader)
    
BROKER_URL = f"redis://{settings.get('REDIS_HOST')}:{settings.get('REDIS_PORT')}/{settings.get('REDIS_DB')}"
DEBUG = True
TIME_ZONE='Asia/Kolkata'
RETRY_BACKOFF=5#seconds
app = Celery('queueing_job', broker=BROKER_URL, backend=BROKER_URL)
app.conf.timezone = TIME_ZONE

app.conf.broker_transport_options = {
    'priority_steps': list(range(10)),
    'queue_order_strategy': 'priority',
}

def write_history(status):
    # Check if file exists or not
    HISTORY_PATH = 'total_sensor_process.json'
    if os.path.isfile(HISTORY_PATH) and os.access(HISTORY_PATH, os.R_OK):
        with open(HISTORY_PATH,'rw') as file:
            # Open History file
            file_data = json.load(file)
            if status:
                file_data['total_success'] += 1
            else:
                file_data['total_failed'] += 1
            file.write(json.dumps(file_data))
    else:
        with open(HISTORY_PATH,'w') as file:
            # Open History file
            file_data = {'total_success': 0, 'total_failed': 0}
            if status:
                file_data['total_success'] = 1
            else:
                file_data['total_failed'] = 1
            file.write(json.dumps(file_data))

def read_history():
    HISTORY_PATH = 'total_sensor_process.json'
    if os.path.isfile(HISTORY_PATH) and os.access(HISTORY_PATH, os.R_OK):
        with open(HISTORY_PATH) as file:
            # Open History file
            file_data = json.load(file)
            return file_data
    return {'total_success': 0, 'total_failed': 0}

@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=RETRY_BACKOFF, name="Store sensor task")
def store_sensor_task(payload):
    client = HttpClient(debug=DEBUG)
    status, response = client.add_data(payload)
    if not status:
        logging.error("Store sensor data failed =>%s"%response)
        today = pendulum.now(tz=TIME_ZONE)
        #Publish all the buffered data (Failed to push) after every 5 seconds
        next_execute_at = today.add(seconds=RETRY_BACKOFF)
        store_sensor_task.apply_async(args=(payload,), eta=next_execute_at)
        logging.error("Store sensor data retry at =>%s"%next_execute_at)
