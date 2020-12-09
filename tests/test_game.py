from mighty import Game


class TestGame:
    def test_init(self):
        game = Game()

        game.pledge_start(player=0, min_count=13)
        for i in range(Game.NUM_PLAYERS):
            assert len(game.hand(i)) == 10
