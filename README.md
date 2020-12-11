# Mighty Engine

## Example

```python
game = PledgePhase(start_player=0, min_count=13)
while not game.pledge_done():
    print('Boss: {}\tShape: {}\tCount: {}'.format(*game.current_pledge()))
    print('queue: {}'.format(game.pledge_queue))
    player = game.turn_player()
    print('Player {}: {}'.format(player, game.hand(player=player)))

    pledge_until_valid(game)

if game.boss is not None:
    game = ExtraPhase(*game.pledge_result())
    game.prepare_extra_hand()
    boss = game.boss
    hand = game.hand(player=boss)
    print('Boss extra hand: {}'.format(hand))
    discard = list(map(int, input('Discard: ').split()))
    game.discard_extra(discard=discard)
    friend_condition = input('Pick friend: ')
    game.pick_friend(friend_condition)

    game = PlayPhase(*game.extra_result())
    for r in range(10):
        print('Round {}'.format(r))
        for _ in range(game.NUM_PLAYERS):
            print(game.round_state())
            player = game.turn_player()
            hand = game.hand(player=player)
            print(hand)
            while True:
                card = int(input('Card: '))
                valid, actions = game.check_submit(card=card)
                if not valid:
                    continue
                elif actions:
                    print(actions)
                    action = actions[int(input())]
                    game.submit(card=card, action=action)
                else:
                    game.submit(card=card, action=None)
                break
            print(game.submitted_cards())
        print(game.round_summary())
    print(game.final_summary())
```
