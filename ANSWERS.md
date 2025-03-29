1. La sécurité est mauvaise car les données ne sont pas chiffrées : sur le serveur, on peut voir les informations des utilisateurs (clients) et le contenu de leurs messages en clair.

2. La sérialisation pickle est un mauvais choix car les données ne sont pas chiffrées et il n'y a pas de moyen de vérifier si les données ont été altérées. Lors de la désérialisation, le pickle peut éxécuter un script python, qui pourrait être malvaillant.

3. Les principales alternatives à l'utilisation de pickle sont le JSON ou MessagePack.

4. Le chiffrement seul est insuffisant car il garanti la confidentialité, mais pas l'intégrité.