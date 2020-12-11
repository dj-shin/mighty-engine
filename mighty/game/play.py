# pyright: strict
import logging
from typing import Tuple, Optional, List

from .common import Player, PhaseBase
from ..card import Shape, Card, Joker
from ..action import Action, JokerCall, JokerShape


class PlayPhase(PhaseBase):
    def __init__(self, boss: Player, kiru: Optional[Shape], count: int,
                 hands: List[List[Card]], discarded: List[Card]) -> None:
        super().__init__(kiru, hands, boss)
        self.boss = boss
        self.count = count
        self.discarded = discarded

        self.round_count = 1
        self._init_round()
        self._round_results = []    # type: List[Tuple[Player, List[Card]]]

    def _init_round(self):
        self.round_shape = None     # type: Optional[Shape]
        self.round_first = True
        self.joker_called = False
        self.submitted = [None for _ in range(self.NUM_PLAYERS)]    # type: List[Optional[Card]]

    def round_state(self) -> str:
        summary = 'Shape: {}'.format(self.round_shape)
        if self.joker_called:
            summary += '\tJoker Called!'
        return summary

    def _check_card_valid(self, card: Card) -> bool:
        logging.debug("Checking: {}".format(card))
        if isinstance(card, Joker):
            logging.debug("\tJoker => True")
            return True
        if card.is_mighty(self.kiru):
            logging.debug("\tMighty => True")
            return True

        if self.round_count == 1 and self.round_first and card.shape == self.kiru:
            logging.debug("\tRound count == 1 & Round first & Kiru => False")
            return False

        hand = self._hands[self.turn_player()]   # type: List[Card]
        if self.round_shape is not None and \
           [c for c in hand if c.shape == self.round_shape] and card.shape != self.round_shape:
            logging.debug("\tRound shape: {} & Card shape: {}".format(self.round_shape, card.shape))
            return False

        if self.joker_called and [c for c in hand if isinstance(c, Joker)]:
            logging.debug("\tJoker called & !Joker => False")
            return False

        return True

    def check_submit(self, card: int) -> Tuple[bool, List[Action]]:
        player = self.turn_player()
        hand = self.hand(player)    # type: List[Card]
        card_inst = hand[card]

        if self._check_card_valid(card_inst):
            return True, self._possible_actions(card_inst)
        return False, []

    def submit(self, card: int, action: Optional[Action], check: bool = False) -> None:
        player = self.turn_player()
        hand = self.hand(player)    # type: List[Card]

        if check:
            assert self._check_card_valid(hand[card])
            assert action in self._possible_actions(hand[card])

        card_inst = hand.pop(card)
        self.submitted[player] = card_inst
        self._hands[player] = hand

        if isinstance(action, JokerShape):
            if self.round_first:
                self.round_first = False
                self.round_shape = action.shape
        else:
            if isinstance(action, JokerCall):
                self.joker_called = action.effect
            if self.round_first:
                self.round_first = False
                self.round_shape = card_inst.shape

        if not (None in self.submitted):
            winner = self._eval_winner()
            self._round_results.append((winner, [x for x in self.submitted if x is not None]))
            self._init_round()
            self.round_count += 1
            self._turn_player = winner
        else:
            self._turn_player = (player + 1) % self.NUM_PLAYERS

    def _card_value(self, card: Card) -> int:
        if isinstance(card, Joker):
            if self.joker_called or self.round_count == 1 or self.round_count == 10:
                return 0
            else:
                return 100
        if card.is_mighty(self.kiru):
            return 1000
        if card.shape == self.kiru:
            return 70 + card.number
        if card.shape == self.round_shape:
            return 30 + card.number
        return card.number

    def _eval_winner(self) -> Player:
        cards = [x for x in self.submitted if x is not None]
        order = sorted(range(len(cards)), key=lambda k: self._card_value(cards[k]))
        winner = order[-1]
        top = cards[winner]
        logging.debug('Player {} wins with Top card {}'.format(winner, top))
        return winner

    def _possible_actions(self, card: Card) -> List[Action]:
        if isinstance(card, Joker):
            if self.round_first:
                return [JokerShape(shape) for shape in Shape]
            else:
                return []
        if card.is_joker_call(self.kiru) and self.round_first:
            return [JokerCall(True), JokerCall(False)]
        return []

    def submitted_cards(self) -> List[Card]:
        return [x for x in self.submitted if x is not None]

    def round_summary(self) -> str:
        if self._round_results:
            return str(self._round_results[-1])
        else:
            return 'No round results'

    def final_summary(self) -> str:
        scores = [0 for _ in range(self.NUM_PLAYERS)]     # type: List[int]
        for r in self._round_results:
            winner, cards = r
            score = sum(map(lambda c: c.score(), cards))
            scores[winner] += score
        assert sum(scores) + sum(map(lambda c: c.score(), self.discarded)) == 20
        return str(scores)
