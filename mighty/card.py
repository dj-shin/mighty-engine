# pyright: strict
from enum import Enum
from typing import Any, Optional, Union


class Shape(Enum):
    H = 'heart'
    D = 'diamond'
    C = 'clover'
    S = 'spade'


class CardBase:
    def is_mighty(self, kiru: Optional[Shape]) -> bool:
        raise NotImplementedError

    def deal_score(self, kiru: Optional[Shape]) -> int:
        raise NotImplementedError

    def score(self) -> int:
        raise NotImplementedError


class NormalCard(CardBase):
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

    def __init__(self, shape: Shape, number: int) -> None:
        super().__init__()
        self.shape = shape
        self.number = number

    def is_mighty(self, kiru: Optional[Shape]) -> bool:
        return (kiru == Shape.S and self.shape == Shape.D and self.number == 14)\
                or (kiru != Shape.S and self.shape == Shape.S and self.number == 14)

    def deal_score(self, kiru: Optional[Shape]) -> int:
        if self.is_mighty(kiru):
            return 0
        elif self.number >= 10:
            return 1
        else:
            return 0

    def score(self) -> int:
        if self.number >= 10:
            return 1
        else:
            return 0

    def __repr__(self) -> str:
        return '({} {})'.format(self.shape.value, self.NUM_MAP[self.number])

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NormalCard):
            return self.shape == other.shape and self.number == other.number
        return False

    def __hash__(self):
        return hash(self.shape) ^ hash(self.number)

    def is_joker_call(self, kiru: Optional[Shape]) -> bool:
        if kiru == Shape.C:
            return self.shape == Shape.H and self.number == 3
        else:
            return self.shape == Shape.C and self.number == 3


class Joker(CardBase):
    def __init__(self) -> None:
        super().__init__()
        self.shape = None
        self.number = None

    def is_mighty(self, kiru: Optional[Shape]) -> bool:
        return False

    def deal_score(self, kiru: Optional[Shape]) -> int:
        return -1

    def score(self) -> int:
        return 0

    def __repr__(self) -> str:
        return '(Joker)'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Joker)

    def __hash__(self):
        return hash('Joker') ^ hash('joker')


Card = Union[NormalCard, Joker]
