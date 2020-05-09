from pypokerengine.api.game import setup_config, start_poker
from monte_carlo_bot import MonteCarloBot

config = setup_config(max_round=99, initial_stack=1000, small_blind_amount=10)
config.register_player(name="p1", algorithm=MonteCarloBot())
config.register_player(name="p2", algorithm=MonteCarloBot())
config.register_player(name="p3", algorithm=MonteCarloBot())
game_result = start_poker(config, verbose=1)
print(game_result)