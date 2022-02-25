from bridge import Bridge
import ipfshttpclient
import json
import sys

class Adapter:
    base_url = 'http://root:root@runtime:8888'

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        print(self.request_data, file=sys.stderr)

        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_url()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_url(self):
        #montar a url corrretamente aqui, validando para casos em que nao tem / ou tem sobrando
        self.base_url = self.base_url + self.request_data.get('path') + self.request_data.get('id')

    def upload_json(self, stringJson):
        print(stringJson, file=sys.stderr)

        hash = ''
        
        with open('app.json', 'w') as fp:
            json.dump(stringJson, fp)
        with ipfshttpclient.connect("/dns/ipfs/tcp/5001/http") as client:
            hash = client.add('app.json')['Hash']

        return hash

    def create_request(self):
        try:
            print(self.base_url, file=sys.stderr)

            response = self.bridge.request(self.base_url)
            data = response.json()[0]
            hash = self.upload_json(data)
            print(hash, file=sys.stderr)
            print(data, file=sys.stderr)

            self.result_success(hash)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, hash):
        self.result = hash

    def result_error(self, error):
        self.result = ''
