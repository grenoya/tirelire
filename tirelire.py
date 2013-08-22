#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Gestion simplifiée d'une tirelire """
from __future__ import print_function
import shelve
from datetime import datetime
from datetime import date as dtdate


class Cochons():
    """ Tirelire """
    def __init__(self):
        #: montant total possédé
        self._courant = 0.0
        #: liste des cochons
        self._noms = []
        #: montant des cochons
        self._montants = []
        #: montant non attribué à un cochon
        self._cagnotte = 0.0
        #: historique des mouvements du total possédé
        self._historiqueExterne = []
        #: historique des mouvements internes
        self._historiqueInterne = []
        #: nom du fichier de sauvegarde
        self._chemin = None

    def ajouteCourant(self, montant, commentaire, date=None):
        """ apport d'argent """
        date, msg = gereDate(date)
        self._courant += montant
        self._cagnotte += montant
        self._historiqueExterne.append((date, montant, "versement",
                                        commentaire))
        self._historiqueInterne.append((date, montant, "versement",
                                        commentaire))
        if msg:
            print(msg)
        return msg

    def ajouteCochon(self, nom, date=None):
        """ création d'un cochon """
        date, msg = gereDate(date)
        self._noms.append(nom)
        self._montants.append(0.0)
        self._historiqueInterne.append((date, None, "creation Cochon",
                                        nom))
        if msg:
            print(msg)
        return msg

    def verseCochon(self, nom, montant, date=None):
        """ versement d'argent de la cagnotte vers un cochon """
        date, msg = gereDate(date)
        indice = self._noms.index(nom)
        self._montants[indice] += montant
        self._cagnotte -= montant
        self._historiqueInterne.append((date, montant,
                                        "versement Cochon", nom))
        if msg:
            print(msg)
        return msg

    def depense(self, nom, montant, commentaire, date=None):
        """ depense l'argent d'un cochon """
        date, msg = gereDate(date)
        indice = self._noms.index(nom)
        self._montants[indice] -= montant
        self._courant -= montant
        self._historiqueExterne.append((date, montant, "depense", commentaire))
        self._historiqueInterne.append((date, montant, "depense Cochon", nom))
        if msg:
            print(msg)
        return msg

    def etatCochons(self):
        """ affiche l'état de chaque cochon """
        print("cagnotte: %f" % self._cagnotte)
        print("---------")
        for elem in self._noms:
            print("%s: %f" % (elem, self._montants[self._noms.index(elem)]))

    def afficheHistorique(self):
        """ affiche l'historique des recettes et dépenses """
        for elem in self._historiqueExterne:
            print("%s  %s | %s | %s" % elem)

    def sauve(self, nom_fichier=None):
        """ sauve la tirelire dans un fichier """
        if nom_fichier:
            self._chemin = nom_fichier
        fic = shelve.open(self._chemin)
        fic['courant'] = self._courant
        fic['noms'] = self._noms
        fic['montants'] = self._montants
        fic['cagnotte'] = self._cagnotte
        fic['historiqueExterne'] = self._historiqueExterne
        fic['historiqueInterne'] = self._historiqueInterne
        fic.close()

    def charge(self, nom_fichier):
        """ charge une tirelire depuis une sauvegarde """
        self._chemin = nom_fichier
        fic = shelve.open(self._chemin)
        self._courant = fic['courant']
        self._noms = fic['noms']
        self._montants = fic['montants']
        self._cagnotte = fic['cagnotte']
        self._historiqueExterne = fic['historiqueExterne']
        self._historiqueInterne = fic['historiqueInterne']
        fic.close()


def gereDate(date):
    """ Renvoie la sate fournie au format datetime """
    msg = None
    if not date:
        date = dtdate.today()
    else:
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            msg = "Date incomprehensible, on prend la date actuelle"
            date = dtdate.today()
    return date, msg
