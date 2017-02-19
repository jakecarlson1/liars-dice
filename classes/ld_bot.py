#!/usr/bin/env python
# ld_bot
# By: Jake Carlson
# 2016-10-20

# imports
import players

class Bot(players.Player):
    '''Bot inherits from Player. The Bot can play dice without a player telling
    it what moves to make.

    Attributes:
    _difficulty - difficulty level for the bot
    _call_set - set of all allowable calls the bot can make
    _opponents - list of _Opponent objects, each one representing a player the
            bot is playing, a reference to the bot is added at it's location in
            the list
    _last_updated_opp - index of the last opponent to make a call, when the bot
            makes it's call this will hold the index of player just before the bot
    '''

    # static class variable for the number of bots, used in naming.
    # the call set can be shared across all bots since it does not differ
    bot_count = 0
    _call_set = []

    # initializes the bot with the specified difficulty and a name based on the difficulty
    def __init__(self, dif):
        super(self.__class__, self).__init__()
        # increment static class variable
        Bot.bot_count = Bot.bot_count + 1
        # the bot's name is generated
        self._name = "Bot " + str(Bot.bot_count) + ", lvl " + str(dif)
        # sets the bot's difficulty
        self._difficulty = int(dif)
        # variables for hard difficulty are initialized
        self._opponents = []
        self._last_updated_opp = 0

    # the bot makes a call using the appropriate function for the bot's difficulty
    def make_call(self, call, num_pl, num_dice, wild):
        print "It's " + self._name + "'s turn."

        # bot will stop the round if more dice are called than exist in the game
        if call[0] > num_dice:
            return "liar"

        # easy mode
        if self._difficulty == 1:
            return self._easy(call, num_pl, num_dice, wild)

        # medium mode
        elif self._difficulty == 2:
            return self._medium(call, num_pl, num_dice, wild)

        # hard mode
        elif self._difficulty == 3:
            return self._hard(call, num_pl, num_dice, wild)

    # easy mode will increment the call by one or call liar if the quantity of
    # dice is greater than 1/6th the total dice (1/3rd if ones are wild)
    def _easy(self, call, num_pl, num_dice, wild):
        # _generate_call_set() will only execute if the list is empty,
        # saving the operations for subsequent easy() calls, however it needs to be
        # called for the largest value of num_dice
        if not self._call_set:
            self._generate_call_set(num_dice)

        # if the bot calls first they make the best call they can in their hand
        if call[0] == 0 and call[1] == 0:
            return self._get_most_frequent_die(wild)

        if wild:
            # checks if the threshold to call liar is met
            if call[0] > num_dice / 3:
                return "liar"
            else:
                # up the call
                return self._up_the_call(call, wild)
        else:
            # checks if the threshold to call liar is met
            if call[0] > num_dice / 6:
                return "liar"
            else:
                # up the call
                return self._up_the_call(call, wild)

    # increases the call by one using _call_set, will not call ones if they are wild
    def _up_the_call(self, call, wild):
        # finds the location the current call is at in the call set
        loc = self._call_set.index(call)

        # prevents calling ones if they are wild
        if wild:
            if self._call_set[loc + 1][1] is 1:
                return self._call_set[loc + 2]

        # returns the next call
        return self._call_set[loc + 1]

    # populates _call_set with all allowable calls based on the number of dice
    def _generate_call_set(self, num_dice):
        self._call_set
        # iterates over all combinations of quantities and dice
        for i in range(1, num_dice + 1):
            for j in range(1, 7):
                self._call_set.append((i, j))

    # returns the most frequent die in the bots hand
    def _get_most_frequent_die(self, wild):
        best = 0
        count = 0
        # steps from 6 to 1 to prevent calling ones if all dice are distinct
        for i in [6,5,4,3,2,1]:
            temp = self._hand.count(i)
            # updates count and best if a die with a higher count is found
            if temp > count:
                count = temp
                best = i

        # if ones are wild the count for the ones is added to the count to return
        if wild and best != 1:
            one_count = self._hand.count(1)
            count = count + one_count

        return (count, best)

    # medium mode will call the dice they have the most of or call liar if the
    # call conditions for _easy are satisfied unless the bot holds a larger than
    # average quantity of the dice to be called
    def _medium(self, call, num_pl, num_dice, wild):
        best_in_hand = self._get_most_frequent_die(wild)
        new_call = (best_in_hand[0] + num_pl - 1, best_in_hand[1])

        # if medium bot calls first, or if the current call has a lower quantity
        # than new call, it calls the most frequent die it has with a
        # and assumes every other player has at least one of that die
        if (call[0] == 0 and call[1] == 0) or call[0] < new_call[0]:
            return new_call

        # if the bot has a good hand it calls the best die it has at a higher
        # quantity than the current call
        if wild:
            if best_in_hand[0] > num_dice / num_pl:
                # no need to increment quantity if the die to be called is
                # greater than the die currently called
                if call[1] < best_in_hand[1]:
                    return (call[0], best_in_hand[1])
                else:
                    return (call[0] + 1, best_in_hand[1])
            else:
                return "liar"
        else:
            if best_in_hand[0] > num_dice / (2 * num_pl):
                # no need to increment quantity if the die to be called is
                # greater than the die currently called
                if call[1] < best_in_hand[1]:
                    return (call[0], best_in_hand[1])
                else:
                    return (call[0] + 1, best_in_hand[1])
            else:
                return "liar"

    # generates the opponent list for the bot
    def gen_opp_list(self, num_pl, my_index):
        if self._difficulty == 3:
            # adds a new opponent for each player
            for i in range(num_pl):
                # the bot adds a reference to itself at its location
                if i == my_index:
                    self._opponents.append(self)
                else:
                    self._opponents.append(_Opponent())

    # add the current call to the round list for the opponent who made the call
    def add_call_to_opp(self, call, opp_index):
        if self._difficulty == 3:
            # would not add a call to self
            if self._opponents[opp_index] is not self:
                self._opponents[opp_index].add_call(call)
                self._last_updated_opp = opp_index

    # mechanism for removing a die from the opponent who kicked in
    def opp_kick_in(self, opp_index):
        if self._difficulty == 3:
            # would not remove a die from self
            if self._opponents[opp_index] is not self:
                self._opponents[opp_index].kick_in()
                self._last_updated_opp = opp_index

                # removes the opponent if they are out of dice
                if self._opponents[opp_index].get_num_dice == 0:
                    del self._opponents[opp_index]

            # resets each opponents calls for the round
            for opp in self._opponents:
                if opp is not self:
                    opp.clear_calls()

    # a bot in _hard mode will profile opponents and base thier calls of of what
    # the table is playing. It tries to add up the number of a certain die out
    # there and call that. It also plays big and small games with different
    # strategies
    def _hard(self, call, num_pl, num_dice, wild):
        if num_dice / num_pl > 3 and self._num_dice >= 3:
            # uses medium level to call if the bot is calling first on a large game
            if call[0] == 0 and call[1] == 0:
                return self._medium(call, num_pl, num_dice, wild)
            # large game
            return self._hard_game_large(call, num_pl, num_dice, wild)

        else:
            # small game
            return self._hard_game_small(call, num_pl, num_dice, wild)

    # function for making calls on a large game
    def _hard_game_large(self, call, num_pl, num_dice, wild):
        # gets the call distribution for the current round
        call_distribution = self._get_call_distribution()
        table_favorite = (0,0,0)

        # get most frequently called die from the call distribution
        for i in range(len(call_distribution)):
            if table_favorite[1] < call_distribution[i][1]:
                table_favorite = call_distribution[i]

        # the direct opponent is the one who calls before the bot
        direct_opp_favorite = self._eval_direct_opp()

        # gets the number of the table's favorite die and the direct opponent's
        # favorite die in the bots hand
        table_fav_in_hand = 0
        opp_fav_in_hand = 0
        # if ones are wild the count of ones in the bots hand are added to the
        # count of the table favorite and the direct opponents favorite
        if wild:
            table_fav_in_hand = self._hand.count(table_favorite[0]) + self._hand.count(1)
            opp_fav_in_hand = self._hand.count(direct_opp_favorite[1]) + self._hand.count(1)
        else:
            table_fav_in_hand = self._hand.count(table_favorite[0])
            opp_fav_in_hand = self._hand.count(direct_opp_favorite[1])

        # if the direct opponent made a call with the table favorite the bot
        # ups the call
        if table_favorite[0] == direct_opp_favorite[1]:
            if table_fav_in_hand >= 2:
                return (call[0] + 1, table_favorite[0])
            else:
                return "liar"
        else:
            if opp_fav_in_hand < 2 or call[0] > 1.5 * num_dice / num_pl:
                return "liar"
            else:
                return self._medium(call, num_pl, num_dice, wild)

    # function for making calls on a small game
    def _hard_game_small(self, call, num_pl, num_dice, wild):
        direct_opp_favorite = self._eval_direct_opp()

        # bot uses a unique strategy when it only has one die left
        if len(self._hand) == 1:
            # starts off by calling sixes so the next player has to increase the quantity
            if call[0] == 0 and call[1] == 0:
                if num_dice > 6:
                    return (2, 6)
                else:
                    return (1, 6)

            # bot will up the call if it holds the die being called or if the
            # direct opponent holds more dice than called
            if self._hand[0] == call[1] or self._opponents[self._last_updated_opp].get_num_dice() - 2 > call[0]:
                return (call[0] + 1, call[1])

            # threshold for calling liar
            if call[0] > num_dice / 2:
                return "liar"

            # if the bot holds a wild one and the quantity does not need to be
            # increased the bot ups the call
            elif self._hand[0] == 1 and wild and call[1] != 6:
                return (call[0], call[1] + 1)

            # finally the bot will call what they hold
            else:
                if call[1] < self._hand[0]:
                    return (call[0], self._hand[0])
                else:
                    return "liar"

        # if the game is small but the bot holds more than one die
        else:
            # calls the best the bot holds
            if call[0] == 0 and call[1] == 0:
                return self._get_most_frequent_die(wild)

            # threshold for liar
            if call[0] > num_dice / 2:
                return "liar"

            # plays easy to avoid dramatically overcalling
            return self._easy(call, num_pl, num_dice, wild)

    # sums the number of calls for each die
    def _get_call_distribution(self):
        # each list in the distribution has the structure:
        # [die, count of calls for die, current max call for die]
        call_dist = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

        for opp in self._opponents:
            if opp is not self:
                for call in opp.get_round_calls():
                    # increment count of calls for die
                    call_dist[call[1] - 1][1] = call_dist[call[1] - 1][1] + 1
                    # save die being called
                    call_dist[call[1] - 1][0] = call[1]
                    # if the quantity of the call is greater than the current
                    # max call it is saved
                    if call[0] > call_dist[call[1] - 1][2]:
                        call_dist[call[1] - 1][2] = call[0]

        # convert to tuples (immutable)
        for i in range(len(call_dist)):
            call_dist[i] = tuple(call_dist[i])

        return call_dist

    # returns the die called most frequently by the opponent before the bot and
    # the quantity they last called that die at
    def _eval_direct_opp(self):
        # with self._opponents[self._last_updated_opp] as opp:
        opp = self._opponents[self._last_updated_opp]
        if opp is not self:

            # sums the number of calls for each die made by the direct opponent
            call_counts = [0,0,0,0,0,0]
            for call in opp.get_round_calls():
                call_counts[call[1] - 1] = call_counts[call[1] - 1] + 1

            result = [0, call_counts.index(max(call_counts)) + 1]

            # get quantity for most frequently called die
            for call in opp.get_round_calls():
                if call[1] == result[1] and call[0] > result[0]:
                    result[0] = call[0]

            return tuple(result)

# internal Opponent object for profiling players in _hard mode
class _Opponent(object):

    # initializes the opponent with 5 dice ane an empty list of round calls
    def __init__(self):
        self._num_dice = 5
        self._round_calls = []

    # adds a call to the opponents round calls
    def add_call(self, call):
        self._round_calls.append(call)

    # resets the list of round calls for the opponent
    def clear_calls(self):
        self._round_calls = []

    # removes a die from the opponents hand
    def kick_in(self):
        self._num_dice = self._num_dice - 1

    # returns the number of dice the opponent has
    def get_num_dice(self):
        return self._num_dice

    # returns the round calls for the opponent
    def get_round_calls(self):
        return self._round_calls
