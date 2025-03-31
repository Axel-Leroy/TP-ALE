from AEClient import AEClient
from cryptography.hazmat.primitives.hmac import HMAC
import os
from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from names_generator import generate_name

class AEADClient(AEClient):
    def __init__(self, host: str, send_port: int, broadcast_port: int, nick: str, password: str):
        super().__init__(host, send_port, broadcast_port, nick, password)
        
    def encrypt_message(self, password: str, message: str) -> Tuple[bytes, bytes]:
        
        #génération d'un salt aléatoire pour chaque message
        salt = os.urandom(16)
        #création d'une clé à partir du salt
        key = self.derive_key_from_password(password, salt)
        fernet = Fernet(key)
        
        # Hashage du nick et du message
        hmac_digest = HMAC(key, f"{self._nick}{message}".encode(), hashes.SHA256()).digest()
        
        encrypted_message = fernet.encrypt(message.encode() + hmac_digest)
        return salt, encrypted_message
    

    def decrypt_message(self, password: str, encrypted: bytes, salt: bytes, nick: str) -> str:
        key = self.derive_key_from_password(password, salt)
        fernet = Fernet(key)
        
        # Déchiffrage et vérification HMAC
        decrypted = fernet.decrypt(encrypted)
        msg, received_hmac = decrypted[:-32], decrypted[-32:]  # HMAC-SHA256 = 32 octets 
        
        expected_hmac = HMAC(key, f"{nick}{msg.decode()}".encode(), hashes.SHA256()).digest()
        
        if received_hmac != expected_hmac:
            raise ValueError("Message modifié ou nick falsifié !")
        
        return msg.decode()
    
if __name__ == "__main__":
    client = AEADClient("localhost", 6666, 6667, generate_name(), "Best_Secr3t_ever_!")
    client.run() 