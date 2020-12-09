from mighty import Game


if __name__ == '__main__':
    game = Game()

    game.pledge_start(player=0, min_count=13)
    while not game.pledge_done():
        print('Boss: {}\tShape: {}\tCount: {}'.format(*game.current_pledge()))
        print('queue: {}'.format(game.pledge_queue))
        player = game.turn_player()
        print('Player {}: {}'.format(player, game.hand(player=player)))

        while True:
            try:
                shape, count = input().split()
                count = int(count)
                if count == 0:
                    shape = None
                    count = None
                elif shape == 'no':
                    shape = None
                elif shape not in list(map(lambda x: x.value, Shape)):
                    continue

                valid = game.pledge_step(shape=shape, count=count)
                if valid:
                    break
            except Exception:
                continue

    game.prepare_extra_hand()
    hand = game.hand(player=boss)
    print('Boss extra hand: {}'.format(hand))
    discard = list(map(int, input('Discard: ').split()))
    game.discard_extra(discard=discard)

    for r in range(10):
        print('Round {}'.format(r))
        for _ in range(Game.NUM_PLAYERS):
            print(game.round_state())
            player = game.turn_player()
            hand = game.hand(player=player)
            print(hand)
            while True:
                card = int(input('Card: '))
                valid = game.submit(card=card)
                if valid:
                    break
            print(game.submitted_cards())
        print(game.round_summary())
    print(game.final_summary())