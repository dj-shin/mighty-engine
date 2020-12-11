# pyright: strict
import logging
from typing import Optional, List

from .common import Player, PhaseBase
from ..card import Shape, Card


class ExtraPhase(PhaseBase):
    def __init__(self, boss: Player, kiru: Optional[Shape], count: int,
                 hands: List[List[Card]], extra: List[Card]) -> None:
        super().__init__(kiru, hands, boss)
        self.boss = boss
        self.count = count
        self.extra = extra

    def prepare_extra_hand(self) -> None:
        assert self.boss is not None
        self._hands[self.boss] += self.extra

    def discard_extra(self, discard: List[int]) -> None:
        assert self.boss is not None
        extra = self.hand(self.boss)    # type: List[Card]
        self.discarded = [extra[i] for i in discard]
        logging.debug('Discarding {}'.format(self.discarded))
        hand = [extra[i] for i in range(len(extra)) if i not in discard]
        self._hands[self.boss] = hand

    def extra_result(self):
        return self.boss, self.kiru, self.count, self._hands, self.discarded

    def pick_friend(self, condition: str) -> None:
        pass
