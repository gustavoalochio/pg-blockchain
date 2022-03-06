from bridge import Bridge
import ipfshttpclient
import json
import sys
import requests

class Validator:
#{'hashIpfs': 'IlFtZGFrQVNUb2RFcGdERTNrOGJDeVI4RTI2M3QxZW1zNEpKVWFlN1RCZHUyS1ciCg==', 'path': '/api/v1/wtps/00:0D:B9:2F:56:63'}

    base_url = 'http://root:root@runtime:8888'
    ipfs_url = 'http://ipfs:8080/ipfs/'

    def __init__(self, input):
        self.request_data = input.get('data')

        if self.validate_request_data():
            self.bridge = Bridge()
            self.logValidation()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def result_success(self, path):
        print("SUCCESS: Rota: " + str(path) + " verificada!", file=sys.stderr)
        self.result = "SUCCESS: Rota: " + str(path) + " verificada!"

    def result_error(self, path):
        print("ERROR: Rota: " + str(path) + " corrompida!", file=sys.stderr)
        self.result = "ERROR: Rota: " + str(path) + " corrompida!"

    def logValidation(self):
        try:
            print(self.request_data, file=sys.stderr)

            #GET IPFS JSON
            hashIpfs = self.request_data['hashIpfs']

            if not hashIpfs or not hashIpfs.startswith('Qm'):
                self.result_error("")

            url = self.ipfs_url + hashIpfs
            jsonIpfs = self.bridge.request(url).json()
            print(jsonIpfs, file=sys.stderr)

            #GET API JSON
            url = self.base_url + self.request_data['path']
            jsonApi = self.bridge.request(url).json()
            print(jsonApi, file=sys.stderr)

            if(jsonIpfs == jsonApi):
                self.result_success(self.request_data['path'])
            else:
                self.result_success(self.request_data['path'])

        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()