import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()

        # Eingabe in das Modell
        self.current_player = spaces.Discrete(3) # welcher Spieler ist gerade dran
        self.current_phase = spaces.Discrete(6) # initial_research, research, action, production, drafting, end
        #self.initial_research_phase = spaces.MultiBinary(1) # ob wir in der research phase sind
        self.dealt_project_cards = spaces.MultiBinary(170) # welche karten schon ausgespielt wurden
        # initial research phase
        self.available_corporations = spaces.MultiBinary(12) # zwei davon sind immer 1
        self.available_initial_project_cards = spaces.MultiBinary(170) # 10 davon sind 1
        # action phase
        self.available_actions = spaces.MultiBinary(40) # muss ich nochmal richtig zählen
        self.select_action = spaces.Discrete(30) # z.b. select card to remove 1 animals - und nochmal richtig zählen
        self.cards_available_for_selection = spaces.MultiBinary(170) # nochmal zählen
        self.min_energy_to_spend = spaces.Box(low=0, high=1, shape=(1,))
        self.available_spaces = spaces.Discrete(35) # nochmal alle felder zählen
        self.which_production = spaces.Discrete(5) # nochmal zählen
        self.decrease_production_how_many_steps = spaces.Box(low=1, high=2, shape=(1,))
        self.tile_to_place_name = spaces.Discrete(5) # Commercial District, Restricted Area, Natural Preserve, Nuclear Zone, Mohole Area,



        # Ausgabe des Modells
        # research phase
        self.chosen_corporation = spaces.Discrete(12) # ein einziges wählen
        self.chosen_initial_project_cards = spaces.Box(0, 1, shape=(170,), dtype=np.float32) # select 10
        # action phase
        self.chose_action = spaces.Discrete(40) # eine der verfügbaren aktionen wählen
        self.selected_card = spaces.Box(0, 1, shape=(170,), dtype=np.float32) # select 1
        self.select_how_many = spaces.MultiBinary(1) # wenn 0 oder 1 gezogen werden müssen
        self.selected_space = spaces.Discrete(35) #richtig zählen
        self.selected_player = spaces.Discrete(3)


        # Diskreter Beobachtungsraum
        self.discrete_obs_space = spaces.Discrete(10)
        # Kontinuierlicher Beobachtungsraum
        self.continuous_obs_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        # Kombination von Beobachtungen
        self.observation_space = spaces.Dict({
            "discrete": self.discrete_obs_space,
            "continuous": self.continuous_obs_space
        })

        # Diskreter Aktionsraum
        self.discrete_action_space = spaces.Discrete(5)
        # Kontinuierlicher Aktionsraum
        self.continuous_action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
        # Kombinierter Aktionsraum
        self.action_space = spaces.Dict({
            "discrete": self.discrete_action_space,
            "continuous": self.continuous_action_space
        })

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        discrete_obs = self.discrete_obs_space.sample()
        continuous_obs = self.continuous_obs_space.sample()
        return {"discrete": discrete_obs, "continuous": continuous_obs}, {}

    def step(self, action):
        # Beispiel-Logik für Belohnung und Fertigkeitsstatus
        reward = np.random.random()
        done = reward > 0.95

        if action["discrete"] == 4:
            self.discrete_obs_space = np.int64(3)

        discrete_obs = self.discrete_obs_space.sample()
        continuous_obs = self.continuous_obs_space.sample()
        observation = {"discrete": discrete_obs, "continuous": continuous_obs}

        return observation, reward, done, False, {}
