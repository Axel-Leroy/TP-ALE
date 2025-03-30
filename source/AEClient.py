import logging
import base64
import os
from typing import Tuple
import msgpack
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from pywebio.output import put_text
from names_generator import generate_name
from simple_client import SimpleClient

ITERATIONS=100
KDF_LENGTH=32

class AEClient(SimpleClient):
    def __init__(self, host: str, send_port: int, broadcast_port: int, nick: str, password:str):
        super().__init__(host, send_port, broadcast_port, nick)

        # Configuration crypto
        self._password = password.encode()
        self._log = logging.getLogger(f"AEClient[{nick}]")

    
    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KDF_LENGTH,
            salt=salt,
            iterations=ITERATIONS
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_message(self, password: str, message: str) -> Tuple[bytes, bytes]:
        #génération d'un salt aléatoire pour chaque message
        salt = os.urandom(16)
        #création d'une clé à partir du salt
        key = self.derive_key_from_password(password, salt)

        fernet = Fernet(key)
        #chiffrement du message
        encrypted_message = fernet.encrypt(message.encode())
        return salt, encrypted_message 
    
    def decrypt_message(self, password: str, encrypted_message: bytes, salt: bytes, nick:str) -> str:
        #Déchiffrement d'un message avec le salt fourni
        key = self.derive_key_from_password(password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_message).decode()

    def send(self, frame:dict)->dict:
        #Envoi d'un message chiffré au serveur
        try:
            # Sérialisation avec msgpack
            packet = msgpack.packb(frame)
            response_packet = self._client.send(packet)
            
            if response_packet:
                return msgpack.unpackb(response_packet)
        except Exception as e:
            self._log.error(f"Erreur d'envoi: {e}")
            return {"response": "ko"}

        

    def message(self, message:str):
        #chiffrement du message
        salt, encrypted_message = self.encrypt_message(self._password.decode(), message)
        #création de la frame du meessage
        frame = {
            "type": "message",
            "nick": self._nick,
            "message": {
                "salt": salt.hex(),
                "encrypted_message": encrypted_message.hex()
            }
            }
        self.send(frame)

    def on_recv(self, packet: bytes):
        #Reçoit et déchiffre les messages broadcastés
        try:
            frame = msgpack.unpackb(packet)
            if frame["type"] == "message":
                salt = bytes.fromhex(frame["message"]["salt"])
                encrypted_message = bytes.fromhex(frame["message"]["encrypted_message"])
                #déchiffre le message à partir du salt
                decrypted = self.decrypt_message(self._password.decode(), encrypted_message, salt, frame["nick"])
                put_text(f"{frame['nick']}: {decrypted}", scope='scrollable')
        except Exception as e:
            self._log.error(f"Erreur de déchiffrement: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = AEClient("localhost", 6666, 6667, generate_name(), "Best_Secr3t_ever_!")
    client.run() 

    