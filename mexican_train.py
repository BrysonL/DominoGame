from domino import Domino
from domino_player import DominoPlayer
from domino_train import DominoTrain
from domino_player_cpu import DominoPlayerCPU
from random import randint


class MexicanTrain:

    # to create a domino game, make the dominoes in every combination from 0 to 13 (Double 13 set)
    def __init__(self):
        self.dominoes = []
        self.center_domino = None
        self.players = []
        self.mexican_train = None

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
            print(current_player.name + "'s turn")
            # let the player play on their own train until they can't play any more
            while True:
                # if the player doesn't want to (or can't) play any more, let them end their turn
                attempted_play = current_player.play_on_train(train=self.players[player_turn]["train"],
                                                              center_domino=self.center_domino)
                if attempted_play is None:
                    print("Turn ended")
                    break

                # if the player's train hasn't started yet, their play should start their train
                if self.players[player_turn]["train"] is None:
                    if attempted_play.match(self.center_domino):
                        if attempted_play.num2 == self.center_domino.num1:
                            attempted_play.flip()
                        self.players[player_turn]["train"] = DominoTrain(attempted_play)
                    else:
                        print("That domino can't play")
                        current_player.add_domino(attempted_play)
                        continue
                # if the player's train has already started, their play should add to their train
                elif not self.players[player_turn]["train"].add_domino(attempted_play):
                    print("That domino can't play")
                    current_player.add_domino(attempted_play)
                    continue
                print("Domino added")
                print("Your new train: ", self.players[player_turn]["train"])

        # track some stats about the match
        total_turns = len(self.players)
        passes = 0
        plays = 0
        last_play_turn = 0
        draw = False

        # the game continues until someone uses all their dominoes
        while 0 not in [len(p["player"].hand) for p in self.players]:
            # track which trains the player can play on
            playable_trains = {}
            # the next player gets to play, and reset the count at the last player
            player_turn += 1
            player_turn %= len(player_list)
            total_turns += 1

            # if the game goes on too long, it's a draw
            # (there are better ways to determine this, but I 80/20'd it
            if total_turns > 1000:
                print("too many turns, assuming a draw")
                draw = True
                break

            # display the current trains
            current_player = self.players[player_turn]["player"]
            print(current_player.name + "'s turn")
            print("Your train: ", self.players[player_turn]["train"])
            if self.mexican_train is None:
                print("The Mexican Train hasn't started yet")
            else:
                print("The Mexican Train is: ", self.mexican_train)
            playable_trains["__self"] = self.players[player_turn]["train"]

            playable_trains["__mexican_train"] = self.mexican_train

            # if someone else's train is marked, you can play on them
            marked_trains = []
            for p in self.players:
                if p["train"] is None or p["player"] == current_player:
                    continue
                elif p["train"].is_marked:
                    print(p["player"].name + "'s train is marked: ", p["train"])
                    marked_trains.append(p["train"])
                    # note this implementation will have problems if a player's name is __self or __mexican_train
                    playable_trains[p["player"].name] = p["train"]

            # let the player play a maximum of once
            while True:
                # since there are multiple trains the player could play on, we need to know the train and the domino
                # they select
                play_dict = current_player.play_on_trains(trains=playable_trains,
                                                          center_domino=self.center_domino)
                if play_dict is None:
                    print("Turn skipped, drawing domino and marking train")
                    self.draw_domino(current_player)
                    # if the player decides not to play, mark their train
                    if self.players[player_turn]["train"] is not None:
                        self.players[player_turn]["train"].mark()
                    passes += 1
                    break

                # store the train they want to play on and the domino they want to play for easy access
                train_to_play = playable_trains[play_dict["train_key"]]
                attempted_play = play_dict["domino"]

                # if the train hasn't started yet, start it
                if train_to_play is None:
                    if attempted_play.match(self.center_domino):
                        if attempted_play.num2 == self.center_domino.num1:
                            attempted_play.flip()
                        if play_dict["train_key"] == "__self":
                            self.players[player_turn]["train"] = DominoTrain(attempted_play)
                        elif play_dict["train_key"] == "__mexican_train":
                            self.mexican_train = DominoTrain(attempted_play)
                        break
                    else:
                        print("That domino can't play")
                        current_player.add_domino(attempted_play)
                # if their domino can play on the existing train, play it
                elif not train_to_play.add_domino(attempted_play):
                    print("That domino can't play")
                    current_player.add_domino(attempted_play)
                    continue

                print("Play successful. New train:", train_to_play)
                plays += 1
                last_play_turn = total_turns
                if play_dict["train_key"] == "__self":
                    self.players[player_turn]["train"].unmark()

                break

        # if the game ended in a draw, print that
        if draw:
            print("The match was a draw")

        # print the hand of each player
        for p in self.players:
            if len(p['player'].hand) == 0:
                print(p["player"].name, "wins!")
            else:
                print(p["player"].name, "'s hand", ' '.join(str(d) for d in p["player"].hand))

        # we'll say the game "ended" when the last play was made
        # this is the same as the total_turns unless it was a draw
        print("Total turns: ", last_play_turn)
        print("Total times around: ", round(last_play_turn / len(self.players)))
        print("Plays: ", plays)
        print("Passes: ", passes)


game = MexicanTrain()

p1 = DominoPlayerCPU("p1")
p2 = DominoPlayerCPU("p2")

game.play_game([p1, p2])
