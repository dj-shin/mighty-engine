# pyright: strict
from .card import Shape


class Action:
    pass


class JokerCall(Action):
    def __init__(self, effect: bool):
        super().__init__()
        self.effect = effect


class JokerShape(Action):
    def __init__(self, shape: Shape):
        super().__init__()
        self.shape = shape
