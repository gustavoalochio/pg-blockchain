from bridge import Bridge


class Adapter:
    base_url = 'http://root:root@54.232.62.226:8888/api/v1/wtps'
    from_params = ['id']

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_params(self):
        for param in self.from_params:
            self.from_param = self.request_data.get(param)
            if self.from_param is not None:
                break
        # for param in self.to_params:
        #     self.to_param = self.request_data.get(param)
        #     if self.to_param is not None:
        #         break

    def create_request(self):
        try:
            params = {
                '': self.from_param,
            }
            response = self.bridge.request(self.base_url, params)
            data = response.json()[0]
            print(data)
            # self.result = data
            # data['result'] = self.result
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': data,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
