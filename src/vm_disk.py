import docker
import asyncio
import logging
import subprocess
import requests

from kademlia.network import Server

class VMDisk:
    def __init__(self, num_disk, type_disk='default'):
        # self.vm = docker.from_env()
        self.num_disk = num_disk
        if type_disk == 'default':
            self.name = f'raidvmdisk_{self.num_disk}'
        else:
            self.name = f'raidvmdisk_{type_disk}_{self.num_disk}'
        # self._pull()
        # self._network(num_disk)
        # self._rm_disk()
        # self._run()
        
    def _network(self):
        self.vm.networks.create(f'net_{self.name}', driver='bridge')
        
    def _pull(self):
        self.vm.images.pull('llleeemh/raidvmdisk')
        
    def run(self):
        # self.vm.containers.run('llleeemh/raidvmdisk', detach=True, name=self.name)
        subprocess.run(['docker', 'run', '--name', self.name, '-d', 'llleeemh/raidvmdisk'])
        self.ip = self._get_ip()
        print(f'Created VM {self.name}')
    
    def _get_ip(self):
        return subprocess.run(['docker', 'inspect', '-f', '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}', self.name], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    
    def rm_disk(self):
        # self.vm.containers.get(self.name).remove(force=True)
        subprocess.run(['docker', 'stop', self.name])
        subprocess.run(['docker', 'rm', self.name])
        print(f'Removed VM {self.name}')
    
    def write(self, data):
        return requests.post(f'http://{self.ip}:5000/write', data=data)
    
    def detect(self):
        return requests.get(f'http://{self.ip}:5000/detect')
    
    def read(self):
        return requests.get(f'http://{self.ip}:5000/read')
    
    def fail(self):
        return requests.post(f'http://{self.ip}:5000/fail')
    
    def detect(self):
        return requests.get(f'http://{self.ip}:5000/detect')
    
        
    async def get(self, key, server: Server, port=5000):
        server = Server()
        await server.listen(8469)
        await server.bootstrap([f'raidvmdisk_{self.num_disk}'], port=port)
        result = await server.get(key)
        server.stop()
        return result
        
    async def set(self, key, value, server: Server, port=5000):
        server = Server()
        await server.listen(8469)
        await server.bootstrap([f'raidvmdisk_{self.num_disk}'], port=port)
        await server.get(key, value)
        server.stop()
        
        
if __name__ == '__main__':
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('kademlia')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    async def run():
        server = Server()
        await server.listen(8470)
        bootstrap_node = ("localhost", 8469)
        await server.bootstrap([bootstrap_node])

        result = await server.get("myKey2")
        print("Get result:", result)
        server.stop()

    asyncio.run(run())