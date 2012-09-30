#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime


class Boite():

    def __init__(self, name, value, info, parent):
        self.name = name
        self.montant = value
        self.creationDate = datetime.now()
        self.info = info
        if info in ["Cochon Matelas", "Cochon Depense", "Cochon Virement"]:
            self.history = parent.courant.history
        else:
            self.history = []

    def putMoney(self, value, origin, commentary):
        self.montant += value
        if self.info in ["Cochon Matelas", "Compte Epargne"]:
            self.history.append((datetime.now(), value, origin, commentary))

    def getMoney(self, value, destination, commentary):
        self.montant -= value
        if self.info in ["Compte Epargne", "Cochon Depense", "Cochon Virement"]:
            self.history.append((datetime.now(), - value, destination, commentary))

    def summary(self, beginDate, endDate):
        sumup = ""
        for elem in self.history:
            if beginDate < elem[0] < endDate:
                sumup += repr(elem)
        return sumup

    def __repr__(self):
        return "%s (%s) : %s\n" % (self.name, self.info, self.montant)


if __name__ == "__main__":
    bb = Boite("courant", 12000, "Compte Courant", ())
