Tirelire
********

*Tirelire* is a piggy bank software.
You can consider your Tirelire as pig breeding: the Tirelire will be composed of
several little pigs, one per expense field (Food, Home, Sport...).

Let's create our Tirelire with those 3 pigs::
    >>> from tirelire import Tirelire
    >>> myTirelire = Tirelire()
    >>> myTirelire.createPig("Food")
    >>> myTirelire.createPig("Home")
    >>> myTirelire.createPig("Sport")

When earning money, you will want to provision your Tirelire and distribute it
to your pigs (to feed them)::
    >>> myTirelire.provision(500., "salary")
    >>> myTirelire.feed("Home", 350.)
    >>> myTirelire.feed("Food", 100.)
    >>> myTirelire.feed("Sport", 25.)

Amounts of money can be assign to a pig, the remaining money will automatically
be put in a special pig called "Remaining".

Let's have a look at our Tirelire::
    >>> myTirelire
    Remaining: 25.000000
    ---------
    Food: 100.000000
    Home: 350.000000
    Sport: 25.000000

When the time has come, you will pay the home rent and buy some food::
    >>> myTirelire.spend("Home", 349., comment="Sept. rent")
    >>> myTirelire.spend("Food", 25.)
    >>> myTirelire
    Remaining: 25.000000
    ---------
    Food: 75.000000
    Home: 1.000000
    Sport: 25.000000

What about the history::
    >>> myTirelire.showHistory()
    2015-08-30  500.0 | input | salary
    2015-08-30  349.0 | outgo | Sept. rent
    2015-08-30  25.0 | outgo | 

Saving:: 
    >>> myTirelire.save("myTir")

Loading again::
    >>> loaded_Tirelire = Tirelire()
    >>> loaded_Tirelire.load("myTir")
    >>> loaded_Tirelire
    Remaining: 25.000000
    ---------
    Food: 75.000000
    Home: 1.000000
    Sport: 25.000000
    >>> loaded_Tirelire.showHistory()
    2015-08-30  500.0 | input | salary
    2015-08-30  349.0 | outgo | Sept. rent
    2015-08-30  25.0 | outgo | 

Saving under the same name::
    >>> loaded_Tirelire.save()

Or with another::
    >>> loaded_Tirelire.save("myTir2")
