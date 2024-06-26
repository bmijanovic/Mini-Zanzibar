import asyncio
import json
import consul.aio


class ConsulDBHandler:
    def __init__(self, host='localhost', port=8500):
        self.client = consul.aio.Consul(host=host, port=port)
        self.config = {}
        self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.initialize())

    async def initialize(self):
        namespaces = await self.get("namespaces")
        for namespace in namespaces:
            current_version = await self.get("current_version_" + namespace)
            self.config[namespace] = await self.get(current_version + "_" + namespace)

    async def create_new_config(self, namespace, new_config):
        namespaces = await self.get("namespaces")
        namespaces.append(namespace)
        await self.put("namespaces", namespaces)

        new_version = "v1"
        latest_version = await self.get("latest_version_" + namespace)
        if latest_version is not None:
            new_version = 'v' + str(int(latest_version.lstrip("v")) + 1)
        await self.put(new_version + "_" + namespace, new_config)
        await self.put("latest_version_" + namespace, new_version)

        # set new version for current version
        await self.put("current_version_" + namespace, new_version)

    async def change_config_to_version(self, namespace, version):
        found_config = await self.get(version + "_" + namespace)
        if found_config is None:
            return False
        self.config[namespace] = found_config
        return True

    async def get_config(self, namespace):
        if namespace not in self.config.keys():
            return None
        return self.config[namespace]

    async def put(self, key, value):
        value_json = json.dumps(value)
        await self.client.kv.put(key, value_json)

    async def get(self, key):
        index, data = await self.client.kv.get(key)
        if data and 'Value' in data:
            value_str = data['Value'].decode('utf-8')
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                return value_str
        return None
