import logging
import asyncio

from kademlia.network import Server

def main():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('kademlia')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)


    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    server = Server()
    loop.run_until_complete(server.listen(8468))

    # To bootstrap the server with known nodes 
    bootstrap_node = ("0.0.0.0", 8468)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()
