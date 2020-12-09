# pyright: strict
import random
from functools import cmp_to_key
from typing import Tuple, Optional, List

from .card import Shape, Card, Joker, NormalCard


Player = int


class Game:
    NUM_PLAYERS = 5

    def __init__(self) -> None:
        cards = []
        for shape in Shape:
            for number in range(2, 15):
                cards.append(NormalCard(shape, number))
        cards.append(Joker())
        random.shuffle(cards)
        self._hands = [[] for _ in range(self.NUM_PLAYERS)]   # type: List[List[Card]]
        for i in range(self.NUM_PLAYERS):
            self._hands[i] = cards[i * 10:(i + 1) * 10]
        self.extra = cards[-3:]

    def turn_player(self) -> Player:
        return self._turn_player

    def pledge_start(self, player: Player, min_count: int = 13) -> None:
        self.boss = None
        self._turn_player = player
        self.shape = None
        self.count = min_count - 2
        self.pledge_queue = [(player + i) % self.NUM_PLAYERS for i in range(self.NUM_PLAYERS)]

    def pledge_done(self) -> bool:
        return len(self.pledge_queue) == 1 or self.count == 20

    def current_pledge(self) -> Tuple[Optional[Player], Optional[Shape], Optional[int]]:
        return self.boss, self.shape, self.count

    def _check_pledge_valid(self, shape: Optional[Shape], count: int) -> bool:
        if count == 20:
            return True
        current_value = self.count + 1 if self.shape is None else self.count
        new_value = count + 1 if shape is None else count
        if new_value > current_value:
            return True
        return False

    def pledge_step(self, shape: Optional[Shape], count: Optional[int]) -> bool:
        if count is None:
            player = self.pledge_queue.pop(0)
            self._turn_player = self.pledge_queue[0]
            return True

        valid = self._check_pledge_valid(shape, count)
        if valid:
            player = self.pledge_queue.pop(0)
            self.boss = player
            self.shape = shape
            self.count = count
            self._turn_player = self.pledge_queue[0]
            self.pledge_queue.append(player)
        return valid

    def _compare_card(self, a: Card, b: Card) -> int:
        if isinstance(a, Joker):
            return -1
        if isinstance(b, Joker):
            return 1

        if a.shape == self.shape and b.shape != self.shape:
            return -1
        if a.shape != self.shape and b.shape == self.shape:
            return 1
        if a.shape.value < b.shape.value:
            return -1
        elif a.shape.value > b.shape.value:
            return 1
        return b.number - a.number

    def hand(self, player: Player) -> List[Card]:
        return sorted(self._hands[player], key=cmp_to_key(lambda x, y: self._compare_card(x, y)))

    def prepare_extra_hand(self) -> None:
        assert self.boss is not None
        self._hands[self.boss] += self.extra

    def discard_extra(self, discard: List[int]) -> None:
        assert self.boss is not None
        extra = self._hands[self.boss]  # type: List[Card]
        hand = [extra[i] for i in range(len(extra)) if i not in discard]
        self._hands[self.boss] = hand
        self._turn_player = self.boss

        self.round_shape = None
        self.round_first = True
        self.joker_called = False
        self.round_count = 1
        self.submitted = [None for _ in range(self.NUM_PLAYERS)]    # type: List[Optional[Card]]

    def round_state(self) -> str:
        summary = 'Shape: {}'.format(self.round_shape)
        if self.joker_called:
            summary += '\tJoker Called!'
        return summary

    def _check_card_valid(self, card: Card) -> bool:
        raise NotImplementedError()

    def submit(self, card: int) -> None:
        player = self.turn_player()
        assert player is not None
        hand = self.hand(player)    # type: List[Card]
        card_inst = hand[card]

        if self._check_card_valid(card_inst):
            self.submitted[player] = card_inst

    def submitted_cards(self) -> List[Card]:
        raise NotImplementedError()

    def round_summary(self) -> str:
        raise NotImplementedError()

    def final_summary(self) -> str:
        raise NotImplementedError()
