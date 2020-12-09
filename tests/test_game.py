import unittest
from mighty import Game


class TestGame(unittest.TestCase):
    def test_init(self):
        game = Game()

        game.pledge_start(player=0, min_count=13)
        for i in range(Game.NUM_PLAYERS):
            self.assertEqual(len(game.hand(i)), 10)
