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




#Normalizing the states functions
def norm_array(array,size):
    return array/size
def norm_number(number,size):
    return number / size
def norm_time(time,limit):
    return time / limit

def norm_obs(time,number,array, size,limit):
    return np.concatenate([
                          np.array([norm_number(number,size)]),
                          norm_array(array,size)])

def norm_x(n_obs, action,size):
    return np.concatenate([np.array([action / size]),n_obs])


#q linear functions
def q_linear(x, w):
    return np.sum(x * w)


#Saarsa algorithm 
def Sarsa(env, w, alpha=0.01, epsilon=.5,gamma=.99):
    obs = env.reset()
    done = False
    new_w = w
    
    
    #Normalize the initial state 
    current_n_obs = norm_obs(env.time,env.number, env.array,size,time_limit)
    #Choose an Initial Action (Again eps-greedy algorithm )
    coin = np.random.binomial(1,epsilon)
    if(coin == 1):
            next_action = env.action_space.sample()
    else:
        next_action = 0
        for action in range(size):
            if q_linear(norm_x(current_n_obs,action,size),new_w) > q_linear(norm_x(current_n_obs,next_action,size),new_w):
                next_action = action
                
                
    while not done:  #Lopp for each step in the episode
        
        current_action = next_action
        prev_n_obs = current_n_obs
        
        #Take the Action Chosen the previous step, observe next state and reward 
        obs, reward, done,_ = env.step(current_action)
        current_n_obs = norm_obs(env.time,env.number, env.array,size,time_limit)
        
        
        
        
        #if we are done, last reward and break 
        
        if done:
            x_prev = norm_x(prev_n_obs,current_action,size)
            new_w = new_w + alpha*(reward - q_linear(x_prev,new_w))*x_prev
            break
        
        
        #otherwise, choose a new action A', according to Greedy and q_linear
        coin = np.random.binomial(1,epsilon)
        if(coin == 1):
            next_action = env.action_space.sample()
        else:
            next_action = 0
            for action in range(size):
                if q_linear(norm_x(current_n_obs,action,size),new_w) > q_linear(norm_x(current_n_obs,next_action,size),new_w):
                    next_action = action
        
        #update the weights
        x_prev = norm_x(prev_n_obs,current_action,size)
        x_current = norm_x(current_n_obs,next_action,size)
        new_w = new_w + alpha*(reward + gamma * q_linear(x_current,new_w) - q_linear(x_prev,new_w))*x_prev
        
    
    return new_w
            

#Extract best action from q function

def best_action(env, w):
    n_obs = norm_obs(env.time,env.number, env.array,size,time_limit)
    next_action = 0
    for action in range(size):
        if q_linear(norm_x(n_obs,action,size),w) > q_linear(norm_x(n_obs,next_action,size),w):
            next_action = action
    return next_action


#Example how to use 
'''
1)Initialize the w with zeros 
w = np.zeros(size+1+1)

2)Loop to train the w 
for _ in range(100):
    w = Sarsa(env,w)

3)use best_action to find best action at each step


'''