import logging
from AEServer import AEServer

class RogueServer(AEServer):
    def __init__(self, recv_port: int, broadcast_port: int) -> None:
        super().__init__(recv_port, broadcast_port)
        logging.basicConfig(level=logging.DEBUG)


    def on_message(self, packet: bytes, frame: dict) -> tuple:

        if frame["nick"] not in self._clients:
            self._log.error(f"Client '{frame['nick']}' n'est pas connecté, impossible d'envoyer le message.")
            return None, self._serial_function({"response": "ko"})

        try:
            if "message" in frame:
                logging.info(f"Message avant modification : {frame["message"]}")
                #on modifie le message
                frame["message"]["encrypted_message"]+=b"[modified by server]".hex()
                logging.info(f"Message après modification : {frame["message"]}")
                modified_packet = self._serial_function(frame)
                #on renvoie le nouveau packet qui a la frame modifiée
                return modified_packet, self._serial_function({"response": "ok"})
            
        except Exception:
            return None, self._serial_function({"response": "ko"})

if __name__ == "__main__":
    server = RogueServer(6666, 6667)
    try:
        while True: server.update()
    except KeyboardInterrupt:
        server.close()

