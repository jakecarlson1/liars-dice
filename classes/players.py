#!/usr/bin/env python
# Players
# By: Jake Carlson
# 2016-10-21

# imports
import random

class Player(object):
    '''Base class for someone playing the game.

    Attributes:
    _hand - list of dice the player has
    _num_dice - number of dice the player has
    _name - name of the player
    '''

    # initializes the player with an empty hand, 5 dice, and no name
    def __init__(self):
        self._hand = []
        self._num_dice = 5
        self._name = ""

    # randomly generate _num_dice mane values from 1 to 6
    def roll_dice(self):
        self._hand = []
        for i in range(self._num_dice):
            self._hand.append(random.randint(1, 6))

    # decreases the number of dice the player has by 1
    def kick_in(self):
        print self._name + " kicks in a die."
        self._num_dice = self._num_dice - 1
        if self._num_dice == 0:
            print self._name + " is out of the game."

    # shows the player's hand
    def get_hand(self):
        return self._hand

    # gets the number of dice a player has
    def get_num_dice(self):
        return self._num_dice

    # gets the player's name
    def get_name(self):
        return self._name

class Person(Player):
    '''Person inherits from Player. The Person class implements the make_call()
    function which is the only functional difference between the Person and Bot
    subclasses.
    '''

    # calls the initializer for the base class and sets the players name
    def __init__(self, name):
        super(self.__class__, self).__init__()
        self._name = name

    # prompts the user with relevant information and asks them to make a call
    def make_call(self, call, num_pl, num_dice, wild):
        print "The call is " + str(call) + ", there are " + str(num_dice) + " dice, and " + str(num_pl) + " players in."
        if wild:
            print "Ones are wild."
        print "\nYour hand is: " +  str(self._hand)
        print "What is your call?\n"

        num = raw_input("Enter the number of dice or liar: ")
        while not is_int(num) :
            if num == "liar":
                return num
            num = raw_input("Not a valid number, please enter a number or liar: ")

        die = raw_input("Enter the die: ")
        while not is_int(die):
            die = raw_input("Invalid number, plese enter a number: ")

        return (int(num), int(die))

# returns True if the input can be cast to an integer, False otherwise
def is_int(i):
    try:
        int(i)
        return True
    except:
        return False
