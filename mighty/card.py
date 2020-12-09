from enum import Enum


class Shape(Enum):
    H = 'heart'
    D = 'diamond'
    C = 'clover'
    S = 'spade'


class Card:
    NUM_MAP = {
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A',
    }

    def __init__(self, shape, number, joker):
        self.shape = shape
        self.number = number
        self.joker = joker

    def is_mighty(self, kiru):
        return (kiru == Shape.S and self.shape == Shape.D and self.number == 14)\
                or (kiru != Shape.S and self.shape == Shape.S and self.number == 14)

    def deal_score(self, kiru):
        if self.joker:
            return -1
        elif self.is_mighty(kiru):
            return 0
        elif self.number >= 10:
            return 1
        else:
            return 0

    def score(self):
        if self.number >= 10:
            return 1
        else:
            return 0

    def __repr__(self):
        if self.joker:
            return '[Joker]'
        return '({} {})'.format(self.shape.value, self.NUM_MAP[self.number])


