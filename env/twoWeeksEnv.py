import gym
from gym import spaces 
import numpy as np

class TwoSchechEnv(gym.Env):
    
    metadata = {'render.mode': ['human']}
    
    def __init__(self,  DAYS,SLOTS1,SLOTS2, NEXT_DAY_P ):
        
        '''
        
        '''
        #Variables used for the state 
        
        #Scheduale for D1
        self.sched1 = np.zeros(DAYS)
        
        #Schedule for D2
        self.sched2 = np.zeros(DAYS)
        
        
        
        #Number of collection days of current patient
        #This is the distrebution we were given for collection days
        self.patient_collection_days = np.random.choice([1,2,3,4,5], p = [.4,.3,.15.1,.05])
        
        #The Current Day 
        self.current_day = 0 
        
        #Observation Space
        #One array of length = 1 + 1 + DAY1 + DAYS2
        #index (0) is current day
        #index(1) is patient collection number
        #indeces (2 - DAY1 + 1) is sched1
        #The rest os sched2
        self.observation_space spaces.Box(low =0 , high = SLOT1, shape = (2+DAYS+DAYS,), dtype = int)
        
        #Action Space
        self.action_space = spaces.MultiDiscrete(DAYS,DAYS)
        
        
        
        #Internal variables we use to build the schedule 
        
        #Patient number 
        self.patient_number = 1 
        
        #Matrix for sched1 and sched2 
        self.MatrixSched1 = np.zeros((DAYS1,SLOT1))
        self.MatrixSched2 = np.zeros((DAYS2,SLOTS2 * 9 ))
        self.Q1 = np.array([])

        self.end_day = 0
        
        #remianing Slots
        self.remainingSlots1 = DAYS * SLOT1
        
        self.remainingSlots2 = DAYS * SLOT2 * 9
        
        
        #Counting variabels
        self.overlap_count = 0
        self.total_reward = 0
        self.two_weeks_violations = 0
        
    
    
    def step(self,action):
        #Tranistion returns True or False, depending on whither scheduling happened
        schedled = self.Transition(action)
        
        reward = self.Reward(action,schedled)
        
        self.total_reward += reward
        
        obs = self.makeObs()
        
        done = self.done
        
        return obs, reward, done, {}
    
    def reset(self, action):
        
        
        self.sched1 = np.zeros(DAYS)
        self.sched2 = np.zeros(DAYS)  
        self.patient_collection_days = np.random.randint(1,COLLECTIONS)
        self.current_day = 0 
        self.patient_number = 1 
        self.MatrixSched1 = np.zeros((DAYS1,SLOT1))
        self.MatrixSched2 = np.zeros((DAYS2,SLOTS2 * 9 ))
        self.Q1 = np.array([])
        self.end_day = 0
        self.remainingSlots1 = DAYS * SLOT1
        self.remainingSlots2 = DAYS * SLOT2 * 9
        self.overlap_count = 0
        self.total_reward = 0
        self.two_weeks_violations = 0
        
        obs = makeObs()
        
        return obs
    

    def render(self):
        pass
    
    #************************ Foramting Logic ******************************"""

    
    #Makes an Observation in the observation space format
    def makeObs(self):
        return np.concatenate([np.array([self.current_day]), np.array([self.patient_collection_days]), self.sched1,
                              self.sched2])
    
    #  Tells us when to to stap, return True or False
    def done(self):
        pass
    
    #********************************Transition Logic**************************************"""

    
    def Transition(self,action):
        #Returns boolean depending on whither scheduling happend or not
        scheduled = self.updateSched(action)
        
        self.updateInternalStates(action,scheduled)
        self.updateObservations(action, scheduled)
        
    def updateSched(self,action):
        pass
    
    def updateInternalStates(self,action,scheduled):
        pass
    
    def updateObservations(self,action,schedled):
        pass
    
#**********************************Reward Logic ***************************************"""

    def Reward(self,action,scheduled):
    
        return self.SlotReward(action,scheduled) + self.QReward(action,scheduled)
    
    def SlotReward(self,action,scheduled):
        pass
    
    def QReward(self,action,scheduled):
        pass
    
    