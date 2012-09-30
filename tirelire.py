#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime
from os.path import exists, splitext
from os import remove
from pickle import dump, load
from boite import Boite


authorisedTransactions = {
    "Cochon Matelas": "Cochon Depense",
    "Cochon Matelas": "Cochon Virement",
    "Exterieur": "Cochon Matelas",
    "Cochon Depense": "Exterieur",
    "Cochon Depense": "Cochon Matelas",
    "Cochon Virement": "Cochon Matelas",
    "Cochon Virement": "Compte Epargne",
    "Compte Epargne": "Cochon Matelas",
    }


class Tirelire():

    @classmethod
    def new(cls, name, value, **kwargs):
        # Check the existance of a previus eponym Tirelire in the same directory
        # before creating it.
        if name.endswith('.tir'):
            filename = name
        else:
            filename = name + '.tir'

        if exists(filename):
            if "force" in kwargs:
                msg = "Tirelire %s already exists! use --force to rewrite it" \
                        % filename
                return -1, msg
            remove(filename)

        # TODO: verification of the value validity
        return Tirelire(filename, value)


    def __init__(self, name, value):
        self.ficname = name
        self.creationdate = datetime.now()
        self.courant = Boite("Courant", 0, "Compte Courant", self)
        self.exterieur = Boite("Exterieur", 0, "Exterieur", self)
        self.matelas = Boite("Matelas", value, "Cochon Matelas", self)
        self.boxes = []
        self.updateCourant()

    def updateCourant(self):
        self.courant.montant = self.matelas.montant
        for elem in self.boxes:
            if elem.info != "Epargne":
                self.courant.montant += elem.montant

    def addCompteEpargne(self, name, value, **kwargs):
        #TODO: check the validity of value
        # Add a Saving account to the Tirelire.
        for elem in self.boxes:
            if elem.name == name:
                if "force" in kwargs:
                    msg = "%s account already exists ! " \
                        + "use --force to remove it" % name
                    return -1, msg
                self.removeCompteEpargne(name)
        self.boxes.append(Boite(name, value, "Compte Epargne", self))
        return

    def addCochon(self, name, pigType, **kwargs):
        # Add a Cochon to the Tirelire.
        for elem in self.boxes:
            if elem.name == name:
                if "force" in kwargs:
                    msg = "%s pig already exists ! " \
                        + "use --force to remove it" % name
                    return -1, msg
                self.removeCochon(name)
        self.boxes.append(Boite(name, 0, pigType, self))
        return

    def removeBox(self, name, **kwargs):
        for elem in self.boxes:
            if elem.name == name:
                if "force" in kwargs:
                    msg = "Emptying %s %s before destruction" \
                            % (elem.info, elem.name)
                    self.transaction(elem.montant, elem, self.matelas, msg)
                    self.boxes.remove(elem)
                    return 1, "Box %s removed with force" % elem.name
                if elem.montant != 0:
                    return -2, "Box %s is not empty ! use --force" \
                        % elem.name
                self.boxes.remove(elem)
                return 1, "Box %s removed the soft way" % name

    def transaction(self, value, origin, destination, comment):
        # TODO: verification of the value validity
        if (origin.info, destination.info) in authorisedTransactions.items():
            origin.getMoney(value, destination, comment)
            destination.putMoney(value, origin, comment)

    def save(self):
        tirFile = open(self.ficname, 'w')
        dump(self, tirFile)
        tirFile.close()

    def summary(self, beginDate, **kwargs):
        #TODO: make the date optional
        # return all the transations since the given date.
        return ''

    def __repr__(self):
        # return the actual status of the Tirelire.
        message = "Tirelire %s cree le %s\n" % (self.ficname, self.creationdate)
        message += repr(self.courant)
        message += repr(self.matelas)
        for elem in self.boxes:
                message += repr(elem)
        return message


def loadTirelire(name):
    if splitext(name)[1] != '.tir':
        name += '.tir'
    if not exists(name):
        return 1, "The Tirelire %s doesn't exist." % name
    tirFile = open(name, 'r')
    tir = load(tirFile)
    tirFile.close()
    return tir


if __name__ == "__main__":
    tirtest = Tirelire()
    print(tirtest)

