# Nom d'équipiers :                                               Matricule:
# Vincent-Gabriel Proulx                                          111 268 023
# Maxime Imbeau                                                   111 186 939
# Jean-Philippe Pepin                                             111 224 495

import socket
import select
import re
import os
import smtplib
from socketUtils import recv_msg, send_msg
from hashlib import sha512
from email.mime.text import MIMEText

ENTETE_RECEPTION_CREATION = "CREATION"
ENTETE_RECEPTION_CONNECTER = "CONNECTER"
ENTETE_RECEPTION_CONSULTER = "CONSULTER"
ENTETE_RECEPTION_OBTENTION = "OBTENTION"
ENTETE_RECEPTION_ENVOI = "ENVOI"
ENTETE_RECEPTION_STATISTIQUE = "STATISTIQUE"

REPONSE_VALIDE_CREATION_COMPTE = "Création du compte réussi."
REPONSE_INVALIDE_CREATION_COMPTE = "Création du compte échoué.\n"
REPONSE_VALIDE_CONNEXION_COMPTE = "Connexion du compte réussi."
REPONSE_INVALIDE_CONNEXION_COMPTE = "Connexion du compte échoué.\n"
REPONSE_VALIDE_ENVOI_COURRIEL = "Envoi du courriel réussi."
REPONSE_INVALIDE_ENVOI_COURRIEL = "Envoi du courriel échoué."
REPONSE_INVALIDE_CONSULTATION_COURRIEL = "Consultation du courriel échoué."
REPONSE_INVALIDE_OBTENTION_COURRIEL = "Obtention du courriel échoué."
REPONSE_INVALIDE_STATISTIQUE_COMPTE = "Obtention des statistiques échoué."

ERREUR_UTILISATEUR_EXISTANT = "Utilisateur existant."
ERREUR_UTILISATEUR_INEXISTANT = "Utilisateur inexistant."
ERREUR_FORMAT_MOT_PASSE_INVALIDE = "Veuillez entrer un mot de passe qui contient entre 8 et 20 caractères, dont au moins un chiffre, deux lettres majuscules, deux lettres minuscules."
ERREUR_MOT_DE_PASSE_INVALIDE = "Mot de passe incorrecte."

NOM_DOSSIER_ERREUR = "ERREUR"
NOM_FICHIER_MOT_DE_PASSE = "password.txt"

cheminProjet = os.getcwd()

socServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socServeur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socServeur.bind(("localhost", 1234))
socServeur.listen()

listeClients = []
listeAttente = []

if (os.path.isdir(NOM_DOSSIER_ERREUR) == False):
    os.mkdir(NOM_DOSSIER_ERREUR)

def creationEmail(socClient, nomUtilisateur, motDePasse):
    try:
        if (os.path.isdir(nomUtilisateur)):
            send_msg(socClient, REPONSE_INVALIDE_CREATION_COMPTE + ERREUR_UTILISATEUR_EXISTANT)
        else:
            if (re.search(r"^(?=.{8,20}$)(?=(?:.*?[A-Z]){2})(?=(?:.*?[a-z]){2})(?=(?:.*?[0-9]){1}).*$", motDePasse)):
                motDePasseHacher = sha512(motDePasse.encode()).hexdigest()
                os.mkdir(nomUtilisateur)
                os.chdir(nomUtilisateur)
                file = open(NOM_FICHIER_MOT_DE_PASSE, "w", encoding ="utf8")
                file.write(motDePasseHacher)
                file.close()
                os.chdir(cheminProjet)
                send_msg(socClient, REPONSE_VALIDE_CREATION_COMPTE)
            else:
                send_msg(socClient, REPONSE_INVALIDE_CREATION_COMPTE + ERREUR_FORMAT_MOT_PASSE_INVALIDE)
    except:
        send_msg(socClient, REPONSE_INVALIDE_CREATION_COMPTE)
    listeClients.remove(socClient)
    socClient.close()

def connexionEmail(socClient, nomUtilisateur, motDePasse):
    try:
        if (os.path.isdir(nomUtilisateur)):
            os.chdir(nomUtilisateur)
            motDePasseHacher = sha512(motDePasse.encode()).hexdigest()
            file = open(NOM_FICHIER_MOT_DE_PASSE)
            motDePasseUtilisateur = file.readline()
            if(motDePasseUtilisateur == motDePasseHacher):
                send_msg(socClient, REPONSE_VALIDE_CONNEXION_COMPTE)
            else:
                send_msg(socClient, REPONSE_INVALIDE_CONNEXION_COMPTE + ERREUR_MOT_DE_PASSE_INVALIDE)
            os.chdir(cheminProjet)
        else:
            send_msg(socClient, REPONSE_INVALIDE_CONNEXION_COMPTE + ERREUR_UTILISATEUR_INEXISTANT)
    except:
        send_msg(socClient, REPONSE_INVALIDE_CONNEXION_COMPTE)
    listeClients.remove(socClient)
    socClient.close()

