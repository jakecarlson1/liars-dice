#!/usr/bin/env python
# Game
# By: Jake Carlson
# 2016-10-21

# imports
import players
import ld_bot

class Game(object):
    '''Game object manages the game. Maintians the list of players and manages
    the game logic.

    Attributes:
    _players - list of players in the game
    _ones_wild - boolean for whether ones are wild for the current round
    _total_num_dice - number of dice in the round
    _current_call - tuple representing the current call
    _quick_mode - controls whether the player is prompted to continue the game
            before dice are rolled
    '''

    # initializes a game object
    def __init__(self):
        self._players = []
        self._ones_wild = True
        self._num_dice = 0
        self._current_call = (0, 0)
        self._quick_mode = False
        self._cheat_mode = False

    # adds a player to the list of players, updates the numebr of dice
    def _add_player(self, pl):
        self._players.append(pl)
        self._num_dice = self._num_dice + 5

    # removes the player at index from the list of players
    def _remove_player_at(self, index):
        del self._players[index]

    # inivializes and runs a game using command line arguments as parameters
    def initialize_game_cmd_line(self, args):
        # args format: liars_dice.py -nb 5 -d 3 2 3 1 2 -q -c
        # -nb denotes the number of bots, -d lists the difficulty of the bots
        # -q flag makes the game run in "quick mode", there will be no pauses
        # between rounds (optional, default to false), -c flag puts the game in
        # "cheat mode" which will display everyones hand at the start of each
        # round

        nb_index = 0
        d_index = 0
        q_index = 0
        c_index = 0

        # grabs -nb (number of bots) flag
        if "-nb" in args:
            nb_index = args.index("-nb")
        else:
            print "-nb flag not specified"
        # checks that the values suppied is an integer
        if not is_int(args[nb_index + 1]):
            print "expected integer following -nb flag"

        # grabs -d (bot difficulties) flag
        if "-d" in args:
            d_index = args.index("-d")
        else:
            print "-d flag not specified"

        # grabs -q (quick mode) flag, updates quick mode if found
        if "-q" in args:
            q_index = args.index("-q")
            self._quick_mode = True

        # grabs the -c (cheat mode) flag, updates cheak mode if found
        if "-c" in args:
            c_index = args.index("-c")
            self._cheat_mode = True

        # adds the bots to the game
        for i in range(int(args[nb_index + 1])):
            d_index = d_index + 1
            try:
                if is_int(args[d_index]):
                    self._add_player(ld_bot.Bot(args[d_index]))
            except:
                print "number difficulties less than number of bots or integer not provided, default difficulty is 2"
                self._add_player(ld_bot.Bot(2))

    # gets human players, bots and bot difficulty, and adds them to the game
    def initialize_game(self):
        print "Welcome to Liars Dice!\n"

        # adding human players to the game
        person_count = raw_input("Enter the number of people: ")

        while not is_int(person_count):
            person_count = raw_input("Not a number, please enter a number: ")

        # allows players to set their name
        for i in range(int(person_count)):
            name = raw_input("Enter player " + str(i + 1) + "'s name: ")
            self._add_player(players.Person(name))

        # adding bot players to the game
        bot_count = raw_input("Enter the number of bots: ")

        while not is_int(bot_count):
            bot_count = raw_input("Not a number, please enter a number: ")

        # sets the difficulty for the bots
        for i in range(int(bot_count)):
            dif = raw_input("Specify the difficulty for the bot (1 - 3): ")
            while not is_int(dif) or int(dif) > 3 or int(dif) < 1:
                dif = raw_input("Invalid bot difficulty, please enter a number from 1 to 5: ")

            self._add_player(ld_bot.Bot(dif))

    # main game loop
    def run_game(self):
        # current player set to first player in the list
        current_player = 0
        self._setup_bots()

        while len(self._players) > 1:
            # call set to non-sense for placeholder first call
            self._current_call = (0, 0)
            self._ones_wild = True
            # waits for player input before starting the round
            if not self._quick_mode:
                raw_input("\nPress [enter] to continue.")
            current_player = self._play_round(current_player)

        print self._players[0].get_name() + " won the game!\n"

    # receives the player to start with and returns the player to start the next
    # round with, holds the main logic for a single round
    def _play_round(self, current_player):
        liar_called = False

        # rolls all of the players dice and prints the hands to the human players
        print "\n***roll dice***\n"

        # roll dice
        for pl in self._players:
            pl.roll_dice()

        # in cheat mode print all players in order of how many dice they have (most to least)
        if self._cheat_mode:
            sorted_players = sorted(self._players, key=lambda player: player.get_num_dice(), reverse=True)
            for pl in sorted_players:
                print pl.get_name()
                print str(pl.get_hand())
            print "\n"
        # otherwise print all of the players in the game and the number of dice they have
        else:
            for pl in self._players:
                print pl.get_name(), "has", len(pl.get_hand()), "dice"
            print "\n"

        # gets the first call
        call = self._players[current_player % len(self._players)].make_call(self._current_call, len(self._players), self._num_dice, False)

        # checks that the call if formatted correctly, the call cannot be liar
        while call == "liar" or not self._valid_call(call):
            print str(call) + " is not a valid call."
            call = self._players[current_player % len(self._players)].make_call(self._current_call, len(self._players), self._num_dice, False)

        print "\n" + self._players[current_player % len(self._players)].get_name() + " called " + str(call) + "\n"

        # if ones are called on the first call, they are not wild for the round
        if call[1] == 1:
            print "Ones were called on the first move, ones are not wild for this round."
            self._ones_wild = False

        # update _current_call
        self._current_call = call
        # update bots to new call here
        self._notify_bots_to_call(current_player % len(self._players))


        # the round runs until liar is called
        while not liar_called:
            # current_player is incremented
            current_player = current_player + 1

            # gets the next call from the current_player
            call = self._players[current_player % len(self._players)].make_call(self._current_call, len(self._players), self._num_dice, self._ones_wild)

            # checks that the call if formatted correctly
            while not self._valid_call(call):
                print str(call) + " is not a valid call."
                call = self._players[current_player % len(self._players)].make_call(self._current_call, len(self._players), self._num_dice, self._ones_wild)

            # prints the call for the rest of the players to see
            print self._players[current_player % len(self._players)].get_name() + " called " + str(call) + "\n"

            # if the call is liar, liar_called is updated so the round loop will end
            if call == "liar":
                liar_called = True
                print self._players[current_player % len(self._players)].get_name(), "called liar.\n"

            # _current_call will not be updated to liar, allowing it to be used in _evaluate_liar()
            else:
                self._current_call = call
                # update bots to new call here
                self._notify_bots_to_call(current_player % len(self._players))

        # the liar is evaluated
        current_player = self._evaluate_liar(current_player)
        return current_player

    # checks that the call is formatted correctly
    def _valid_call(self, call):
        # call must be liar
        if call == "liar":
            return True
        # the die called must be a number from 1 to 6
        elif call[1] > 6 or call[1] < 1:
            return False
        # if the quantity is the same, the value of the die face must increment
        elif call[1] > self._current_call[1] and call[0] == self._current_call[0]:
            return True
        # if the quantity changes, any die face may be called
        elif call[0] > self._current_call[0]:
            return True

    # sums all of the dice, the player that lied kicks in a die
    def _evaluate_liar(self, player_loc):
        limit = self._current_call[0]
        die = self._current_call[1]
        count = [0, 0, 0, 0, 0, 0]

        # sum all of the dice from each players hand
        for pl in self._players:
            hand = pl.get_hand()

            for d in hand:
                count[d - 1] = count[d - 1] + 1

        # the total dice are diplayed for the players
        print "Total dice:"
        for i in range(len(count)):
            print " die:", i + 1, " | count:", count[i]

        print "\nThe call was " + str(self._current_call) + "\n"

        total_for_die = count[die - 1]
        print "There are (" + str(total_for_die) + ", " + str(die) + ")."

        # if ones are wild the total number of ones is added to the total for the desired die
        if die != 1 and self._ones_wild:
            total_for_die = total_for_die + count[0]
            print "With ones, there are (" + str(total_for_die) + ", " + str(die) + ")."

        # the player who called liar is a location player_loc

        # player who called liar kicks in
        if total_for_die >= limit:
            self._players[player_loc  % len(self._players)].kick_in()

            # update bots to kick in here
            self._notify_bots_to_liar(player_loc  % len(self._players))

            if self._players[player_loc % len(self._players)].get_num_dice() == 0:
                self._remove_player_at(player_loc % len(self._players))
                # start of the next round goes to the player after the one eliminated
                player_loc = player_loc + 1

        # player with the standing call kicks in
        else:
            self._players[(player_loc - 1) % len(self._players)].kick_in()

            # update bots to kick in here
            self._notify_bots_to_liar((player_loc - 1) % len(self._players))

            if self._players[(player_loc - 1) % len(self._players)].get_num_dice() == 0:
                self._remove_player_at((player_loc - 1) % len(self._players))
            else:
                player_loc = player_loc - 1

        # number of dice is decremented
        self._num_dice = self._num_dice - 1

        return player_loc

    # initializes bots of difficulty 3
    def _setup_bots(self):
        for pl in self._players:
            if isinstance(pl, ld_bot.Bot):
                pl.gen_opp_list(len(self._players), self._players.index(pl))

    # notifies bots of difficulty 3 to new calls and the player who made them
    def _notify_bots_to_call(self, index):
        for pl in self._players:
            if isinstance(pl, ld_bot.Bot):
                pl.add_call_to_opp(self._current_call, index)

    # notifies bots to the player who kicked in a die
    def _notify_bots_to_liar(self, index):
        for pl in self._players:
            if isinstance(pl, ld_bot.Bot):
                pl.opp_kick_in(index)

# returns True if the input can be cast to an integer, False otherwise
def is_int(i):
    try:
        int(i)
        return True
    except:
        return False
