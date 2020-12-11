# pyright: strict
import random
from typing import Tuple, Optional, List

from .common import Player, PhaseBase
from ..card import Shape, Card, Joker, NormalCard


class PledgePhase(PhaseBase):
    def __init__(self, min_count: int = 13, start_player: Player = 0, hands: Optional[List[List[Card]]] = None) -> None:
        cards = []
        if hands is None:
            for shape in Shape:
                for number in range(2, 15):
                    cards.append(NormalCard(shape, number))
            cards.append(Joker())
            random.shuffle(cards)
            self._hands = [[] for _ in range(self.NUM_PLAYERS)]   # type: List[List[Card]]
            for i in range(self.NUM_PLAYERS):
                self._hands[i] = cards[i * 10:(i + 1) * 10]
            self.extra = cards[-3:]
        else:
            assert len(hands) == self.NUM_PLAYERS + 1
            self._hands = [hands[i] for i in range(self.NUM_PLAYERS)]   # type: List[List[Card]]
            self.extra = hands[-1]

        super().__init__(None, self._hands, start_player)

        self.boss = None
        self.count = min_count - 2
        self.pledge_queue = [(start_player + i) % self.NUM_PLAYERS for i in range(self.NUM_PLAYERS)]

    def pledge_done(self) -> bool:
        return (self.boss is not None and len(self.pledge_queue) == 1) or \
               (self.boss is None and len(self.pledge_queue) == 0) or \
               self.count == 20

    def current_pledge(self) -> Tuple[Optional[Player], Optional[Shape], Optional[int]]:
        return self.boss, self.kiru, self.count

    def _check_pledge_valid(self, kiru: Optional[Shape], count: int) -> bool:
        if count == 20:
            return True
        current_value = self.count + 1 if self.kiru is None else self.count
        new_value = count + 1 if kiru is None else count
        if new_value > current_value:
            return True
        return False

    def pledge_step(self, kiru: Optional[Shape], count: Optional[int]) -> bool:
        if count is None:
            player = self.pledge_queue.pop(0)
            self._turn_player = self.pledge_queue[0]
            return True

        valid = self._check_pledge_valid(kiru, count)
        if valid:
            player = self.pledge_queue.pop(0)
            self.boss = player
            self.kiru = kiru
            self.count = count
            self._turn_player = self.pledge_queue[0] if self.pledge_queue else player
            self.pledge_queue.append(player)
        return valid

    def pledge_result(self) -> Tuple[Player, Optional[Shape], int, List[List[Card]], List[Card]]:
        assert self.boss is not None
        return self.boss, self.kiru, self.count, self._hands, self.extra
