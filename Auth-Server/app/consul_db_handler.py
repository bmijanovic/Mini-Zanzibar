import json
import consul


class ConsulDBHandler:
    def __init__(self, host='localhost', port=8500):
        self.client = consul.Consul(host=host, port=port)
        self.latest_version = self.get("latest_version")
        if self.latest_version is None:
            self.current_version = "v0"
            self.latest_version = "v0"
            self.config = {}
        else:
            self.config = self.get(self.latest_version)

    def create_new_config(self, new_config):
        new_version = 'v' + str(int(self.latest_version.lstrip("v")) + 1)
        self.put(new_version, new_config)
        self.put("latest_version", new_version)
        self.latest_version = new_version

        # change to newly added config
        self.change_config_to_version(str(new_version))

    def change_config_to_version(self, version):
        found_config = self.get(version)
        if found_config is None:
            return
        self.put("current_version", version)
        self.current_version = version
        self.config = found_config

    def get_config(self):
        return self.config

    def put(self, key, value):
        value_json = json.dumps(value)
        self.client.kv.put(key, value_json)

    def get(self, key):
        index, data = self.client.kv.get(key)
        if data and 'Value' in data:
            value_str = data['Value'].decode('utf-8')
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                return value_str
        return None
