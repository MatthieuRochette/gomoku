#!/usr/bin/env python -u
from gomoku import *

pbrain = Brain()
pbrain.start_loop()

# Nt = 5 - len(ligne) avec Nt lignes ayant les extrémités libres
# Donc si Nt + len(ligne) = 5 -> alors on valeur = +-3
# Echelle définitive:
# 0: aucun impact connu
# 1: donne un petit avantage (n'assure pas la victoire)
# 2: coup qui assure la victoire à t + 1 (= au tour suivant)
# 3: un coup gagnant
#
# si chiffre positif: bon pour nous
# si chiffre négatif: bon pour l'adversaire
#
# algo vise toujours le plus haut (garder le 1er plus grand en mémoire)
# utiliser une map de string qui représente la board a un tour t
# algo de minmax (avec alpha/beta pruning si possible) (récursif)
# à chaque tour qu'on joue:
# - calculer les p tours suivants possibles pour une profondeur n:
#   p = 0
#   alread_finished_turns = x
#   max_turns = 19**2
#   for i in range(n):
#     p *= max_turns - already_finished_turns - i
#
# https://www.youtube.com/watch?v=l-hh51ncgDI
# https://svn.code.sf.net/p/piskvork/code/trunk/source/doc/protocl2en.htm
