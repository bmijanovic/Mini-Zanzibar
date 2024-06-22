import asyncio
import json
import consul.aio


class ConsulDBHandler:
    def __init__(self, host='localhost', port=8500):
        self.client = consul.aio.Consul(host=host, port=port)
        self.latest_version = None
        self.current_version = None
        self.config = {}
        self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.initialize())

    async def initialize(self):
        self.latest_version = await self.get("latest_version")
        self.current_version = await self.get("current_version")
        if self.latest_version is not None and self.current_version is not None:
            self.config = await self.get(self.current_version)
        else:
            self.current_version = "v0"
            self.latest_version = "v0"
            self.config = {}

        # self.loop.create_task(self.watch_for_current_version())

    async def watch_for_current_version(self):
        while True:
            up_to_date_current_version = await self.get("current_version")
            if self.current_version != up_to_date_current_version:
                self.current_version = up_to_date_current_version
                self.config = await self.get(self.current_version)
            up_to_date_latest_version = await self.get("latest_version")
            if self.latest_version != up_to_date_latest_version:
                self.latest_version = up_to_date_latest_version
            await asyncio.sleep(1)

    async def create_new_config(self, new_config):
        new_version = 'v' + str(int(self.latest_version.lstrip("v")) + 1)
        await self.put(new_version, new_config)
        await self.put("latest_version", new_version)
        self.latest_version = new_version

        # change to newly added config
        await self.change_config_to_version(str(new_version))

    async def change_config_to_version(self, version):
        found_config = await self.get(version)
        if found_config is None:
            return
        await self.put("current_version", version)
        self.current_version = version
        self.config = found_config

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
