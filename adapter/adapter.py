from bridge import Bridge
import ipfshttpclient
import json

class Adapter:
    base_url = 'http://root:root@runtime:8888'

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_param_and_url()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_param_and_url(self):
        self.params = {
            '': self.self.request_data.get('id')
        }

        self.base_url = self.base_url + self.request_data.get('path')

    def upload_json(self, stringJson):
        print(stringJson)
        hash = ''
        
        with open('app.json', 'w') as fp:
            json.dump(stringJson, fp)
        with ipfshttpclient.connect("/dns/ipfs/tcp/5001/http") as client:
            hash = client.add('app.json')['Hash']

        return hash

    def create_request(self):
        try:
            response = self.bridge.request(self.base_url, self.params)
            data = response.json()[0]
            hash = self.upload_json(data)
            print(hash)
            print(data)
            self.result_success(hash)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, hash):
        self.result = hash

    def result_error(self, error):
        self.result = ''
