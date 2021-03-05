def grille_art_ascii(ensemble):
    for indice, valeur in enumerate(ensemble):
        minimum_i = valeur[0]
        if valeur[0] < minimum_i:
            minimum_i = valeur[0]
        indice += 1
    
    indice = 0
    for indice, valeur in enumerate(ensemble):
        maximum_i = valeur[0]
        if valeur[0] > maximum_i:
            maximum_i = valeur[0]
        indice += 1
    for indice, valeur in enumerate(ensemble):
        minimum_j = valeur[1]
        indice = 0
        if valeur[1] < minimum_j:
            minimum_j = valeur[1]
            indice += 1
    for indice, valeur in enumerate(ensemble):
        maximum_j = valeur[1]
        indice = 0
        if valeur[1] > maximum_j:
            maximum_j = valeur[1]
            indice += 1
        
    print(minimum_i)
    print(maximum_i)
    print(minimum_j)
    print(maximum_j)
        
        
grille_art_ascii({(-1, 1), (1, 0), (1, -2), (2, 3)})