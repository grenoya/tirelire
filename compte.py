#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime

class Compte():
    def __init__(self, nom, infoType):
        self.nom = nom
        self.montant = 0.0
        while infoType not in ['courant', 'epargne']:
            print("Le type '%s' n'est pas possible." % infoType)
            print("Veuillez choisir entre : courant (1) ou epargne (2)")
            rep = raw_input()
            if rep == '1':
                infoType = 'courant'
            elif rep == '2':
                infoType = 'epargne'
            else:
                pass
        self.infoType = infoType
        print("creation du compte : %s" % repr(self))

    def depose(self, montant):
        self.montant += montant

    def retire(self, montant):
        self.montant -= montant
        if self.montant < 0:
            print("ATTENTION ! vous etes en negatif sur ce compte :")
            date = datetime.now()
            print(" %s : %s" % date, self.montant)

    def __repr__(self):
        message = "\t%s (%s) : %s\n" % (self.nom, self.infoType, self.montant)
        return message

if __name__ == "__main__":
    aa = Compte('aa', 'zut')
