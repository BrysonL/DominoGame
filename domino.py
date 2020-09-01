from random import randint

class Domino:

    # create a domino that has two numbers on it
    def __init__(self, num1 = None, num2 = None):
        # if either number is not provided, generate both randomly
        if num1 is None or num2 is None:
            num1 = randint(0, 12)
            num2 = randint(0, 12)

        # make sure the numbers are within a valid range (0-12)
        self.check_num(num1)
        self.check_num(num2)

        # set the numbers if they are valid
        self.num1 = num1
        self.num2 = num2

    # make sure the domino numbers are valid
    def check_num(self, num):
        # number must be between 0 and 12
        if num > 12 or num < 0:
            raise ValueError

    # print the domino
    def __str__(self):
        return "[" + str(self.num1) + "|" + str(self.num2) + "]"

    # "rotate" the domino by switching the positions of its two numbers
    def flip(self):
        z = self.num1
        self.num1 = self.num2
        self.num2 = z

    # check whether two dominoes can be paired next to each other
    def match(self, other_domino):
        if not isinstance(other_domino, Domino):
            return False

        # the domino matches if at least one side of the first domino matches at least one side of the second domino
        return True in self.check_matches(other_domino)

    # check which pairs of ends match between two dominoes
    def check_matches(self, other_domino):
        if not isinstance(other_domino, Domino):
            raise TypeError

        # check each pair of ends to see if they match
        # returns front_front, front_back, back_front, back_back
        return [(self.num1 == other_domino.num1), (self.num1 == other_domino.num2), (self.num2 == other_domino.num1), (self.num2 == other_domino.num2)]

    # check if two dominoes have the same two numbers
    def __eq__(self, other):
        if not isinstance(other, Domino):
            return False

        # check both orientations of the domino to see if it identical to another domino
        return (self.num1 == other.num1 and self.num2 == other.num2) or (self.num1 == other.num2 and self.num2 == other.num1)

    def is_double(self):
        return self.num1 == self.num2


# #Test out the domino class to see if it works
# #init a domino
# d1 = Domino(3, 5)
#
# #print the domino to the console
# print(d1)
#
# #flipping the domino
# d1.flip()
#
# #make sure the flip worked
# print(d1)
#
# #make another domino
# d2 = Domino(3, 3)
#
# #print it out to see if it worked
# print(d2)
#
# #check which sides match the first domino
# print(d1.check_matches(d2))
#
# #check if it matches at all
# print(d1.match(d2))
#
# #see if the dominos are the same
# print(d1 == d2)
