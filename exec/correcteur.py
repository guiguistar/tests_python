# coding: utf-8

import threading
import multiprocessing
import time

with open('eleve.py') as f:
    code1 = f.read()

with open('eleve2.py') as f:
    code2 = f.read()

def verifier_fonction(nom_fonction):
    if nom_fonction in globals():
        print('Fonction "{}" définie'.format(nom_fonction))
        print(une_fonction)
    else:
        print('Fonction "{}" non définie.'.format(nom_fonction))

def cible():
    while True:
        print('Bonjour, je suis la cible.')
        time.sleep(1)
        
verifier_fonction('une_fonction')
        
exec(code1)
une_fonction()

verifier_fonction('une_fonction')

#t1 = threading.Thread(target=lambda code:exec(code),args=(code2))
t1 = multiprocessing.Process(target=cible)
t1.start()
t1.join(5)

if t1.is_alive():
    t1.terminate()
    print('Delai depassé.')

#exec(code2)
#une_fonction()

verifier_fonction('une_fonction')
