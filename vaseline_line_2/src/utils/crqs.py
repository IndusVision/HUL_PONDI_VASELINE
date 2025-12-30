import requests
from datetime import datetime

class params:
    def __init__(self, url):
        self.url = url

    def send_params(self, params_count):
        try:
            # Current system date and time
            recorded_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            # JSON payload
            payload = {
                "params_count": params_count,
                "recorded_date_time": recorded_date_time,
                "parameter": 1,
                "plant_id":10,
                "machine_id":32
            }
            # print('payload',payload)
            # Send POST request
            response = requests.post(self.url, json=payload)
            # print('self.url',self.url)
            # print('response',response)
            # Check response status
            if response.status_code == 200:
                print("Params sent successfully.")
            else:
                print("Failed to send params. Status code:", response.status_code)
        except Exception as e:
            print("Error sending params:", str(e))