1. La sécurité est mauvaise car les données ne sont pas chiffrées : sur le serveur, on peut voir les informations des utilisateurs (clients) et le contenu de leurs messages en clair.

2. La sérialisation pickle est un mauvais choix car les données ne sont pas chiffrées et il n'y a pas de moyen de vérifier si les données ont été altérées. Lors de la désérialisation, le pickle peut éxécuter un script python, qui pourrait être malvaillant.

3. Les principales alternatives à l'utilisation de pickle sont le JSON ou MessagePack.

4. Le chiffrement seul est insuffisant car il garanti la confidentialité, mais pas l'intégrité.

5. 2 solutions pour générer des salts sont :
#1
import secrets
salt = secrets.token_bytes(SALT_LENGTH) 

#2
import os
salt = os.urandom(SALT_LENGHT)

6. Il faut transmettre le salt en clair car on compte sur la confidentialité de la clé. De plus, il est nécessaire pour regénérer la clé côté destinataire.

7. On observe que la structure des messages a changé sur les logs du serveur (ajout du salt). On constate également que le message est illisible.

8. Un serveur malveillant pourrait modifier les données envoyées.

9. Dans le cas de données modifiées, il faudrait ajouter une signature afin de vérifier l'authenticité du message. Fernet n'est pas adapté car le serveur peut recréer un HMAC valide après modification et donc modifier un message et le rechiffre sans être détecté.

10. En pratique, en gardant Fernet, on peut mettre le nick dans le HMAC et vérifier qu'il est bien identique à la réception.