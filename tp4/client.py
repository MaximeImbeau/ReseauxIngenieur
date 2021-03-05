# Nom d'équipiers :                                               Matricule:
# Vincent-Gabriel Proulx                                          111 268 023
# Maxime Imbeau                                                   111 186 939
# Jean-Philippe Pepin                                             111 224 495

import re
import socket
import getpass
import os
from socketUtils import recv_msg , send_msg

ENTETE_RECEPTION_CREATION = "CREATION"
ENTETE_RECEPTION_CONNECTER = "CONNECTER"
ENTETE_RECEPTION_CONSULTER = "CONSULTER"
ENTETE_RECEPTION_OBTENTION = "OBTENTION"
ENTETE_RECEPTION_ENVOI = "ENVOI"
ENTETE_RECEPTION_STATISTIQUE = "STATISTIQUE"

REPONSE_SERVEUR_VALIDE_CREATION_COMPTE = "Création du compte réussi."
REPONSE_VALIDE_CONNEXION_COMPTE = "Connexion du compte réussi."

nomUsageActif = ""
reponseIncorrect = True

while reponseIncorrect:
    print("\nMenu de connexion\n1. Creer un compte\n2. Se connecter\n")
    reponseConnexion = input("")
    if reponseConnexion == "1" or reponseConnexion == "2":
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(("localhost", 1234))
        nomUsager = input("\nEntrer le nom d'usager: ")
        motPasse = getpass.getpass('Entrer le mot de passe: ')
        if reponseConnexion == "1":
            message = ENTETE_RECEPTION_CREATION + '|' + nomUsager + '|' + motPasse + '|null|null'
        else:
            message = ENTETE_RECEPTION_CONNECTER + '|' + nomUsager + '|' + motPasse + '|null|null'
        send_msg(soc, message)
        reponse = recv_msg(soc)
        print("\n" + reponse)
        if(reponse == REPONSE_SERVEUR_VALIDE_CREATION_COMPTE or reponse == REPONSE_VALIDE_CONNEXION_COMPTE):
            reponseIncorrect = False
    else:
        print("\nCommande inconnue")

while True:
    print("\nMenu principal\n1. Consultation de courriels\n2. Envoi de courriels\n3. Statistiques\n4. Quitter\n")
    reponsePrincipal = input("")
    if reponsePrincipal == "1" or reponsePrincipal == "2" or reponsePrincipal == "3":
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(("localhost", 1234))
        if reponsePrincipal == "2":
            adresseReception = nomUsager + "@ift.glo2000.ca"
            adresseDestination = input("\nEntrer l\'adresse de destination: ")
            sujet = input("\nEntrer le sujet du message: ")
            corpsMessage = input("\nEntrer le corps du message: ")
            message = ENTETE_RECEPTION_ENVOI + '|' + adresseReception + '|' + adresseDestination + '|' + sujet + '|' + corpsMessage
            send_msg(soc, message)
            reponse = recv_msg(soc)
            print("\n" + reponse)
        else:
            if reponsePrincipal == "1":
                message = ENTETE_RECEPTION_CONSULTER + '|' + nomUsager + '|null|null|null'
                send_msg(soc, message)
                reponse = recv_msg(soc)
                i = 0
                listNomSujet = reponse.split('|')
                choixInvalide = True
                while choixInvalide:
                    i = 0
                    for sujet in listNomSujet:
                        i += 1
                        print("\n" + str(i) + ". " + sujet)
                    print("\n")
                    choixCourriel = input("")
                    if choixCourriel.isnumeric() and int(choixCourriel) <= i:
                        choixInvalide = False
                        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        soc.connect(("localhost", 1234))
                        message = ENTETE_RECEPTION_OBTENTION + '|' + nomUsager + '|' + choixCourriel + '|null|null'
                        send_msg(soc, message)
                        reponse = recv_msg(soc)
                        print("\n" + reponse)
                        entreeUtilisateur = input("\nAppuyer sur une touche pour aller vers le menu...")
                    else:
                        print("\nCommande inconnue")
            else:
                message = ENTETE_RECEPTION_STATISTIQUE + '|' + nomUsager + '|null|null|null'
                send_msg(soc, message)
                reponse = recv_msg(soc)
                print("\n" + reponse)
                entreeUtilisateur = input("\nAppuyer sur une touche pour aller vers le menu...")
    else:
        if reponsePrincipal == "4":
            break
        else:
            print("\nCommande inconnue")