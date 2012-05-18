#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

class Distribution():
    def __init__(self, cochon, montant):
        self.cochon = cochon
        self.montant = montant

    def __repr__(self):
        message = "\t%s (%s) : %s\n" % (self.nom, self.infoType, self.montant)
        return message

def verifieFichier(maTirelire, monFichier):
    fic = open(monFichier, 'r')
    for ligne in fic:
        if not ligne.startswith("#"):
            champ = ' '.join(ligne.split()[:-1])
            if champ not in maTirelire.cochons:
                print("Le cochon %s n'existe pas, voulez-vous le créer ?" %
                        champ)
                rep = ''
                while rep == '':
                    rep = raw_input("Non(N)/Cigale(C)/Fourmis(F)?")
                    if rep.lower() == 'c':
                        maTirelire.ajouteCochon(champ, 'cigale')
                    elif rep.lower() == 'f':
                        maTirelire.ajouteCochon(champ, 'fourmis')
                    elif rep.lower() == 'n':
                        pass
                    else:
                        rep = ''
    fic.close()
