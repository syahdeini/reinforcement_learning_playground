import cv2
from enduro.agent import Agent
from enduro.action import Action
from enduro.state import EnvironmentState
import numpy as np
import random
import pdb

class QAgent(Agent):
    def __init__(self):
        super(QAgent, self).__init__()
        # Add member variables to your class here
        # if not self.total_reward:
        # self.total_reward = 0
        self.policy_s_a = {}
        self.state_dict = {}
        self.epsilon = 0.4
        self.alpha = 0.5
        self.gamma = 0.9
        self.current_reward = 0
        self.set_total_reward = []

    def state_Q(self,l,q_state,i):
        if i==len(q_state):
            l.append(list(q_state))
            return
        q_state[i]='0'
        self.state_Q(l,q_state,i+1)
        q_state[i]='1' 
        self.state_Q(l,q_state,i+1)

    def init_Q(self):
        _l = [0 for i in range(5)]
        q_grid = []
        self.state_Q(q_grid,_l,0)
        for grid in q_grid:
            for act in self.getActionsSet():
                key = ''.join(grid)+ '_' + Action.toString(act)
                self.state_dict[key] = 1.0/len(q_grid)
                if act == Action.ACCELERATE:
                    self.policy_s_a[key] = 1.0/len(self.getActionsSet()) + 0.45 #encourage to accelearte
                else:
                    self.policy_s_a[key] = 1.0/len(self.getActionsSet())

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
        self.current_reward = self.move(action) 
        self.total_reward += self.current_reward
        self.set_total_reward.append(self.total_reward)

    def sense(self, grid):
        """ Constructs the next state from sensory signals.

        gird -- 2-dimensional numpy array containing the latest grid
                representation of the environment
        """
        # Visualise the environment grid
        cv2.imshow("Environment Grid", EnvironmentState.draw(grid))

    # def update_policy(max_key):
    #     state,max_act = max_key.split('_')
    #     for act in self.getActionsSet():

    def get_max_action(self,state,val_dict):
        possible_move = []
        max_pol_s_a = -1000
        max_a = None
        for act in self.getActionsSet():
            key_s_a = state+'_'+Action.toString(act)
            pol_s_a = val_dict[key_s_a]
            if pol_s_a > max_pol_s_a:
                max_pol_s_a = pol_s_a
                max_a = act
        return max_a

    def get_act_from_policy(self,max_act):
        # 1 - ( self.epsilon + float(self.epsilon) / len(self.getActionsSet()))
        # float(self.epsilon) / len(self.getActionsSet()
        rand = random.random()
        if rand >= self.epsilon:
            return random.choice(self.getActionsSet())
        else: # rand  
            return max_act

    def get_surrround_agent(self,grid):
        pos_i = list(grid[0]).index(2)
        # if it's on the left or ride side
        # LEFT
        temp_grid =['1' for i in range(5)]
        if pos_i-1 > 0:
            temp_grid[0]=str(grid[0][pos_i-1])
            temp_grid[1]=str(grid[1][pos_i-1])
        # RIGHT
        temp_grid[2]=str(grid[1][pos_i])
        if pos_i < len(grid[0]):
            temp_grid[3]=str(grid[0][pos_i+1])
            temp_grid[4]=str(grid[1][pos_i+1])
        # update the poliocy
        return ''.join(temp_grid)

    def learn(self,grid,next_grid,act):
        """ Performs the learning procudre. It is called after act() and
        sense() so you have access to the latest tuple (s, s', a, r).
        """
        print("learning")
        # there is no need for next grid
        state = self.get_surrround_agent(grid)
        key_q_s_a = state + "_" + Action.toString(act)
        q_s_a = self.state_dict[key_q_s_a]

        next_state = self.get_surrround_agent(next_grid)
        # find max action Q(s',a) based on policy (next state)
        max_act = self.get_max_action(next_state,self.state_dict) # get the maximum action
        key_qnext_s_a = next_state + '_' + Action.toString(max_act)
        qnext_s_a = self.state_dict[key_qnext_s_a]        
        q_s_a  = q_s_a + self.alpha * (self.current_reward+ (self.gamma * qnext_s_a)  - q_s_a) 
        self.state_dict[key_q_s_a] = q_s_a

        next_max_act = self.get_max_action(state,self.policy_s_a) # get the maximum action        
        return next_max_act


    def callback(self, learn, episode, iteration):
        """ Called at the end of each timestep for reporting/debugging purposes.
        """
        print "{0}/{1}: {2}".format(episode, iteration, self.total_reward)
        # Show the game frame only if not learning
        self.epsilon = float(1)/(iteration * (episode + 1))
        # if not learn:
        # cv2.imshow("Enduro", self._image)
            # cv2.waitKey(40)

    def write_to_file(self, episode, _l, filename):
        f = open(filename,"a")
        val = (episode, np.mean(_l), np.var(_l), self.total_reward)
        f.write("%d-%.4f-%.4f-%.4f\n"% val)

    def end_state(self,episode):
        self.write_to_file(episode, self.set_total_reward, "reward_file")
    
 

if __name__ == "__main__":
    a = QAgent()
    a.run(True, episodes=100, draw=True)
    print 'Total reward: ' + str(a.total_reward)
