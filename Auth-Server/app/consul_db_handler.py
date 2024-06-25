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
        current_version = await self.get("current_version")
        if current_version is not None:
            self.config = await self.get(current_version)
        else:
            self.config = {}

    async def create_new_config(self, new_config):
        latest_version = await self.get("latest_version")
        if latest_version is None:
            latest_version = "v0"
        new_version = 'v' + str(int(latest_version.lstrip("v")) + 1)
        await self.put(new_version, new_config)
        await self.put("latest_version", new_version)

        # set new version for current version
        await self.put("current_version", new_version)

    async def change_config_to_version(self, version):
        found_config = await self.get(version)
        if found_config is None:
            return False
        self.config = found_config
        return True

    async def get_config(self):
        return self.config

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
