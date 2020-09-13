from domino_player import DominoPlayer
from domino_train import DominoTrain
from domino import Domino


class DominoPlayerCPU(DominoPlayer):

    def play_on_train(self, train=None, center_domino=None):
        if train is not None and not isinstance(train, DominoTrain):
            raise TypeError
        if center_domino is not None and not isinstance(center_domino, Domino):
            raise TypeError
        if train is None and center_domino is None:
            raise ValueError

        if train is not None:
            for d in self.hand:
                if train.can_add_domino(d):
                    self.hand.remove(d)
                    return d
        elif center_domino is not None:
            for d in self.hand:
                if center_domino.match(d):
                    self.hand.remove(d)
                    return d



    def play_on_trains(self, trains, center_domino=None):
        if trains is not None and not isinstance(trains, dict):
            raise TypeError
        if center_domino is not None and not isinstance(center_domino, Domino):
            raise TypeError

        for key in trains:
            if trains[key] is not None and not isinstance(trains[key], DominoTrain):
                raise TypeError

            if trains[key] is not None:
                if True in [trains[key].can_add_domino(d) for d in self.hand]:
                    return {"train_key": key, "domino": self.play_on_train(trains[key])}
            elif True in [center_domino.match(d) for d in self.hand]:
                return {"train_key": key, "domino": self.play_on_train(train=None, center_domino=center_domino)}
