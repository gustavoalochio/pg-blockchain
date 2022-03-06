from bridge import Bridge
import ipfshttpclient
import json
import sys

class Adapter:
    base_url = 'http://root:root@runtime:8888'

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        # print(self.request_data, file=sys.stderr)

        if self.validate_request_data():
            self.bridge = Bridge()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def upload_json(self, jsonDict):
        # print(jsonDict, file=sys.stderr)
        # print(json.dumps(jsonDict), file=sys.stderr)
        # print(type(jsonDict), file=sys.stderr)

        hash = ''
    
        with ipfshttpclient.connect("/dns/ipfs/tcp/5001/http") as client:
            hash = client.add_str(json.dumps(jsonDict))
            client.pin.ls(type='all')
            
        return hash

    def create_request(self):
        try:
            # print(self.base_url, file=sys.stderr)

            response = self.bridge.request(self.base_url + self.request_data.get('path'))
            data = response.json()
            # print(data, file=sys.stderr)

            hash = self.upload_json(data)
            # print(hash, file=sys.stderr)

            self.result_success(hash)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, hash):
        print("Hash gerada!", file=sys.stderr)
        print(hash, file=sys.stderr)
        self.result = hash

    def result_error(self, error):
        print("Error: Sem hash!", file=sys.stderr)
        self.result = ''
