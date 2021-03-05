## Maxime Imbeau, Équipe 33, 111 186 939

from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire
import socket
import argparse
from socketUtils import recv_msg, send_msg, recvall
from datetime import datetime


parser = argparse.ArgumentParser(description="Description du programme.")
parser.add_argument("-p", "--port", dest="port", required=True, type=int, action="store", default=3300, help="Choisir un port(Par défaut : 3300)")
parser.add_argument("-6", dest="IPv6", action="store_true", default=False, help="Permet de démarrer le programme avec le protocol IPv6(Par défault : IPv4)")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-e", "--ecoute", dest="server", action="store_true", default=False, help="Serveur en mode écoute")
group.add_argument("-a", "--address", dest="address", action="store", help="Indiquer l’adresse de l’hôte")
args = parser.parse_args()

try:
    if args.server:
        if not args.IPv6:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind(("localhost", args.port))
        serverSocket.listen(5)
        print("Ecoute sur le port " + str(serverSocket.getsockname()[1]))
        numClient = 1
        while True:
            (clientSocket, addr) = serverSocket.accept()
            
            print("Connexion n°" + str (numClient))
            print("--------------------------------------------------------")
            numClient += 1
            # Le serveur prépare et envoie le modulo et la base encodé en UTF-8
            a = trouverNombrePremier()
            b = entierAleatoire(a)
            print(f'Envoi du modulo: {a}')
            print(f'Envoi de la base: {b}')
            print("--------------------------------------------------------")
            
            send_msg(clientSocket, str(a))
            send_msg(clientSocket, str(b))
            
            # Le serveur génère une clé privée
            cle_privee_serveur = entierAleatoire(a)
            print(f'Clé privée : {cle_privee_serveur}')
            
            # Le serveur calcule la clé publique
            cle_publique_serveur = exponentiationModulaire(b, cle_privee_serveur, a)
            print(f'Clé publique à envoyer : {cle_publique_serveur}')
            
            # Le serveur envoie la clé publique au client
            send_msg(clientSocket, str(cle_publique_serveur))
            
            # Le serveur recoit la clé publique du client
            cle_publique_recue = int(recv_msg(clientSocket))
            print(f'Clé publique recue: {cle_publique_recue}')
            
            # Le serveur calcule la clé partagée
            cle_partagee_serveur = exponentiationModulaire(cle_publique_recue, cle_privee_serveur, a)
            print(f'Clé partagée: {cle_partagee_serveur}')
           
            clientSocket.close()
            
    else:
        if not args.IPv6:
            sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sockt = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            
        destination = (args.address, args.port)
        sockt.connect(destination)   
        
        # Le client recoit le modulo et la base du serveur
        a = int(recv_msg(sockt))
        b = int(recv_msg(sockt))
        print(f'Reception du modulo: {a}')
        print(f'Reception de la base: {b}')
        print("--------------------------------------------------------")
        
        # Le client recoit la clé publique du serveur
        cle_publique_recue = int(recv_msg(sockt))
        
        # Le client génère une clé privée
        cle_privee_client = entierAleatoire(a)
        
        # Le client calcule la clé publique
        cle_publique_client = exponentiationModulaire(b, cle_privee_client, a)
        
        # Le client calcule la clé partagée
        cle_partagee = exponentiationModulaire(cle_publique_recue, cle_privee_client, a)
        
        print(f'Clé privée : {cle_privee_client}')
        print(f'Clé publique à envoyer : {cle_publique_client}')
        
        # Le client envoie la clé publique au serveur
        send_msg(sockt, str(cle_publique_client))
        
        print(f'Clé publique recue: {cle_publique_recue}')
        print(f'Clé partagée: {cle_partagee}')
        
        sockt.close()
        
except socket.gaierror:
    file = open("Error.log", "w", encoding='utf8')
    file.write("Erreur soulevée à " + str(datetime.now()) + "\n" + "L’adresse est inaccessible")
    file.close()
    print("L’adresse est inaccessible, voir le fichier error.log")
except socket.error:
    file = open("Error.log", "w", encoding='utf8')
    file.write("Erreur soulevée à " + str(datetime.now()) + "\n" + "La connexion a été refusée")
    file.close()
    print("La connexion a été refusée, voir le fichier error.log")