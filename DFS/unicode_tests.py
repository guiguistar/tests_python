# coding: utf-8

import random
import os
"""
La convention est la suivante:
 - 0001 pour le demi-trait du haut
 - 0010 pour le demi-trait de droite
 - 0100 pour le demi-trait du bas
 - 1000 pour le demi-trait de gauche
"""
codes = [  0x20, # 0000 vide
         0x2575, # 0001 up
         0x2576, # 0010 right
         0x2514, # 0011 
         0x2577, # 0100 
         0x2502, # 
         0x250c,
         0x251c,
         0x2574,
         0x2518,
         0x2500,
         0x2534,
         0x2510,
         0x2524,
         0x252c,
         0x253c,
]
def grille_aleatoire(largeur,hauteur):
    for i in range(hauteur):
        ligne=''
        for j in range(largeur):
            clef_aleatoire = random.choice(list(codes))
            ligne += chr(codes[clef_aleatoire])
        print(ligne)

def creer_matrice(largeur,hauteur):
    matrice = []
    for i in range(hauteur):
        matrice.append([])
        for j in range(largeur):
            matrice[-1].append(0)
            #matrice[-1].append(0x20)
            #matrice[-1].append(chr(codes[random.choice(list(codes))]))
    return matrice

def afficher_matrice(matrice):
    os.system('cls' if os.name=='nt' else 'clear')
    for i in range(len(matrice)):
        #ligne = ''.join(chr(c) for c in matrice[i])
        ligne = ''.join(chr(codes[c]) for c in matrice[i])
        print(ligne)

def generer_profondeur(matrice):
    une_pile = []

    hauteur = len(matrice)
    largeur = len(matrice[0])

    i_0 = random.randrange(hauteur)
    j_0 = random.randrange(largeur)

    une_pile.append((i_0, j_0))

    while une_pile:
        i, j = une_pile[-1]

        #voisins_libres = 0
        
        #if u_libre(matrice,i,j): voisins_libres |= 1
        #if r_libre(matrice,i,j): voisins_libres |= 2
        #if d_libre(matrice,i,j): voisins_libres |= 4
        #if l_libre(matrice,i,j): voisins_libres |= 8

        voisins_libres = []
        
        if u_libre(matrice,i,j): voisins_libres.append((i-1,j))
        if r_libre(matrice,i,j): voisins_libres.append((i,j+1))
        if d_libre(matrice,i,j): voisins_libres.append((i+1,j))
        if l_libre(matrice,i,j): voisins_libres.append((i,j-1))

        #if u_libre(matrice,i,j): voisins_libres.append(1)
        #if r_libre(matrice,i,j): voisins_libres.append(2)
        #if d_libre(matrice,i,j): voisins_libres.append(4)
        #if l_libre(matrice,i,j): voisins_libres.append(8)

        random.shuffle(voisins_libres)
        
        #print('voisins_libres', voisins_libres)

        if voisins_libres:
            I, J = voisins_libres.pop()
            if (I,J) == (i-1,j):
                matrice[i][j] |= 1
                matrice[I][J] |= 4
            if (I,J) == (i,j+1):
                matrice[i][j] |= 2
                matrice[I][J] |= 8
            if (I,J) == (i+1,j):
                matrice[i][j] |= 4
                matrice[I][J] |= 1
            if (I,J) == (i,j-1):
                matrice[i][j] |= 8
                matrice[I][J] |= 2
                
            une_pile.append((I,J))

            afficher_matrice(matrice)
            print('matrice[i][j]:', matrice[i][j], 'len(une_pile):', len(une_pile))
            input()
        else:
            une_pile.pop()
            
def u_libre(matrice,i,j):
    return i > 0 and matrice[i-1][j] == 0
def r_libre(matrice,i,j):
    return j < len(matrice[0])-1 and matrice[i][j+1] == 0
def d_libre(matrice,i,j):
    return i < len(matrice)-1 and matrice[i+1][j] == 0
def l_libre(matrice,i,j):
    return j > 0 and matrice[i][j-1] == 0

def char_en_couple(c,i,j):
    if c == 'u': return (i-1,j)
    if c == 'r': return (i,j+1)
    if c == 'd': return (i+1,j)
    if c == 'l': return (i,j-1)

if __name__ == '__main__':

    #grille_aleatoire(100,15)
    matrice = creer_matrice(60,30)
    afficher_matrice(matrice)

    generer_profondeur(matrice)
