Liars Dice
Jake Carlson
CSE 3353

My goal for this project was to create a liars dice game with a companion bot that was capable of playing the game. I wanted the bot to have several difficulty levels. Each level used a unique method for generating calls to play the game. 

If you are unfamiliar with the rules for liars dice, they have been provided here.

The rules for liars dice:
1. All players start with 5 six-sided dice.
2. At the start of a round, all players roll their dice and may view their hand.
3. A player is chosen to start, that player makes a call.
4. A call is a quantity of same-sided dice (e.g. 3 fives).
5. The order of play is counterclockwise.
6. On a players turn, they must either up the call by calling something higher than the current call, or call the previous player a liar showing that they believe the quantity of dice called exceeds the actual number of that sided die on the table.
7. When a player calls liar, all players show their hands and the total number of the desired die are determined. If the number of dice is greater than or equal to the quantity called, the player who called liar kicks in a die. If the number of dice is less than the quantity called, the player who made the call kicks in a die.
8. The player who kicked in a die starts the next round.
9. The last player with dice left is the winner.
10. Ones are wild unless called on the first call.

I originally aimed to develop five difficulty levels for the bot. The easiest difficult for the bot would simply up the call by one or call liar if the quantity of dice called exceeded 1/6th of the total number of dice (1/3rd if ones are wild). This difficulty level was meant to be useful primarily while building the game itself as these are simple behaviors to code. I wanted the highest difficulty bot to build profiles for the players it is playing against and use those profiles to determine the best call to make.

The first step in this project was completing a Game class what would contain coded representations of all of the rules for the game above. The Game class is responsible for adding both human and bot players to the game, making sure calls made by those players are valid, and determining the player that needs to kick in a die when “liar” is called.

The Game class was fairly straightforward to implement. A lot of the size of the Game class is dedicated to handling user input, making sure calls are valid, and formatting output so that the game looks clean and fun to play in a terminal. When I transitioned to developing the different difficulties for the bots, I decided to add a way to initialize an instance of the game using command line arguments so that I could use the Game class as more of a test bed for building the bot.

The easy difficulty for the bot was the easiest to implement. Based on the number of dice in the game (n), a set of all valid calls (C) can immediately be determined:
	C = {(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,1), (2,2), …, (n,6)}
The easy difficulty bot uses this set to determine what to call next. If the threshold for the bot to call “liar” is not met, the bot determines the index of the current call and simply calls the next call in the set. If ones are wild, the bot will not call ones.

Because the behaviors of the bot on easy are so simple (they do not even consider the dice the bot has in their hand) if a game consists only of easy bots, they will each raise the call by one until, eventually, the threshold is met and one of them calls “liar”. The easy bot can also easily be made to call “liar” if you call something with a high quantity. This is reasonable for large games (most players have lost of their dice), but can be exploited in small games (a majority of the dice have been kicked in).

I aimed to remedy this behavior in the medium difficulty where bots will make the best call that they have in their hand. They will call what they are holding if they have a higher than average (number of dice / number of players) quantity of a certain die in their hand. If the medium difficulty bot calls first, it calls the die it is holding the most of and assumes every other player has at least one of that die in their hand. Again, this is a reasonable strategy for large games, but this breaks down for small games where medium bots can make somewhat outrageous calls if all of the players only have one or two dice in their hands. 

Playing a game with a mix of easy and medium bots is pretty fun though. Their simple behaviors can still make it difficult to confidently make a call, especially if you know that the player after you is going to call you a liar no matter what die you’re calling. But both of these difficulties struggle with small games and it’s usually pretty easy to eliminate all remaining players once a majority of the dice have been kicked in. Because of time constraints I decided to cut the number of difficulties down from five to three. The hard difficulty bot would still build profiles for the other players to use when making calls, but it would also play large games differently than small games.

The hard difficult bot maintains a list of _Opponent objects during a round. Every time a new call is made, the bot records the call in the _Opponent object corresponding to the player who made the call. When it’s the bot’s turn to call, it analyzes all of the calls made on each die and compares the most frequently called die to the dice in its hand and the call made by the player before it. If the bot holds a few of the most frequently called die for the round it will up the call on that die. Because the hard difficulty handles large and small games differently, it uses a more aggressive threshold for when it will call “liar” during large games. This is a trait that is wanted for large games only as it was the main reason medium and easy difficulty bots could throw games away once they got small enough. A bot on hard also uses a unique strategy once it is down to only one die in its hand which is designed to put other players in difficult spots. It does this by calling sixes first. The player that follows is forced to increase the quantity which should be avoided in small games.

The hardest part of this project was representing all of the different behaviors in code. The bots use a lot of nested conditionals (particularly in hard mode) for determining the calls to make. Coming up with the conditional statements to make the bots work as desired was difficult. Changing the order of the conditionals can have a large effect on how well the bot plays liars dice.

That being said, the hard mode is pretty effective at playing the game. I’ve lost to hard mode twice now, once where the rest of the bots were also on hard and once where the rest were a mix of easy and medium bots. A bot on hard mode is also capable of wining a game with more than one die left in its hand. In this way, my project has met my expectations.

If I were to extend this project, I would want to add another difficulty mode. Right now, the bot on hard mode only considers the calls made on the round being played. It clears the list of calls made on the round by its opponents after the round ends. I would want to extend the opponent profiling to include calls made on previous rounds. I believe that the calls from the previous rounds can be used to determine the thresholds the other players have for calling liar (both bot and human). Once this metric is determined, it can be used to determine the likelihood that the player after the bot would call liar on the call the bot would make.



Liars Dice Bot, 2016
- built a liars dice game that came with a bot that could play the game
- the bot featured three difficulty levels that each implemented a different strategy for playing the game
- the easy difficulty determined when to call “liar” using a basic statistical analysis of the state of the game
- the medium difficulties determined considered its own hand when determining when to call “liar”
- the hard difficulty used a profiling system to profile opponents and make calls based on what the rest of the players were calling
