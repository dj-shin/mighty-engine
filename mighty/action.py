# pyright: strict
from .card import Shape


class Action:
    pass


class JokerCall(Action):
    def __init__(self, effect: bool):
        super().__init__()
        self.effect = effect

    def __repr__(self) -> str:
        return '<JokerCall: {}>'.format(self.effect)


class JokerShape(Action):
    def __init__(self, shape: Shape):
        super().__init__()
        self.shape = shape

    def __repr__(self) -> str:
        return '<Joker: {}>'.format(self.shape.value)
