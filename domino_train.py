from domino import Domino

class DominoTrain:

    # a train is a connection of dominoes that have matching numbers at each intersection of dominoes
    def __init__(self, first_domino):
        if not isinstance(first_domino, Domino):
            raise TypeError

        self.train = [first_domino]
        self.is_marked = False

    def __str__(self):
        return ' '.join(str(d) for d in self.train)

    # mark the train so others can play on it
    def mark(self):
        self.is_marked = True

    # unmark the train so others can't play on it
    def unmark(self):
        self.is_marked = False

    # to add a domino to a train, it must match the last domino in the train
    def add_domino(self, domino):
        if not isinstance(domino, Domino):
            raise TypeError

        # the last domino in the train is the one at the end of the list
        last_domino = self.train[-1]

        # if the either the first or last number of the new domino matches the last number of the last domino,
        # it can be added to the list
        if domino.num1 == last_domino.num2:
            self.train.append(domino)
            return True

        if domino.num2 == last_domino.num2:
            domino.flip()
            self.train.append(domino)
            return True

        # if the new domino doesn't match, it can't be added to the list
        return False

    # in order to add a domino to the train, first or last number of the new domino must
    # match the last number of the last domino
    def can_add_domino(self, domino):
        if not isinstance(domino, Domino):
            raise TypeError

        last_domino = self.train[-1]
        if domino.num1 == last_domino.num2:
            return True

        if domino.num2 == last_domino.num2:
            return True

        return False

