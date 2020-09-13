from domino import Domino
from domino_train import DominoTrain

class DominoPlayer:

    # a player has a hand, a train, and a name
    def __init__(self, name = None):
        if name is None:
            name = "Player X"

        self.hand = []
        self.name = name

        return

    # given a list of dominoes, set it as the player's hand
    def set_hand(self, domino_list):
        if not all(isinstance(d, Domino) for d in domino_list):
            raise TypeError

        self.hand = domino_list

    # add a domino to the player's hand
    def add_domino(self, domino):
        if not isinstance(domino, Domino):
            raise TypeError

        return self.hand.append(domino)

    # check each domino in the player's hand to find the highest double
    def highest_double(self):
        highest_double = -1

        for d in self.hand:
            if d.is_double():
                if d.num1 > highest_double:
                    highest_double = d.num1

        if highest_double == -1:
            return None

        return highest_double

    # ask the player which domino they'd like to add to the train
    def play_domino(self):
        print(' '.join((str(d) + str(self.hand.index(d)+1)) for d in self.hand))
        d_index = int(input("Which domino would you like to play? ")) - 1
        while not (0 <= d_index < len(self.hand)):
            d_index = int(input("Please choose a domino between 1 and " + str(len(self.hand)) + ": ")) - 1

        # make sure they want to use domino they selected
        ans = input("Are you sure you want to play " + str(self.hand[d_index]) + "? (y/N)")
        while ans not in ["y", "N"]:
            ans = input("Please choose y or N")

        # if they didn't want to add that domino, ask them again which domino they wanted to add
        if ans == "N":
            return None

        # if they wanted to play that domino, take it out of their hand and add it to the train
        return self.hand.pop(d_index)

    def play_on_train(self, train=None, center_domino=None):
        if train is not None and not isinstance(train, DominoTrain):
            raise TypeError
        if center_domino is not None and not isinstance(center_domino, Domino):
            raise TypeError

        # let the player choose a domino to play
        while True:
            ans = input("Would you like to play a domino? (y/N)")
            while ans not in ["y", "N"]:
                ans = input("Please choose y or N")

            if ans == "N":
                return None
            else:
                attempted_play = self.execute_play(train=train, center_domino=center_domino)
                if attempted_play is not None:
                    return attempted_play
                print("That domino can't play, try again.")

    def play_on_trains(self, trains, center_domino=None):
        if trains is not None and not isinstance(trains, dict):
            raise TypeError
        if center_domino is not None and not isinstance(center_domino, Domino):
            raise TypeError

        print("Which train would you like to play on?")
        i = 1
        input_dict = {}
        for key in trains:
            if trains[key] is not None and not isinstance(trains[key], DominoTrain):
                raise TypeError

            if key == "__self":
                print("[", i, "] Your train: ", trains[key])

            elif key == "__mexican_train":
                print("[", i, "] The Mexican Train: ", trains[key])

            else:
                print("[", i, "] ", key, "'s train: ", trains[key])

            input_dict[i] = key
            i += 1

        i -= 1

        while True:
            ans = input("Would you like to play a domino? (y/N)")
            while ans not in ["y", "N"]:
                ans = input("Please choose y or N")

            if ans == "N":
                return None
            else:
                train_choice = input("Choose which train you'd like to play on by entering a number between 1 and "
                                     + str(i) + ": ")
                while not 0 < int(train_choice) <= i:
                    train_choice = input("Choose a number between 1 and " + str(i) + ": ")

                attempted_play = self.execute_play(train=trains[input_dict[int(train_choice)]],
                                                   center_domino=center_domino)
                if attempted_play is not None:
                    return {"train_key": input_dict[int(train_choice)], "domino": attempted_play}




    def execute_play(self, train, center_domino):
        if train is not None and not isinstance(train, DominoTrain):
            raise TypeError
        if center_domino is not None and not isinstance(center_domino, Domino):
            raise TypeError

        attempted_play = self.play_domino()
        if attempted_play is None:
            return None
        if train is None:
            if attempted_play.match(center_domino):
                return attempted_play
            else:
                self.add_domino(attempted_play)

        elif train.can_add_domino(attempted_play):
            return attempted_play
        else:
            self.add_domino(attempted_play)