def envoiCourriel(socClient, adresseReception, adresseDestination, sujet, corpsMessage):
    try:
        [nomUtilisateur, adresseInterne] = adresseDestination.split('@', 1)
        courriel = MIMEText(corpsMessage)
        courriel["From"] = adresseReception
        courriel["To"] = adresseDestination
        courriel["Subject"] = sujet
        if(adresseInterne == "ift.glo2000.ca"):
            if (os.path.isdir(nomUtilisateur)):
                os.chdir(nomUtilisateur)
            else:
                os.chdir(NOM_DOSSIER_ERREUR)
            filename = sujet + ".txt"
            file = open(filename, "w", encoding ="utf8")
            file.write(courriel.as_string())
            file.close()
            os.chdir(cheminProjet)
            send_msg(socClient, REPONSE_VALIDE_ENVOI_COURRIEL)
        else:
            smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
            smtpConnection.sendmail(courriel["From"], courriel["To"], courriel.as_string())
            smtpConnection.quit()
            send_msg(socClient, REPONSE_INVALIDE_ENVOI_COURRIEL)
    except:
        send_msg(socClient, REPONSE_INVALIDE_ENVOI_COURRIEL)
    listeClients.remove(socClient)
    socClient.close()

def consultationCourriel(socClient, nomUtilisateur):
    try:
        listFileName = ''
        i = 0
        listFile = os.listdir(nomUtilisateur)
        listFile.remove(NOM_FICHIER_MOT_DE_PASSE)
        for file in listFile:
            filename = file.split('.')[0]
            if(len(listFile) - 1 != i):
                listFileName = listFileName + filename + '|'
            else:
                listFileName = listFileName + filename
            i += 1
    except:
        send_msg(socClient, REPONSE_INVALIDE_CONSULTATION_COURRIEL)
    send_msg(socClient, listFileName)
    listeClients.remove(socClient)
    socClient.close()

def obtentionCourriel(socClient, nomUtilisateur, index):
    try:
        listFile = os.listdir(nomUtilisateur)
        os.chdir(nomUtilisateur)
        i = 1
        listFile.remove(NOM_FICHIER_MOT_DE_PASSE)
        courriel = ""
        for file in listFile:
            if(int(index) == i):
                courriel = open(file).read()
                send_msg(socClient, courriel)
                os.chdir(cheminProjet)
                break
            i += 1
    except:
        send_msg(socClient, REPONSE_INVALIDE_OBTENTION_COURRIEL)
    listeClients.remove(socClient)
    socClient.close()

def statistiqueCompte(socClient, nomUtilisateur):
    try:
        listFile = os.listdir(nomUtilisateur)
        listeSujet = ""
        os.chdir(nomUtilisateur)
        tailleTotale = os.path.getsize(NOM_FICHIER_MOT_DE_PASSE)
        i = 0
        listFile.remove(NOM_FICHIER_MOT_DE_PASSE)
        for file in listFile:
            tailleTotale += os.path.getsize(file)
            filename = file.split('.')[0]
            if(len(listFile) - 1 != i):
                listeSujet = listeSujet + filename + ', '
            else:
                listeSujet = listeSujet + filename
            i += 1
        os.chdir(cheminProjet)
        infoCompte = "Nombre de(s) message(s): " + str(len(listFile)) + "\nTaille totale du dossier: " + str(tailleTotale) +"\nListe de(s) message(s) par sujet: " + listeSujet
        send_msg(socClient, infoCompte)
    except:
        send_msg(socClient, REPONSE_INVALIDE_STATISTIQUE_COMPTE)
    listeClients.remove(socClient)
    socClient.close()

while True:
    (listeAttente, _, _) = select.select([socServeur] + listeClients, [], [])
    for soc in listeAttente:
        if soc == socServeur:
            (nouveauClient, _) = socServeur.accept()
            listeClients.append(nouveauClient)
        else:
            message = recv_msg(soc)
            try:
                [entete, contenu1, contenu2, contenu3, contenu4] = message.split("|", maxsplit=4)
            except AttributeError:
                listeClients.remove(soc)
            if(entete == ENTETE_RECEPTION_CREATION):
                creationEmail(soc, contenu1, contenu2)
            else:
                if(entete == ENTETE_RECEPTION_CONNECTER):
                    connexionEmail(soc, contenu1, contenu2)
                else:
                    if(entete == ENTETE_RECEPTION_CONSULTER):
                        consultationCourriel(soc, contenu1)
                    else:
                        if(entete == ENTETE_RECEPTION_OBTENTION):
                            obtentionCourriel(soc, contenu1, contenu2)
                        else:
                            if(entete == ENTETE_RECEPTION_ENVOI):
                                envoiCourriel(soc, contenu1, contenu2, contenu3, contenu4)
                            else:
                                if(entete == ENTETE_RECEPTION_STATISTIQUE):
                                    statistiqueCompte(soc, contenu1)