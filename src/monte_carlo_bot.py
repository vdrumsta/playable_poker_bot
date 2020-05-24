from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card, gen_cards


# Estimate the ratio of winning games given the current state of the game
def estimate_win_rate(nb_simulation, nb_player, hole_card, community_card=None):
    if not community_card: community_card = []

    # Make lists of Card objects out of the list of cards
    community_card = gen_cards(community_card)
    hole_card = gen_cards(hole_card)

    # Estimate the win count by doing a Monte Carlo simulation
    win_count = sum([montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
    return 1.0 * win_count / nb_simulation


def montecarlo_simulation(nb_player, hole_card, community_card):
    # Do a Monte Carlo simulation given the current state of the game by evaluating the hands
    community_card = _fill_community_card(community_card, used_card=hole_card + community_card)
    unused_cards = _pick_unused_card((nb_player - 1) * 2, hole_card + community_card)
    opponents_hole = [unused_cards[2 * i:2 * i + 2] for i in range(nb_player - 1)]
    opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
    my_score = HandEvaluator.eval_hand(hole_card, community_card)
    return 1 if my_score >= max(opponents_score) else 0

def calculate_players_remaining(players):
    remaining_players = 0
    
    for player in players:
        if player['state'] == 'participating':
            remaining_players += 1

    return remaining_players

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)



class MonteCarloBot(BasePokerPlayer):
    def __init__(self):
        super().__init__()
        self.wins = 0
        self.losses = 0

    def ActPass(self, valid_actions):
        #print('Pass')
        for act in valid_actions:
            if (act["action"] == 'call'):
                if (act["amount"] == 0):
                    return act["action"], act["amount"]
                break
        return 'fold', 0
   
    def ActCall(self, valid_actions):
       # print('Call')
        for act in valid_actions:
            if (act["action"] == 'call'):
                    return act["action"], act["amount"]
        return 'fold', 0
   
    def ActRaise_x1(self, valid_actions):
        #print('RaiseMin')
        for act in valid_actions:
            if (act["action"] == 'raise'):
                return act["action"], act["amount"]["min"]
        return self.ActCall(valid_actions)

    def ActRaise_x2(self, valid_actions):
        #print('RaiseMin')
        for act in valid_actions:
            if (act["action"] == 'raise'):
                return self.ActRaise(valid_actions, act["amount"]["min"]*2)

        return self.ActCall(valid_actions)
 
    def ActRaise(self, valid_actions, amount):
        #print('Raise')
        for act in valid_actions:
            if (act["action"] == 'raise'):
                if (amount >= act["amount"]["min"]):
                    if (amount <= act["amount"]["max"]):
                        print('wasd1')
                        return act["action"], amount
                    else:
                        print('wasd2')
                        return act["action"], act["amount"]["max"]
                elif (act["amount"]["min"] == -1):
                    return self.ActCall(valid_actions)
                else:
                    print('wasd3')
                    return act["action"], act["amount"]["min"]

    vChanceCall  = {'preflop': 0.13, 'flop': 0.3, 'turn': 0.4, 'river':0.7}
    vChanceRaise_x1  = {'preflop': 0.17, 'flop': 0.45, 'turn': 0.47, 'river':0.8}
    vChanceRaise_x2  = {'preflop': 0.20, 'flop': 0.55, 'turn': 0.47, 'river':0.9}
    def declare_action(self, valid_actions, hole_card, round_state):
        # Estimate the win rate
        win_rate = estimate_win_rate(100, self.players_remaining, hole_card, round_state['community_card'])

        if (win_rate > self.vChanceRaise_x2[round_state['street']]):
            return self.ActRaise_x2(valid_actions)
        if (win_rate > self.vChanceRaise_x1[round_state['street']]):
            return self.ActRaise_x1(valid_actions)
        elif (win_rate > self.vChanceCall[round_state['street']]):
            return self.ActCall(valid_actions)
        else:
            return self.ActPass(valid_actions)

    def receive_game_start_message(self, game_info):
        self.num_players = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.players_remaining = calculate_players_remaining(seats)
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        is_winner = self.uuid in [item['uuid'] for item in winners]
        self.wins += int(is_winner)
        self.losses += int(not is_winner)


def setup_ai():
    return MonteCarloBot()