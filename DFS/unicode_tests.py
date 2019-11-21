# coding: utf-8

import random
import os
import time
import argparse
import json

"""
La convention est la suivante:
 - 0001 pour le demi-trait du haut
 - 0010 pour le demi-trait de droite
 - 0100 pour le demi-trait du bas
 - 1000 pour le demi-trait de gauche
"""

# labyrinthe de la thèse de R. Coulom
vi = [[2, 10, 14,  8, 4],
      [4,  2, 15, 10, 13],
      [3, 10,  9,  2, 9]]

codes = [  0x20, # 0000 vide
         0x2575, # 0001 up
         0x2576, # 0010    right
         0x2514, # 0011 up right
         0x2577, # 0100          down 
         0x2502, # 0101 up       down
         0x250c, # 0110    right down
         0x251c, # 0111 up right down
         0x2574, # 1000               left
         0x2518, # 1001 up            left
         0x2500, # 1010    right      left
         0x2534, # 1011 up right      left
         0x2510, # 1100          down left
         0x2524, # 1101 up       down left
         0x252c, # 1110    right down left
         0x253c, # 1111 up right down left
]

codes_gras = [    0x20, # 0000 vide
                0x2579, # 0001 up
                0x257a, # 0010    right
                0x2517, # 0011 up right
                0x257b, # 0100          down 
                0x2503, # 0101 up       down
                0x250f, # 0110    right down
                0x2523, # 0111 up right down
                0x2578, # 1000               left
                0x251B, # 1001 up            left
                0x2501, # 1010    right      left
                0x253b, # 1011 up right      left
                0x2513, # 1100          down left
                0x252b, # 1101 up       down left
                0x2533, # 1110    right down left
                0x254b, # 1111 up right down left
]

codes_bruts = [ord(c) for c in '0123456789ABCDEF']

def creer_matrice_aleatoire(largeur,hauteur):
    matrice = [ [random.randrange(16) for j in range(largeur)] for i in range(hauteur)]
    return matrice

def creer_matrice(largeur,hauteur):
    matrice =[largeur*[0] for i in range(hauteur)]
    return matrice

def afficher_matrice(matrice,codes):
    os.system('cls' if os.name=='nt' else 'clear')
    resultat = ''
    for i in range(len(matrice)):
        ligne = ''.join(chr(codes[c]) for c in matrice[i])
        resultat += ligne + '\n'
    print(resultat,end='')

def sauvegarder_matrice(matrice):
    hauteur = len(matrice)
    largeur = len(matrice[0])

    with open('matrice_{}_{}.txt'.format(hauteur,largeur),'w') as f:
        for i in range(hauteur):
            for j in range(largeur):
                #f.write(str(matrice[i][j]).rjust(3))
                f.write(chr(codes[matrice[i][j]]))
                if j == largeur -1:
                    f.write('\n')

def charger_matrice(fichier,codes):
    matrice = []
    with open(fichier) as f:
        ligne = f.readline()
        matrice.append([codes.index(ord(c)) for c in list(ligne)[:-1]])
        while ligne:
            ligne = f.readline()
            matrice.append([codes.index(ord(c)) for c in list(ligne)[:-1]])
    return matrice
    
def generer_profondeur(matrice, display=False):
    une_pile = []

    hauteur = len(matrice)
    largeur = len(matrice[0])

    i_0 = random.randrange(hauteur)
    j_0 = random.randrange(largeur)

    une_pile.append((i_0, j_0))

    while une_pile:
        # On lit le point qu'il y a au sommet de la pile
        i, j = une_pile[-1]

        voisins_libres = []
        
        if u_libre(matrice,i,j): voisins_libres.append((i-1,j))
        if r_libre(matrice,i,j): voisins_libres.append((i,j+1))
        if d_libre(matrice,i,j): voisins_libres.append((i+1,j))
        if l_libre(matrice,i,j): voisins_libres.append((i,j-1))

        # On mélange les voisins libres
        random.shuffle(voisins_libres)
        
        #print('voisins_libres', voisins_libres)

        if voisins_libres:
            # On choisit un voisin libre
            I, J = voisins_libres.pop()
            
            if (I,J) == (i-1,j):
                matrice[i][j] |= 1 # ajout du demi-trait sur le noeud père
                matrice[I][J] |= 4 # ajout du demi-trait sur le noeud fils
            if (I,J) == (i,j+1):
                matrice[i][j] |= 2
                matrice[I][J] |= 8
            if (I,J) == (i+1,j):
                matrice[i][j] |= 4
                matrice[I][J] |= 1
            if (I,J) == (i,j-1):
                matrice[i][j] |= 8
                matrice[I][J] |= 2

            # On empile le voisin libre choisit
            une_pile.append((I,J))

            if display:
                afficher_matrice(matrice,codes)
                print('matrice[i][j]:{:2}, len(une_pile):{:3}'.format(matrice[i][j], len(une_pile)))
                time.sleep(0.01)

        # Si le sommet n'a pas de voisins libres, on le dépile
        else:
            une_pile.pop()

u_libre = lambda matrice, i, j: i > 0                 and matrice[i-1][j] == 0
r_libre = lambda matrice, i, j: j < len(matrice[0])-1 and matrice[i][j+1] == 0
d_libre = lambda matrice, i, j: i < len(matrice)-1    and matrice[i+1][j] == 0
l_libre = lambda matrice, i, j: j > 0                 and matrice[i][j-1] == 0

def parcourir_profondeur(matrice):
    afficher_matrice(matrice,codes)

def print_hexa_format():
    for i in range(16):
        description = ''
        if i == 1: description = '   up bit'
        if i == 2: description = 'right bit'
        if i == 4: description = ' down bit'
        if i == 8: description = ' left bit'
        print(hex(i)[2:].upper(), bin(i)[2:].rjust(4,'0'), chr(codes[i]),description)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("rows", type=int, help="number of rows of the maze")
    parser.add_argument("cols", type=int, help="number of columns of the maze")
    parser.add_argument("--display",
                        help="display the animation of the generation of the maze",
                        action="store_true")
    parser.add_argument("--json",
                        help="ouput stringified json 2d array",
                        action="store_true")
    parser.add_argument("--coulom",
                        help="maze from R. Coulom thesis",
                        action="store_true")
    parser.add_argument("--style", type=str,
                        help="should output be haxa codes or bold",
                        choices=["bold", "hexa"])
    args = parser.parse_args()

    # le constructeur prend (largeur, hauteur) en entrée
    matrice = creer_matrice(args.cols, args.rows)
    generer_profondeur(matrice, display=args.display)

    style = codes
    if args.style == "bold": style = codes_gras
    if args.style == "hexa": style = codes_bruts

    if args.coulom:
        matrice = vi
    
    if not args.json:
        afficher_matrice(matrice, codes=style)
    else:
        print(json.dumps(matrice, separators=(',',':')))
