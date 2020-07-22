import gym 
from gym import spaces
import numpy as np


"""  
This is a simple environment for doing simple experiments 
The agent recieves number in order, and the goal is arrange 
them in an array in order.

The observations are the number given at this moment and the array
up to this moment

An action is the index where the current number is to be placed in

"""

class ArrangeEnv(gym.Env):
    metadata = {'render,mode': ['human']}
    
    def __init__(self, size):
        
        self.array = np.zeros(size)
        self.number = 1
        self.time = 0
        self.observation_space = spaces.Box(low = 0, high = size, shape = (size+1, ), dtype = int)
        self.action_space = spaces.Discrete(size)
        
    
    
    def step(self,action):
        stepped  = self.Transition(action)
        
        reward = self.Reward(action, stepped)
        
        done = self.done() 
        
        obs = self.makeObs()
        
        return obs, reward, done,{}
    
    def reset(self):
        self.array = np.zeros(size)
        self.number = 1
        self.time = 1
        
        obs = self.makeObs()
        return obs
    
    def render(self):
        print(self.array)
        print("Number is", self.number)
        print('time:', self.time)
        
        
    
    
    def Transition(self,action):
        self.time += 1
        
        if(self.array[action] != 0):
            return False
        else:
            self.array[action] = self.number
            self.number += 1
            return True
    
    
    def Reward(self,action,stepped):
        
        return self.SlotReward(action,stepped) + self.timeReward()
    
    
    
    def SlotReward(self, action, stepped):
        if(not stepped):
            return -1
        elif(action == self.number -2):
            return 1
        return 1.0 / np.abs(action - self.number +2)
        
    def timeReward(self):
        #if(self.time == time_limit-1):
            #return -size
        return -1.0/time_limit
        
    def done(self):
        return self.number == size+1 or self.time == time_limit
    
    def makeObs(self):
        return np.concatenate([np.array([self.number]), self.array])