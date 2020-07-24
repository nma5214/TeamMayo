import gym
from gym import spaces
import numpy as np

class TwoSchechEnv(gym.Env):

    metadata = {'render.mode': ['human']}

    def __init__(self, DAYS, SLOTS1, SLOTS2, COLLECTIONS, NEXT_DAY_P ):

        ''' Variables:
        Days: total number of days to be scheduled for D1 and D2
        SLOTS1: available number of spots for process 1 (D1)
        SLOTS2: available number of spots for prcess 2 (D2) = SLOTS1 * 8
        COLLECTIONS: number of days needed for D1 (to collect the stem cells)
        '''
        #Variables used for the state

        # daily scheduled patient numbers for D1
        self.sched1 = np.zeros(DAYS)
        # daily scheduled patient numbers for D2
        self.sched2 = np.zeros(DAYS)

        # Number of collection days needed for current patient
        self.currentpatient_collection_day = np.random.choice(np.arange(1, COLLECTIONS+1), p=[0.4, 0.3, 0.15, 0.09, 0.06])

        # Current Day
        self.current_day = 0

        '''Observation Space
        '''
        # shape[0] : current day
        # shape[1] : patient collection number
        # shape[2: 1+DAYS] : schedule for D1
        # shape[2+DAYS : ] : schedule for D2
        shape_length = 1 + 1 + DAYS + DAYS

        # each column of the obs_space contains the information of current_day, collection_number, schedule_D1, schedule_D2
        self.observation_space = spaces.Box(low = 0 , high = SLOT1, shape = (2+DAYS+DAYS,), dtype = int)

        '''Action Space (D1, D2)
        '''
        self.action_space = spaces.MultiDiscrete(DAYS,DAYS)


        '''Internal variables we use to build the schedule
        '''
        # Initialize the patient number
        self.patient_number = 1
        # Matrix for sched1 and sched2
        self.MatrixSched1 = np.zeros((DAYS, SLOTS1))
        self.MatrixSched2 = np.zeros((DAYS, SLOTS2 * 9 ))
        self.Q1 = np.array([])

        self.end_day = 0 #???
        # remianing Slots
        self.remainingSlots1 = DAYS * SLOT1
        self.remainingSlots2 = DAYS * SLOT2 * 9

        # Counting variabels
        self.overlap_count = 0
        self.total_reward = 0
        self.two_weeks_violations = 0



    def step(self,action):
        # Tranistion returns A Boolean value, depending on whether scheduling happened
        schedled = self.Transition(action)
        # Reward returns reward value for each action based on whether scheduling happened
        reward = self.Reward(action,schedled)
        self.total_reward += reward
        # makeObs updates the observatoin space
        obs = self.makeObs()
        # done function check whether
        done = self.done
        return obs, reward, done, {}

    def reset(self, action):
        # same as __init__ ftn
        self.sched1 = np.zeros(DAYS)
        self.sched2 = np.zeros(DAYS)
        self.patient_collection_days = np.random.randint(1,COLLECTIONS)
        self.current_day = 0
        self.patient_index = 0 # patient index
        self.MatrixSched1 = np.zeros((DAYS1,SLOT1))
        self.MatrixSched2 = np.zeros((DAYS2,SLOTS2 * 9 ))
        self.Q1 = np.array([])
        self.end_day = 0
        self.remainingSlots1 = DAYS * SLOT1
        self.remainingSlots2 = DAYS * SLOT2 * 9
        self.overlap_count = 0
        self.total_reward = 0
        self.two_weeks_violations = 0

        obs = makeObs() # should we also initialize the observation space??
        return obs

    # Print out results
    def render(self):
        pass

    #************************ Foramting Logic ******************************"""


    # Makes an observation in the observation space format
    def makeObs(self):
        return np.concatenate([np.array([self.current_day]), np.array([self.currentpatient_collection_day]), self.sched1,
                              self.sched2])

    #  Tells us when to stop, return True or False
    def done(self):
        pass

    #********************************Transition Logic**************************************"""


    def Transition(self,action):
        #Returns boolean depending on whither scheduling happend or not
        scheduled = self.updateSched(action)
        #self.updateInternalStates(action)
        self.updateObservations(action, scheduled)

    def updateSched(self,action):
        d1 = action[0]
        d2 = action[1]
        if (d1 < self.current_day) or (d2 < self.current_day): # out of total days' range
            return False
        elif (d1 + self.currentpatient_collection_day < d2 ): # day2 < day1 + collection#
            return False
        elif self.sched1[d1] < SLOTS1 and self.sched2[d2] < SLOTS2: # do we need this?
            updateInternalStates(self, d1, d2)
            self.patient_index += 1 # go to next patient
            return True
        else:
            return False

    def updateInternalStates(self, day1, day2):
        # we can schedule the patient
        for i in range(SLOTS1):
            if (self.MatrixSched1[day1][i]) != 1: # when the slot is empty
                self.MatrixSched1[day1][i] = self.patient_index
                self.sched1[day1] += 1 # update scheduled patient for D1
                break
        for i in range(SLOTS2):
            if (self.MatrixSched2[day2][i]) != 1: # when the slot is empty
                self.MatrixSched2[day2][i] = self.patient_index
                self.sched2[day2] += 1 # update scheduled patient number for D2
                break



    def updateObservations(self,action,schedled):
        if schedled:
            self.observation_space


#**********************************Reward Logic ***************************************"""

    def Reward(self,action,scheduled):

        return self.SlotReward(action,scheduled) + self.QReward(action,scheduled)

    def SlotReward(self,action,scheduled):
        pass

    def QReward(self,action,scheduled):
        if scheduled:
            return self.currentpatient_collection_day*1.0/(action[1]-action[0])
