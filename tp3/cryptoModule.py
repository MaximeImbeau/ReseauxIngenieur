#importez ces fonctions dans votre fichier avec 
#" from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire "
#assurez-vous que les fichiers sont tous dans le meme repertoire

#generateur de nombres aleatoires
#disclaimer: en cryptographie, les nombres doivent etre impossible a deviner, ce qui n'est pas le cas ici
#ne pas utiliser dans des contextes reels
import random

#nombre de bits des nombres premiers generes. 
#plus ce nombre est grand, plus le protocole est securitaire, mais plus les operations sont lentes
#pour ce tp on utilisera toujours 128 bits
nbBits = 128

def entierAleatoire(modulo):
	#Genere un entier completement aleatoire entre 0 (inclus) et modulo (exclu)
	#Parametres:
	# - modulo: int
	return random.randrange(modulo)

def estProbablementPremier(n):
	#Methode utilitaire pour trouverNombrePremier (n'appelez pas cette fonction vous-meme!)
	#Teste si un nombre n est premier grace au test de fermat
	#Parametres:
	# - n: int
	if n in [0, 1]:
		return False
	elif n in [2, 3]:
		return True
	else:
		a = random.randint(2, n-2)
		return pow(a, n-1, n) == 1

def trouverNombrePremier():
	#Trouve un nombre premier de nbBits bits
	n = 0
	while not estProbablementPremier(n):
		n = random.getrandbits(nbBits)
	return n

def exponentiationModulaire(base, exposant, modulo):
	#Calcule base^exposant mod modulo
	#Parametres:
	# - base: int
	# - exposant: int
	# - modulo: int
	if modulo == 1:
		return 0
	resultat = 1
	base = base % modulo
	while exposant > 0:
		if exposant % 2 == 1:
		   resultat = (resultat * base) % modulo
		exposant = exposant >> 1
		base = (base ** 2) % modulo
	return resultat

