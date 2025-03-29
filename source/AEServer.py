import msgpack
import logging
from simple_server import SimpleServer

class AEServer(SimpleServer):
    def __init__(self, recv_port: int, broadcast_port: int) -> None:
        super().__init__(recv_port, broadcast_port)

        # Remplacement de pickle par msgpack
        self._serial_function = msgpack.packb
        self._deserial_function = msgpack.unpackb

#utilisation d'AEServer identique à celle de simple_server
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = AEServer(6666, 6667)
    print("Ctrl+C to stop")
    try:
        while True:
            server.update()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()