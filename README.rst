Tirelire
********

Creation of an instance::
    >>> from tirelire import Cochons
    >>> myTirelire = Cochons()

Adding a pig::
    >>> myTirelire.ajouteCochon("First_Pig")
    >>> myTirelire.ajouteCochon("Second one", date="2013-08-22")
    >>> myTirelire.ajouteCochon("troisième")

Feeding a pig::
    >>> myTirelire.verseCochon("First_Pig", 10.)

Let's look at the state of it::
    >>> myTirelire.etatCochons()
    cagnotte: -10.000000
    ---------
    First_Pig: 10.000000
    Second one:	0.000000
    troisième: 0.000000

Oops!! We transfered money but none was availlable, let's tell how much is::
    >>> myTirelire.ajouteCourant(500., "salary", date="2013-08-21")
    >>> myTirelire.etatCochons()
    cagnotte: 490.000000
    ---------
    First_Pig: 10.000000
    Second one:	0.000000
    troisième: 0.000000

Time to spend the money::
    >>> myTirelire.depense("First_Pig", 2., "some bread")
    >>> myTirelire.etatCochons()
    cagnotte: 490.000000
    ---------
    First_Pig: 8.000000
    Second one:	0.000000
    troisième: 0.000000

What about the history::
    >>> myTirelire.afficheHistorique()
    2013-08-21  500.0 | versement | salary
    2013-08-22  2.0 | depense | some bread

Saving:: 
    >>> myTirelire.sauve("myTir")

Loading again::
    >>> loaded_Tirelire = Cochons()
    >>> loaded_Tirelire.charge("myTir.s")
    >>> loaded_Tirelire.depense("First_Pig", 2., "some bread")
    >>> loaded_Tirelire.afficheHistorique()
    2013-08-21  500.0 | versement | salary
    2013-08-22  2.0 | depense | some bread
    2013-08-22  2.0 | depense | some bread

Saving under the same name::
    >>> loaded_Tirelire.sauve()

Or with another::
    >>> loaded_Tirelire.sauve("myTir2")
