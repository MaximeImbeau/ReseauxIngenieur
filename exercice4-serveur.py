import socket
import select
from socketUtils import recv_msg , send_msg


ENTETE_RECEPTION_NOM = "NOM"
# On prépare le socket du serveur
socServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socServeur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socServeur.bind(("localhost", 1234))
socServeur.listen ()
# On prépare deux listes :
# La première pour les sockets des clients connectés
# La seconde pour les sockets en attente d’une opération
listeClients = []
listeAttente = []
# Cette fonction sera appelée lors de la connexion d’un nouveau client
def accueil(socServeur):
    (nouveauClient, _) = socServeur.accept()
    # On ajoute le nouveau client à la liste des clients
    listeClients.append(nouveauClient)
    msg = "Bienvenue, quel est votre nom?"
    send_msg(nouveauClient, msg)
# Cette fonction est appelée quand socClient a envoyé son nom
def receptionNom(socClient, nom):
    msg = "Bienvenue " + nom
    send_msg(socClient, msg)
    # On a fini avec ce client , on le retire de la liste
    listeClients.remove(socClient)
    socClient.close()
while True :
    # On passe à select la liste des clients et le socket du serveur
    # On récupère dans la liste d’attente tous les sockets en attente de lecture
    (listeAttente, _, _) = select.select([socServeur] + listeClients, [], [])
    # On parcours la liste des sockets en attente
    for soc in listeAttente:
        # Si le socket retourné est celui du serveur,
        # un nouveau client est en train de se connecter
        if soc == socServeur:
            accueil(socServeur)
        # Dans le cas contraire , un client a envoyé un message
        else:
            message = recv_msg(soc)
            try :
                [entete, contenu] = message.split(maxsplit=1)
            except AttributeError:
                listeClients.remove(soc)
            if(entete == ENTETE_RECEPTION_NOM):
                receptionNom(soc, contenu)
