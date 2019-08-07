# coding: utf-8

import random
import os
"""
La convention est la suivante:
 - u pour le demi-trait du haut
 - r pour le demi-trait de droite
 - d pour le demi-trait du bas
 - l pour le demi-trait de gauche
"""

codes = {'lr':   0x2500,
         'du':   0x2502,
         'dr':   0x250C,
         'dl':   0x2510,
         'ru':   0x2514,
         'lu':   0x2518,
         'dru':  0x251C,
         'dlu':  0x2524,
         'dlr':  0x252C,
         'lru':  0x2534,
         'dlru': 0x253C,
         'l':    0x2574,
         'u':    0X2575,
         'r':    0x2576,
         'd':    0x2577,
         ' ':    0x20}

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
            matrice[-1].append(' ')
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
        i, j = une_pile.pop()

        voisins_occupes = matrice[i][j]
        voisins_libres = ''
        
        if u_libre(matrice,i,j): voisins_libres += 'u'
        if r_libre(matrice,i,j): voisins_libres += 'r'
        if d_libre(matrice,i,j): voisins_libres += 'd'
        if l_libre(matrice,i,j): voisins_libres += 'l'

        print('voisins_libres', voisins_libres)
        while voisins_libres:
            direction = random.choice(voisins_libres)
            voisins_libres = voisins_libres.replace(direction,'')
            
            une_pile.append(char_en_couple(direction,i,j))
            matrice[i][j] = ''.join(sorted(matrice[i][j] + direction)).strip()

            print('matrice[i][j]:', matrice[i][j], 'len(une_pile):', len(une_pile))
            input()
            afficher_matrice(matrice)
        
def u_libre(matrice,i,j):
    return i > 0 and matrice[i-1][j] == ' '
def r_libre(matrice,i,j):
    return j < len(matrice[0])-1 and matrice[i][j+1] == ' '
def d_libre(matrice,i,j):
    return i < len(matrice)-1 and matrice[i+1][j] == ' '
def l_libre(matrice,i,j):
    return j > 0 and matrice[i][j-1] == ' '

def char_en_couple(c,i,j):
    if c == 'u': return (i-1,j)
    if c == 'r': return (i,j+1)
    if c == 'd': return (i+1,j)
    if c == 'l': return (i,j-1)

if __name__ == '__main__':

    for clef in codes:
        code = codes[clef]
        print(hex(code),code,chr(code))

    #grille_aleatoire(100,15)
    matrice = creer_matrice(100,15)
    afficher_matrice(matrice)

    generer_profondeur(matrice)
