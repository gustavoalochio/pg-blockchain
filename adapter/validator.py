from bridge import Bridge
import ipfshttpclient
import json
import sys

class Validator:
    # base_url = 'http://root:root@runtime:8888'

    def __init__(self, input):
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

    def logValidation(self):
        try:
            print(self.request_data, file=sys.stderr)

        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, hash):
        print("Rota:"  , file=sys.stderr)

    def result_error(self, error):
        self.result = {
            'hash': '',
            'route': ''
        }
