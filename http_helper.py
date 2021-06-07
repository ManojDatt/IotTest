# -*- coding: utf-8 -*-
import json
import requests, pdb
import os, yaml
from os import environ

with open(os.path.join(os.getcwd() , 'config.yml'), 'r') as stream:
    settings = yaml.load(stream, yaml.SafeLoader)
  
class HttpClient():
    def __init__(self, debug=True):
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.session = requests.Session()
        if debug:
            self.server = settings.get('SERVER_BASE_URL')
            self.session.auth = (settings.get('SERVER_USERNAME'), settings.get('SERVER_PASSWORD'))
        else:
            self.server = environ.get('SERVER_BASE_URL')
            self.session.auth = (environ.get('SERVER_USERNAME'), environ.get('SERVER_PASSWORD'))
        
    def get(self, endpoint):
        """General purpose GET method.
        Parameters:
            endpoint (str): Endpoint on form ``"path/to/endpoint"``.
            data (str): Data to use in POST request.
        """
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        request_url = self.server + endpoint
        response = self.session.get(request_url, headers=self.headers)
        if response.status_code != 200:
            try:
                return False, response.json()
            except:
                return False, response.text
        return True,  response.json()

    def post(self, endpoint, data=None):
        """General purpose POST method.
        Parameters:
            endpoint (str): Endpoint on form ``"path/to/endpoint"``.
            data (str): Data to use in POST request.
        Returns:
            dict: Dictionary with request result.
        """
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        request_url = self.server + endpoint
        response = self.session.post(request_url, headers=self.headers, data=data)
        if response.status_code != 200:
            return False, response.text
        return True,  response.json()
        
    def add_data(self,timestamp, sensor, sensor_value):
        """
        Parameters:
            timestamp (datetime): Sensor timestamp.
            sensor (str): Sensor Name.
            sensor (float): Sensor Value.
        Returns:
            Sensor Stored Over Cloud Data.
        """
        payload = {
            "timestamp": timestamp,
            "sensor": sensor,
            "value": sensor_value
            }
        status, response = self.post("store", json.dumps(payload))
        return status, response

    def fetch_data(self, limit=10, offset=0):
        """
        Parameters:
            limit (int): Number of data to fetch.
            offset (int): Number of records to skip.
        Returns:
            List Of Sensor Stored Over Cloud Data.
        """
        status, response = self.get(f"data?limit={limit}&offset={offset}")
        return status, response