from domino import Domino
from domino_player import DominoPlayer
from domino_train import DominoTrain
from random import(randint)


class MexicanTrain:

    # to create a domino game, make the dominoes in every combination from 0 to 13 (Double 13 set)
    def __init__(self):
        self.dominoes = []
        self.center_domino = None
        self.is_marked = False
        self.players = []

        # create all the dominoes
        for i in range(0, 13):
            # to prevent creating duplicates, the second loop starts wherever the first loop is
            for j in range(i, 13):
                self.dominoes.append(Domino(i, j))

    # drawing a domino from the center
    def draw_domino(self, player):
        if not isinstance(player, DominoPlayer):
            raise TypeError

        # if we're out of dominoes in the center, you can't draw
        if len(self.dominoes) == 0:
            return False

        # pop a random domino from the middle and add it to the player's hand
        player.hand.append(self.dominoes.pop(randint(0, len(self.dominoes) - 1)))
        return True

    # to start the game, a player needs to draw a hand of dominoes
    def draw_hand(self, player, num_dominoes):
        if not isinstance(player, DominoPlayer):
            raise TypeError

        # you can't draw more dominoes than are in the pile
        if num_dominoes > len(self.dominoes):
            raise ValueError

        # make sure the player's hand is empty then draw the number of dominoes
        player.hand = []
        for i in range(0, num_dominoes):
            self.draw_domino(player)

    # put a domino in the center
    def set_center_domino(self, domino):
        if not isinstance(domino, Domino):
            raise TypeError

        # the center domino has to be a double
        if not domino.is_double():
            return False

        self.center_domino = domino

    # play the game of Mexican train
    def play_game(self, player_list):
        if not all(isinstance(p, DominoPlayer) for p in player_list):
            raise TypeError

        # set the number of dominoes in a hand based on the number of players
        num_players = len(player_list)
        if num_players < 2:
            print("Not enough players")
            return False
        elif num_players == 2:
            num_dominoes = 16
        elif num_players < 5:
            num_dominoes = 15
        else:
            num_dominoes = 12

        # initialize the player list and their trains
        for player in player_list:
            self.players.append({
                "player": player,
                "train": None
            })

        # draw hands and figure out who goes first
        highest_double = -1
        i = 0
        player_turn = -1
        # each player should draw a hand
        for p in self.players:
            player = p["player"]

            self.draw_hand(player, num_dominoes)

            # find the highest double in a player's hand
            hd = player.highest_double()

            # if this player's double is higher than any other player's double so far, they are set up to go first
            if hd is not None and hd > highest_double:
                highest_double = hd
                player_turn = i
            i += 1

        # if no one drew any doubles, draw one by one until someone draws a double
        if player_turn == -1:
            print("No doubles drawn, drawing one at a time")

            # as soon as a player draws a double, drawing stops and the game starts
            while player_turn == -1:
                i = 0
                for p in self.players:
                    player = p["player"]
                    self.draw_domino(player)
                    hd = player.highest_double()
                    if hd is not None:
                        highest_double = hd
                        player_turn = i
                        break
                    i += 1
                print("Drew around once")

        # set the center domino to the highest double drawn
        self.center_domino = Domino(highest_double, highest_double)
        print("Center Domino:", self.center_domino)

        # remove the center domino from the first player's hand
        print("Starting Player:", self.players[player_turn]["player"].name)
        self.players[player_turn]["player"].hand.remove(self.center_domino)

        # in the first turn, players can play as many dominoes as they want
        for i in range(0, num_players):
            # the next player gets to play, and reset the count at the last player
            player_turn += 1
            player_turn %= len(player_list)
            current_player = self.players[player_turn]["player"]

            # let the player play on their own train until they can't play any more
            while True:
                # if the player doesn't want to (or can't) play any more, let them end their turn
                ans = input("Would you like to play a domino? (y/N)")
                while ans not in ["y", "N"]:
                    ans = input("Please choose y or N")

                if ans == "N":
                    break

                # let the player choose a domino to play
                attempted_play = current_player.play_domino()
                if self.players[player_turn]["train"] is None:
                    if attempted_play.match(self.center_domino):
                        if(attempted_play.num2 == self.center_domino.num1):
                            attempted_play.flip()
                        self.players[player_turn]["train"] = DominoTrain(attempted_play)
                    else:
                        print("That domino can't play. Try again.")
                        continue
                else:
                    if not self.players[player_turn]["train"].add_domino(attempted_play):
                        print("That domino can't play. Try again.")
                        continue

                print("Domino added")
                print("Your new train: ", self.players[player_turn]["train"])


        # starting simple with a single train
        train = DominoTrain(self.center_domino)
        while 0 not in [len(player["player"].hand) for player in self.players]:
            player_turn += 1
            player_turn %= len(player_list)
            current_player = self.players[player_turn]["player"]
            attempted_play = current_player.play_domino()

            if train.can_add_domino(attempted_play):
                train.add_domino(attempted_play)
                print("Domino Added")
                print("Current train:", train)
            else:
                current_player.add_domino(attempted_play)
                print("Domino couldn't be added")


        # print the hand of each player
        for p in self.players:
            player = p["player"]
            print(' '.join(str(d) for d in player.hand))



game = MexicanTrain()

p1 = DominoPlayer("p1")
p2 = DominoPlayer("p2")

game.play_game([p1,p2])