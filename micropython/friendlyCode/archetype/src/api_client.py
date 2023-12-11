import urequests as requests
import ujson

class ApiClient:

    def __init__(self, 
                 config_file: str) -> None:

        self.config_file = config_file

        with open(config_file) as f:
            self.config_file = ujson.load(f)
            self.config_file = self.config_file['wifi']
    
    def send_data(self,
                  data: dict) -> None:
            """
                Sends data to the cloud.
                If it fails, raises an exception.
            """
            print('ApiClient sending data to cloud...')
            print('Data: {}'.format(data))
            print('Sending data to: {}'.format(self.config_file['api_url']))

            response = requests.post(self.config_file['api_url'], 
                                     json=data)
            print('Response: {}'.format(response.text))

            if response.status_code != 200:
                raise Exception('Error sending data to cloud.')
            print('Data sent to cloud.')