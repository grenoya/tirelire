#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from os.path import exists, splitext
from os import remove
from datetime import datetime
from pickle import dump, load
from compte import Compte
from cochon import Cochon
from distribution import verifieFichier


class Tirelire():

    @classmethod
    def new(name):
        if exists(name):
            print("La tirelire existe deja, voulez-vous l'ecraser ? (o/N)")
            rep = raw_input()
            if rep.lower() != 'o':
                print("\n")
                return
            remove(name)
        tirelire = Tirelire(name)
        return tirelire

    def __init__(self, nomTirelire):
        self.nom = nomTirelire + '.tir'
        self.dateCreation = datetime.now()
        self.dateModification = datetime.now()
        self.fichiers = []
        self.comptes = {}
        self.cochons = {}
        self.ajouteCochon("Cagnote", "reste")
        self.distributions = {}

    def ajouteFichier(self, fichier):
        if not exists(fichier):
            return 1, "Le fichier %s n'existe pas." % fichier
        verifieFichier(self, fichier)
        self.fichiers.append(fichier)
        return 0, "Le fichier %s a ete ajoute." % fichier

    def ajouteCompte(self, nomCompte, typeCompte):
        if nomCompte in self.comptes:
            return 1, "Le compte %s existe deja." % nomCompte
        self.comptes[nomCompte] = Compte(nomCompte, typeCompte)
        return 0, "Le compte %s a ete cree." % nomCompte

    def depotCompte(self, nomCompte, montant):
        if nomCompte not in self.comptes:
            return 1, "Le compte %s n'existe pas." % nomCompte
        self.comptes[nomCompte].depose(montant)
        return 0, "Le montant %s a ete depose sur le compte %s." % \
            (montant, nomCompte)

    def ajouteCochon(self, nomCochon, typeCochon):
        if nomCochon in self.cochons:
            return 1, "Le cochon %s existe deja." % nomCochon
        self.cochons[nomCochon] = Cochon(nomCochon, typeCochon)
        return 0, "Le cochon %s a ete cree." % nomCochon

    def depotCochon(self, nomCochon, montant):
        if nomCochon not in self.cochons:
            return 1, "Le cochon %s n'existe pas." % nomCochon
        self.cochons[nomCochon].depose(montant)
        return 0, "Le montant %s a ete depose sur le cochon %s." % \
            (montant, nomCochon)

    def retraitCochon(self, nomCochon, montant):
        if nomCochon not in self.cochons:
            return 1, "Le cochon %s n'existe pas." % nomCochon
            exit()
        if self.cochons[nomCochon].infoType is not "stock":
            return 2, "Action impossible depuis ce type de cochon : %s." % \
                self.cochons[nomCochon].infoType
        self.cochons[nomCochon].retire(montant)
        return 0, "Le montant %s a ete retire du le cochon %s." % \
            (montant, nomCochon)

    def sauve(self):
        self.dateModification = datetime.now()
        fic = open(self.nom, 'w')
        dump(self, fic)
        fic.close()

#    def upgrade(self):
#        reference = Tirelire("ref")
#        listeNomNouvelle = dir(reference)
#        listeTypeNouvelle = [type(getattr(reference, elem)) 
#            for elem in listeNomNouvelle]
#        listeNomAncienne = dir(self)
#        listeTypeAncienne = [type(getattr(self, elem)) 
#            for elem in listeNomAncienne]
#        if listeNomAncienne == listeNomNouvelle \
#            and listeTypeAncienne == listeTypeAncienne:
#            return
#        print("Ancienne : %s\n %s" % (listeNomAncienne, listeTypeAncienne))
#        print("Nouvelle : %s\n %s" % (listeNomNouvelle, listeTypeNouvelle))
#        for elem in listeNomAncienne:
#            if elem in listeNomNouvelle:
#                # on vérifie que le type est le même
#                if type(getattr(self, elem)) == type(getattr(reference, elem)):
#                    # si oui on retire l'eleme de la liste nouvelle
#                    listeNomNouvelle.remove(elem)
#                    print("%s est ok !" % elem)
#                else:
#                    # sinon, on retire de self et de listeAncienne
#                    listeNomAncienne.remove(elem)
#                    delattr(self, elem)
#                    print("%s n'avait pas le bon type" % elem)
#            else:
#                # on retire de self
#                delattr(self, elem)
#                print("%s est obsolette" % elem)
#        for elem in listeNomNouvelle:
#            if elem not in listeNomAncienne:
#                # on ajoute l'element dans self
#                setattr(self, elem, type(getattr(reference, elem)))
#                print("nouveau %s" % elem)
#        self.sauve()

    def debutmoi(self):
        date = datetime.now()
        if date.month > self.dateModification.month:
            # on parcourt la liste des distributions
            for elem in self.distributions:
                # on retranche du cochon "reste" pour déposer dans les cochons
                self.comptes["reste"].retire(elem.montant)
                self.cochons[elem.cochon].depose(elem.montant)
            self.sauve()

    def __repr__(self):
        message = "Tirelire %s cree le %s\n" % (self.nom, self.dateCreation)
        message += "Derniere modification le %s\n" % self.dateModification
        if len(self.comptes) != 0:
            message += "Comptes de la tirelire :\n"
            for elem in self.comptes.values():
                message += repr(elem)
        if len(self.cochons) != 0:
            message += "Cochons de la tirelire :\n"
            for elem in self.cochons.values():
                message += repr(elem)
        return message


def chargeTirelire(nom):
    if splitext(nom)[1] != '.tir':
        nom += '.tir'
    if not exists(nom):
        return 1, "La tirelire %s n'existe pas." % nom
    fic = open(nom, 'r')
    laTirelire = load(fic)
    fic.close()
#    laTirelire.upgrade()
    laTirelire.debutmoi()
    return laTirelire


if __name__ == "__main__":
    print("Tirelire !")
    tirelire = Tirelire.new("example")
