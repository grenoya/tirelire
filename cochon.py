#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime

class Cochon():
    def __init__(self, nom, infoType):
        self.nom = nom
        self.montant = 0.0
        self.compte = ''
        while infoType not in ['cigale', 'fourmis', 'reste']:
            print("Le type '%s' n'est pas possible." % infoType)
            # le type reste n'est sensé être utilisé qu'une seule fois : depuis
            # l'initialisation de la tirelire
            print("Veuillez choisir entre : cigale (1) ou fourmis (2)")
            rep = raw_input()
            if rep == '1':
                infoType = 'cigale'
            elif rep == '2':
                infoType = 'fourmis'
                print(" a quel compte ce cochon est-il associé ?")
                compte = raw_input()
                self.compte = compte
            else:
                pass
        self.infoType = infoType
        print("creation du cochon : %s" % repr(self))

    def depose(self, montant):
        self.montant += montant

    def retire(self, montant):
        self.montant -= montant
        if self.montant < 0:
            print("ATTENTION ! vous etes en negatif sur ce cochon :")
            date = datetime.now()
            print(" %s : %s" % date, self.montant)

    def __repr__(self):
        message = "\t%s (%s) : %s\n" % (self.nom, self.infoType, self.montant)
        return message

if __name__ == "__main__":
    aaa = Cochon('toto')
