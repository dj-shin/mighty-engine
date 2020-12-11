# pyright: strict
from typing import List, Optional
from functools import cmp_to_key
from ..card import Shape, Card, Joker


Player = int


class PhaseBase:
    NUM_PLAYERS = 5

    def __init__(self, kiru: Optional[Shape], hands: List[List[Card]], turn_player: Player):
        self.kiru = kiru
        self._hands = hands
        self._turn_player = turn_player

    def _compare_card(self, a: Card, b: Card) -> int:
        if isinstance(a, Joker):
            return -1
        if isinstance(b, Joker):
            return 1

        if a.shape == self.kiru and b.shape != self.kiru:
            return -1
        if a.shape != self.kiru and b.shape == self.kiru:
            return 1
        if a.shape.value < b.shape.value:
            return -1
        elif a.shape.value > b.shape.value:
            return 1
        return b.number - a.number

    def hand(self, player: Player) -> List[Card]:
        return sorted(self._hands[player], key=cmp_to_key(lambda x, y: self._compare_card(x, y)))

    def turn_player(self) -> Player:
        return self._turn_player
