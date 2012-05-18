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
    def __init__(self, nomTirelire):
        self.nom = nomTirelire + '.tir'
        if exists(self.nom):
            print("La tirelire existe deja, voulez-vous l'ecraser ? (o/N)")
            rep = raw_input()
            if rep.lower() != 'o':
                print("\n")
                exit()
            remove(self.nom)
        self.dateCreation = datetime.now()
        self.dateModification = datetime.now()
        self.fichiers = []
        self.comptes = {}
        self.cochons = {}
        self.ajouteCochon("Cagnote", "reste")
        self.distributions = {}

    def ajouteFichier(self, fichier):
        if not exists(fichier):
            print("Le fichier %s n'existe pas.\n" % fichier)
            exit()
        verifieFichier(self, fichier)
        self.fichiers.append(fichier)

    def ajouteCompte(self, nomCompte, typeCompte):
        if nomCompte in self.comptes:
            print("Le compte existe deja\n")
            exit()
        self.comptes[nomCompte] = Compte(nomCompte, typeCompte)

    def depotCompte(self, nomCompte, montant):
        if nomCompte not in self.comptes:
            print("Le compte n'existe pas\n")
            exit()
        self.comptes[nomCompte].depose(montant)

    def ajouteCochon(self, nomCochon, typeCochon):
        if nomCochon in self.cochons:
            print("Le cochon existe deja\n")
            exit()
        self.cochons[nomCochon] = Cochon(nomCochon, typeCochon)

    def depotCochon(self, nomCochon, montant):
        if nomCochon not in self.cochons:
            print("Le cochon n'existe pas\n")
            exit()
        if self.cochons[nomCochon].infoType is not "fourmis":
            print("Seule une fourmis peut apporter de l'argent !\n")
            print(repr(self.cochons[nomCochon]))
            exit()
        self.cochons[nomCochon].depose(montant)

    def retraitCochon(self, nomCochon, montant):
        if nomCochon not in self.cochons:
            print("Le cochon n'existe pas\n")
            exit()
        if self.cochons[nomCochon].infoType is not "cigale":
            print("Seule une cigale peut depenser de l'argent !\n")
            print(repr(self.cochons[nomCochon]))
            exit()
        self.cochons[nomCochon].retire(montant)

    def sauve(self):
        self.dateModification = datetime.now()
        fic = open(self.nom, 'w')
        dump(self, fic)
        fic.close()

    def upgrade(self):
        reference = Tirelire("ref")
        listeNomNouvelle = dir(reference)
        listeTypeNouvelle = [type(getattr(reference, elem)) 
            for elem in listeNomNouvelle]
        listeNomAncienne = dir(self)
        listeTypeAncienne = [type(getattr(self, elem)) 
            for elem in listeNomAncienne]
        if listeNomAncienne == listeNomNouvelle \
            and listeTypeAncienne == listeTypeAncienne:
            return
        print("Ancienne : %s\n %s" % (listeNomAncienne, listeTypeAncienne))
        print("Nouvelle : %s\n %s" % (listeNomNouvelle, listeTypeNouvelle))
        for elem in listeNomAncienne:
            if elem in listeNomNouvelle:
                # on vérifie que le type est le même
                if type(getattr(self, elem)) == type(getattr(reference, elem)):
                    # si oui on retire l'eleme de la liste nouvelle
                    listeNomNouvelle.remove(elem)
                    print("%s est ok !" % elem)
                else:
                    # sinon, on retire de self et de listeAncienne
                    listeNomAncienne.remove(elem)
                    delattr(self, elem)
                    print("%s n'avait pas le bon type" % elem)
            else:
                # on retire de self
                delattr(self, elem)
                print("%s est obsolette" % elem)
        for elem in listeNomNouvelle:
            if elem not in listeNomAncienne:
                # on ajoute l'element dans self
                setattr(self, elem, type(getattr(reference, elem)))
                print("nouveau %s" % elem)
        self.sauve()

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
        print("La tirelire %s n'existe pas.\n" % nom)
        exit()
    fic = open(nom, 'r')
    laTirelire = load(fic)
    fic.close()
#    laTirelire.upgrade()
    laTirelire.debutmoi()
    return laTirelire


if __name__ == "__main__":
    print("Tirelire !")
