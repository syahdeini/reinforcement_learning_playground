import cv2
from enduro.agent import Agent
from enduro.action import Action
from enduro.state import EnvironmentState
import numpy as np 
import random

class RandomAgent(Agent):
    def __init__(self):
        super(RandomAgent, self).__init__()
        # Add member variables to your class here
        self.total_reward = 0
        self.set_total_reward = []

    def initialise(self, grid):
        """ Called at the beginning of an episode. Use it to construct
        the initial state.
        """
        # Reset the total reward for the episode
        self.total_reward = 0
        cv2.imshow("Enduro", self._image)
        cv2.imshow("Environment Grid", EnvironmentState.draw(grid))


    def act(self,action):
        """ Implements the decision making process for selecting
        an action. Remember to store the obtained reward.
        """

        # You can get the set of possible actions and print it with:
        # print [Action.toString(a) for a in self.getActionsSet()]

        # Execute the action and get the received reward signal
        # IMPORTANT NOTE:
        # 'action' must be one of the values in the actions set,
        # i.e. Action.LEFT, Action.RIGHT, Action.ACCELERATE or Action.BREAK
        # Do not use plain integers between 0 - 3 as it will not work
        # action = np.random.randint(0,3)
        action = random.choice(self.getActionsSet())
        self.total_reward += self.move(action)
        self.set_total_reward.append(self.total_reward)


    def sense(self, grid):
        """ Constructs the next state from sensory signals.

        gird -- 2-dimensional numpy array containing the latest grid
                representation of the environment
        """
        # Visualise the environment grid
        cv2.imshow("Environment Grid", EnvironmentState.draw(grid))

    def learn(self,grid,ngrid,act):
        """ Performs the learning procudre. It is called after act() and
        sense() so you have access to the latest tuple (s, s', a, r).
        """
        pass

    def callback(self, learn, episode, iteration):
        """ Called at the end of each timestep for reporting/debugging purposes.
        """
        print "{0}/{1}: {2}".format(episode, iteration, self.total_reward)
        # Show the game frame only if not learning
        # if not learn:
        #     cv2.imshow("Enduro", self._image)
        #     cv2.waitKey(40)

    def write_to_file(self, episode, _l, filename):
        f = open(filename,"a")
        val = (episode, np.mean(_l), np.var(_l), self.total_reward)
        f.write("%d-%.4f-%.4f-%.4f\n"% val)

    def end_state(self,episode):
        self.write_to_file(episode, self.set_total_reward, "random_reward_file")
    
  
if __name__ == "__main__":
    a = RandomAgent()
    a.run(False, episodes=100, draw=True)
    print 'Total reward: ' + str(a.total_reward)
