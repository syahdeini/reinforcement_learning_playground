from ale_python_interface import ALEInterface
from enduro.action import Action
from enduro.control import Controller
from enduro.state import StateExtractor
import random

class Agent(object):
    def __init__(self):
        self._ale = ALEInterface()
        self._ale.setInt('random_seed', 123)
        self._ale.setFloat('repeat_action_probability', 0.0)
        self._ale.setBool('color_averaging', False)
        self._ale.loadROM('roms/enduro.bin')
        self._controller = Controller(self._ale)
        self._extractor = StateExtractor(self._ale)
        self._image = None
        self.curr_action = 0

    def run(self, learn, episodes=1, draw=False):
        """ Implements the playing/learning loop.

        Args:
            learn(bool): Whether the self.learn() function should be called.
            episodes (int): The number of episodes to run the agent for.
            draw (bool): Whether to overlay the environment state on the frame.

        Returns:
            None
        """
        if learn:
            self.init_Q()
        action = random.choice(self.getActionsSet()) # init_action for q_learning
        for e in range(episodes):
            # Observe the environment to set the initial state
            (grid, self._image) = self._extractor.run(draw=draw, scale=4.0)
            self.initialise(grid)

            num_frames = self._ale.getFrameNumber()
            # Each episode lasts 6500 frames
            while self._ale.getFrameNumber() - num_frames < 6500:
                # Take an action
                self.act(action)

                # Update the environment grid
                s_grid = grid
                (grid, self._image) = self._extractor.run(draw=draw, scale=4.0)
                self.sense(grid)
                s_next_grid = grid
                # Perform learning if required
                if learn:
                    # self.learn(s_grid,s_next_grid) # for q learning
                    action = self.learn(s_grid,s_next_grid,action) 

                self.callback(learn, e + 1, self._ale.getFrameNumber() - num_frames)
            self.end_state(e)
            self._ale.reset_game()

    def getActionsSet(self):
        """ Returns the set of all possible actions
        """
        return [Action.ACCELERATE, Action.RIGHT, Action.LEFT, Action.BREAK]

    def move(self, action):
        """ Executes the action and advances the game to the next state.

        Args:
            action (int): The action which should executed. Make sure to use
                          the constants returned by self.getActionsSet()

        Returns:
           int: The obtained reward after executing the action
        """
        return self._controller.move(action)

    def initialise(self, grid):
        """ Called at the beginning of each episode, mainly used
        for state initialisation.

        Args:
            grid (np.ndarray): 11x10 array with the initial environment grid.

        Returns:
            None
        """
        raise NotImplementedError

    def act(self):
        """ Called at each loop iteration to choose and execute an action.

        Returns:
            None
        """
        raise NotImplementedError

    def sense(self, grid):
        """ Called at each loop iteration to construct the new state from
        the update environment grid.

        Returns:
            None
        """
        raise NotImplementedError

    def learn(self):
        """ Called at each loop iteration when the agent is learning. It should
        implement the learning procedure.

        Returns:
            None
        """
        raise NotImplementedError

    def callback(self, learn, episode, iteration):
        """ Called at each loop iteration mainly for reporting purposes.

        Args:
            learn (bool): Indicates whether the agent is learning or not.
            episode (int): The number of the current episode.
            iteration (int): The number of the current iteration.

        Returns:
            None
        """
    def get_surround():


        raise NotImplementedError
