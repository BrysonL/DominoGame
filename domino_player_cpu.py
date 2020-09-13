from domino_player import DominoPlayer


class DominoPlayerCPU(DominoPlayer):

    def play_on_train(self, train, center_domino=None):
        print("here in cpu class")
        return super().play_on_train(train, center_domino)

    def play_on_trains(self, trains, center_domino=None):
        print("here in cpu class")
        return super().play_on_trains(trains, center_domino)