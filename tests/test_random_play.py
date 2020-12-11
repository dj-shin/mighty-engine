import random

from mighty.game import PledgePhase, ExtraPhase, PlayPhase
from mighty.card import Shape


class TestRandomPlay:
    def pledge_until_valid(self, game: PledgePhase):
        while True:
            try:
                shape = random.choice(['heart', 'diamond', 'clover', 'spade', 'no'])
                count = random.randint(12, 20) if random.randrange(10) else 0
                if count == 0:
                    shape = None
                    count = None
                elif shape == 'no':
                    shape = None
                elif shape not in list(map(lambda x: x.value, Shape)):
                    continue
                else:
                    shape = Shape(shape)

                valid = game.pledge_step(kiru=shape, count=count)
                if valid:
                    break
            except Exception:
                continue

    def test_random_play(self):
        random.seed(0)
        game = PledgePhase(start_player=random.randrange(PledgePhase.NUM_PLAYERS), min_count=random.randrange(20))
        while not game.pledge_done():
            self.pledge_until_valid(game)

        if game.boss is None:
            return

        game = ExtraPhase(*game.pledge_result())
        game.prepare_extra_hand()
        discard = random.sample(list(range(13)), k=3)
        game.discard_extra(discard=discard)
        friend_condition = 'mighty'
        game.pick_friend(friend_condition)

        game = PlayPhase(*game.extra_result())
        for r in range(10):
            for _ in range(game.NUM_PLAYERS):
                while True:
                    card = random.randrange(10 - r)
                    valid, actions = game.check_submit(card=card)
                    if not valid:
                        continue
                    elif actions:
                        action = random.choice(actions)
                        game.submit(card=card, action=action)
                    else:
                        game.submit(card=card, action=None)
                    break
