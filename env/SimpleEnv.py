import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class SimpleSchedEnv(gym.Env):
    
    
#************************************Basic Methods Definition ************************  
    
    metadata = {'render.mode': ['human']}
    
  
    def __init__(self, DAYS,SLOTS, COLLECTIONS, NEXT_DAY_P, SIZE):
        
        """ 
        
        """
        
        #the State Variables
        
        #Deterministic
        self.schedule = np.zeros((DAYS,SLOTS), dtype = int)
        self.current_day = 0
        self.current_patient_number = 1
        self.remaining_slots = DAYS*SLOTS
        
        #Stochastic
        self.patient = np.random.randint(1,COLLECTIONS+1)
        self.end_day = 0 
        """
        Becasuase we are interfacing with stable_baseline, we need to represent
        both spaces of observation and of actions as a flat array
            1)Observation Spcae:
                it is an array of size SIZE = 1 + 1 + 1 + 1 + 1 + DAYS*SLOTS
                we index as follows:
                    0) current_day
                    1)current_patient_number
                    2)remaining_slots
                    3)current_patient: collection number
                    4)end_day : 0 for no 1 for yes
                    6 - SIZE-1) schedule
                    
            2)Action Space:
                An action consists of a number between 0 and DAYS*SLOTS-1, we can extract 
                the slot and the day from action as follows:
                    slot = action mod SLOTS
                    day = (action - slot)/SLOTS
        """
        self.observation_space = spaces.Box(low = 0, high = SIZE, shape = (SIZE,), dtype = int)
        
        self.action_space = spaces.Discrete(DAYS)
        
        
        #Observales that are not used by the agent
        self.overlap_count = 0
        self.total_reward = 0
        self.two_weeks_violation = 0
    
    
    
    def step(self,action):
        
        
        scheduled =  self.Tranistion(action)
        
        reward= self.Reward(action, scheduled)
        
        self.total_reward += reward

        obs = self.makeObs()
        
        done = self.done()
        
        
        return obs, reward, done, {}
        
        
        pass
    
    def reset(self):
        self.schedule = np.zeros((DAYS,SLOTS),dtype = int)
        self.current_day = 0
        self.current_patient_number = 1
        self.remaining_slots = DAYS*SLOTS
        
        self.patient = np.random.randint(1,COLLECTIONS+1)
        self.end_day = 0 
        
        self.overlap_count = 0
        self.total_reward = 0
        self.two_weeks_violation = 0
        
        obs = self.makeObs()
        
        return obs
    
    
    def render(self):
        print(self.schedule)
        print("day", self.current_day)
        print("Threre are ", self.overlap_count, "overlaps")
        print("Two Weeks Rule Violation", self.two_weeks_violation)
        print("Patient Number:",self.current_patient_number)
        print("total reward:", self.total_reward)
        print("Slots remaining:", self.remaining_slots)

        
#**********************************Basic Methods End ***********************************"""





#*********************************Helprer Methods Definition***************************"""
    
    

#************************ Foramting Logic ******************************"""
    def makeObs(self):
        return np.concatenate([np.array([self.current_day]),
                       np.array([self.current_patient_number]),
                       np.array([self.remaining_slots]),
                       np.array([self.patient]),
                       np.array([self.end_day]),
                       self.schedule.reshape(DAYS*SLOTS)])
    
    def done(self):
        return (self.current_day == DAYS or self.remaining_slots < COLLECTIONS)
    
    def extractSlotDay(self,action):

        day = action
        
        return int(day)
    
    
#*************************************************************************************"""



#********************************Transition Logic**************************************"""
    
    def Tranistion(self, action):
        scheduled = self.updateSchedule(action)
        
        self.updateDay(scheduled)
        self.updatePatientNumber(scheduled)
        self.updateRemainingSlots(scheduled)
        self.updatePatient(scheduled)
        self.updateEndOfDay(scheduled)
        
        return scheduled
    
    
    # you can add flags to use for rewards later
    def updateSchedule(self,action):
        
        day= self.extractSlotDay(action)
        
        collection_days = self.patient
        
        
        if(day < self.current_day):
            return False
        
    
        if(day + collection_days > DAYS):
            return False
        
        slots = []
        
        
        #Choose the slots over the collection days
        #If there is a day that is not empty, do not schedule
        for d in range(collection_days):
            empty = False
            
            for s in range(SLOTS):
                if self.schedule[day + d,s] == 0:
                    empty = True 
                    slots.append(s)
                    break
            if(not empty):
                self.overlap_count +=1 
                return False 
        
        
        
        #Schedule the days 
        for d in range(collection_days):
            self.schedule[day + d, s] = self.current_patient_number
        return True
        
        
            
    
    def updateDay(self, scheduled):
        if(scheduled):
            self.current_day += self.end_day
            self.remaining_slots = self.remaining_slots - self.end_day * SLOTS
    def updatePatientNumber(self,scheduled):
        if(scheduled):
            self.current_patient_number += 1
    
    def updateRemainingSlots(self,scheduled):
        if(scheduled):
            self.remaining_slots = self.remaining_slots - self.patient 
    
    def updatePatient(self,scheduled):
        if(scheduled):
            self.patient = np.random.randint(1,COLLECTIONS+1)
    
    def updateEndOfDay(self, scheduled):
        if(scheduled):
            self.end_day = np.random.binomial(1,NEXT_DAY_P)
        
        
#**************************************************************************************"""



#**********************************Reward Logic ***************************************"""

    def Reward(self,action, scheduled):
        
        
        reward =  self.slotReward(action,scheduled) 
        
        return reward
    
    def slotReward(self,action,scheduled):
        if(not scheduled):
            return -self.overlap_count
        else:
            day = self.extractSlotDay(action)
            # if(day < .1*(DAYS - self.current_day)):
              #  return 2*(((DAYS-self.current_day)-day)/(DAYS-self.current_day))

            #return 1*(((DAYS-self.current_day)-day)/(DAYS-self.current_day))
            return 10
    
    
    
    
    
    
    
    def twoWeeksReward(self,action,scheduled):
        if(scheduled):
            day = self.extractSlotDay(action)
            collection_days = self.patient
            
            if((day%5) + collection_days >5 ):
                self.two_weeks_violation += 1
                return -5
            return +1
        return 0
    
    
#**************************************************************************************"""