import random
import logging
import traceback

from mighty.game import PledgePhase, ExtraPhase, PlayPhase
from mighty.card import Shape


def pledge_until_valid(game: PledgePhase):
    while True:
        try:
            # shape, count = input().split()
            # count = int(count)
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
            logging.debug(traceback.print_exc())
            continue


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    for _ in range(1000):
        game = PledgePhase(start_player=random.randrange(PledgePhase.NUM_PLAYERS), min_count=random.randrange(20))
        while not game.pledge_done():
            logging.debug('Boss: {}\tShape: {}\tCount: {}'.format(*game.current_pledge()))
            logging.debug('queue: {}'.format(game.pledge_queue))
            player = game.turn_player()
            logging.debug('Player {}: {}'.format(player, game.hand(player=player)))

            pledge_until_valid(game)

        if game.boss is None:
            continue

        game = ExtraPhase(*game.pledge_result())
        game.prepare_extra_hand()
        boss = game.boss
        hand = game.hand(player=boss)
        logging.debug('Boss extra hand: {}'.format(hand))
        # discard = list(map(int, input('Discard: ').split()))
        discard = random.sample(list(range(13)), k=3)
        game.discard_extra(discard=discard)
        # friend_condition = input('Pick friend: ')
        friend_condition = 'mighty'
        game.pick_friend(friend_condition)

        game = PlayPhase(*game.extra_result())
        for r in range(10):
            logging.debug('Round {}'.format(r))
            for _ in range(game.NUM_PLAYERS):
                logging.debug(game.round_state())
                player = game.turn_player()
                hand = game.hand(player=player)
                logging.debug(hand)
                while True:
                    # card = int(input('Card: '))
                    card = random.randrange(10 - r)
                    valid, actions = game.check_submit(card=card)
                    if not valid:
                        continue
                    elif actions:
                        logging.debug(actions)
                        # action = actions[int(input())]
                        action = random.choice(actions)
                        game.submit(card=card, action=action)
                    else:
                        game.submit(card=card, action=None)
                    break
                logging.debug(game.submitted_cards())
            logging.debug(game.round_summary())
        logging.debug(game.final_summary())
