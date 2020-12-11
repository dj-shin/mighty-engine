from mighty.game import PledgePhase
from mighty.card import Shape, NormalCard, Joker


class TestPledge:
    def test_init_random(self):
        game = PledgePhase(start_player=0, min_count=13)
        for i in range(game.NUM_PLAYERS):
            assert len(game.hand(i)) == 53 // game.NUM_PLAYERS

    def test_init_cards(self):
        cards = []
        cards.append(Joker())
        for shape in Shape:
            for number in range(2, 15):
                cards.append(NormalCard(shape, number))

        hands = []
        hand_size = len(cards) // PledgePhase.NUM_PLAYERS
        for i in range(PledgePhase.NUM_PLAYERS):
            hands.append(cards[i * hand_size:(i + 1) * hand_size])
        hands.append(cards[hand_size * PledgePhase.NUM_PLAYERS:])
        game = PledgePhase(start_player=0, min_count=13, hands=hands)
        for i in range(game.NUM_PLAYERS):
            assert len(game.hand(i)) == len(hands[i])
            assert set(game.hand(i)) == set(hands[i])
