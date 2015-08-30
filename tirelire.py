#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Piggy bank application """
from __future__ import print_function
import shelve
from datetime import datetime
from datetime import date as dtdate


class Tirelire():
    """ Piggy bank """
    def __init__(self):
        #: Total amount
        self._total = 0.0
        #: List of pigs
        self._pig_names = []
        #: List of pig's amounts
        self._pig_amounts = []
        #: Remaining amount
        self._remaining = 0.0
        #: History of the total amount
        self._tirelire_history = []
        #: Pigs' history
        self._pigs_history = []
        #: Name of the backup file
        self._backup_filename = None

    def provision(self, amount, comment, date=None):
        """ Povide money to the Tirelire """
        date, msg = gereDate(date)
        self._total += amount
        self._remaining += amount
        self._tirelire_history.append((date, amount, "input",
                                        comment))
        self._pigs_history.append((date, amount, "input",
                                        comment))
        if msg:
            print(msg)
        return msg

    def createPig(self, name, date=None):
        """ Pig creation """
        date, msg = gereDate(date)
        self._pig_names.append(name)
        self._pig_amounts.append(0.0)
        self._pigs_history.append((date, None, "Pig creation",
                                        name))
        if msg:
            print(msg)
        return msg

    def feed(self, name, amount, date=None):
        """ Transfert money to the indicated pig """
        date, msg = gereDate(date)
        indice = self._pig_names.index(name)
        self._pig_amounts[indice] += amount
        self._remaining -= amount
        self._pigs_history.append((date, amount,
                                        "versement Cochon", name))
        if msg:
            print(msg)
        return msg

    def spend(self, name, amount, comment="", date=None):
        """ Spend money from a pig """
        date, msg = gereDate(date)
        indice = self._pig_names.index(name)
        self._pig_amounts[indice] -= amount
        self._total -= amount
        self._tirelire_history.append((date, amount, "outgo", comment))
        self._pigs_history.append((date, amount, "spend Cochon", name))
        if msg:
            print(msg)
        return msg

    def __repr__(self):
        """ Show pigs' state """
        msg = "Remaining: %f\n" % self._remaining
        msg += "---------\n"
        for elem in self._pig_names:
            msg += "%s: %f\n" % (elem, self._pig_amounts[self._pig_names.index(elem)])
        return msg[:-1]

    def showHistory(self):
        """ Show total amount history """
        for elem in self._tirelire_history:
            print("%s  %s | %s | %s" % elem)

    def save(self, name_fichier=None):
        """ Save Tirelire """
        if name_fichier:
            self._backup_filename = name_fichier
        fic = shelve.open(self._backup_filename)
        fic['Total'] = self._total
        fic['Pigs'] = self._pig_names
        fic['Amounts'] = self._pig_amounts
        fic['Remaining'] = self._remaining
        fic['GlobalHistory'] = self._tirelire_history
        fic['PigsHistory'] = self._pigs_history
        fic.close()

    def load(self, name_fichier):
        """ Load file """
        self._backup_filename = name_fichier
        fic = shelve.open(self._backup_filename)
        self._total = fic['Total']
        self._pig_names = fic['Pigs']
        self._pig_amounts = fic['Amounts']
        self._remaining = fic['Remaining']
        self._tirelire_history = fic['GlobalHistory']
        self._pigs_history = fic['PigsHistory']
        fic.close()


def gereDate(date):
    """ Return the date in Datetime format """
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
