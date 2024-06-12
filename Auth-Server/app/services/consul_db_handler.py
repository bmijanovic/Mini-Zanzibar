import json
import consul


class ConsulDBHandler:
    def __init__(self, host='localhost', port=8500):
        self.client = consul.Consul(host=host, port=port)

    def store_config(self, key, config):
        config_json = json.dumps(config)
        self.client.kv.put(key, config_json)

    def retrieve_config(self, key):
        index, data = self.client.kv.get(key)
        if data and 'Value' in data:
            config_json = data['Value'].decode('utf-8')
            return json.loads(config_json)
        return None