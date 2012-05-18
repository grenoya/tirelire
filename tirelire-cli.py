#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from argparse import ArgumentParser
from tirelire import Tirelire, chargeTirelire


def parseur():
    parser = ArgumentParser(description='Outil de finance domestique.')
    parser.add_argument('maTirelire',
                        type=str,
                        nargs='?',
                        help="Nom de la tirelire que vous souhaitez manipuler")
    # création de la Tirelire
    #  ./tirelire-cli --creer maTirelire
    #  ./tirelire-cli -c maTirelire
    parser.add_argument('--creer', '-c',
                        action='store_true',
                        help='cree la tirelire')
    # ajout d'un Compte à la Tirelire
    #  ./tirelire-cli maTirelire --ajoutecompte monCompte sonType
    #  ./tirelire-cli maTirelire -A monCompte sonType
    parser.add_argument('--ajoutecompte', '-A', 
                        nargs=2,
                        action='store',
                        help='ajoute à la tirelire un compte avec son type')
    # ajout d'un Cochon à la Tirelire
    #  ./tirelire-cli maTirelire --ajoutecochon monCochon sonType
    #  ./tirelire-cli maTirelire -a monCochon sonType
    parser.add_argument('--ajoutecochon', '-a', 
                        nargs=2,
                        action='store',
                        help='ajoute un cochon a la tirelire avec son type')
    # déposer de l'argent sur un Compte
    #  ./tirelire-cli maTirelire --deposecompte monCompte monMontant monBlabla
    #  ./tirelire-cli maTirelire -D monCompte monMontant monBlabla
    parser.add_argument('--deposecompte', '-D',
                        nargs=3,
                        action='store',
                        help='depose la somme sur le compte, avec un commentaire')
    # transférer manuellement de l'argent à un Cochon
    #  ./tirelire-cli maTirelire --transfert monCompte monCochon monMontant
    #  ./tirelire-cli maTirelire -t monCompte monCochon monMontant
    parser.add_argument('--transfert', '-t',
                        nargs=3,
                        action='store',
                        help='depose la somme sur le cochon depuis le compte')
    # dépenser l'argent d'un Cochon
    #  .tirelire-cli maTirelire --depensecochon monCochon monMontant monBlabla
    #  .tirelire-cli maTirelire -d monCochon monMontant monBlabla
    parser.add_argument('--depensecochon', '-r',
                        nargs=3,
                        action='store',
                        help='retire la somme sur le cochon, avec un commentaire')
    # ajout de transferts automatique via un fichier ini
    #  ./tirelire-cli maTirelire --fichier monFichier.ini
    #  ./tirelire-cli maTirelire -F monFichier.ini
    parser.add_argument('--fichier', '-F',
                        nargs=1,
                        action='store',
                        help='ajoute les transferts automatiques décris dans le fichier')
    # visualiser le contenu d'une Tirelire
    #  ./tirelire-cli maTirelire --voir
    #  ./tirelire-cli maTirelire -v
    parser.add_argument('--voir', '-v', '-V', 
                        action='store_true',
                        help="voir l'etat de la tirelire")

    args = parser.parse_args()
    return args


def actions(args):
    if args.creer:
        maTirelire = Tirelire(args.maTirelire)
    else:
        maTirelire = chargeTirelire(args.maTirelire)
        if args.ajoutecompte:
            maTirelire.ajouteCompte(args.ajoutecompte[0],
                                    args.ajoutecompte[1])
        elif args.ajoutecochon:
            maTirelire.ajouteCochon(args.ajoutecochon[0],
                                    args.ajoutecochon[1])
        elif args.deposecompte:
            montant = verifieMontant(args.deposecompte[1])
            maTirelire.depotCompte(args.deposecompte[0],
                                   montant,
                                   args.deposecompte[2])
        elif args.transfert:
            montant = verifieMontant(args.transfert[2])
            maTirelire.depotCochon(args.transfert[0],
                                   args.transfert[1],
                                   montant)
        elif args.depensecochon:
            montant = verifieMontant(args.depensecochon[1])
            maTirelire.depense(args.depensecochon[0],
                               montant,
                               args.depensecochon[2])
        elif args.fichier:
            maTirelire.ajouteFichier(args.fichier[0])
        elif args.voir:
            print(repr(maTirelire))
    maTirelire.sauve()
    return


def verifieMontant(montant):
    try: 
        valeur = float(montant)
    except ValueError:
        valeur = montant.replace(',', '.')
        try:
            valeur = float(valeur)
        except ValueError:
            print("Desole, je ne comprend pas la valeur indiquee\n")
            exit()
    return valeur


if __name__ == "__main__":
    print("Tirelire Command Line !")
    print("-----------------------\n")
    args = parseur()
    actions(args)
