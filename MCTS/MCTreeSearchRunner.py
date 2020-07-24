import random 
import gym 
import itertools
from math import sqrt, log

from time import time
from copy import copy



class MCTreeSearchNode():

	def __init__(self, parent,action):
		self.parent = parent
		self.action = action
		self.children = []
		self.explored_children = 0
		self.visits = 0
		self.value = 0


class Runner:

	def __init__(self, env, loops = 300, max_depth = 1000, playouts = 10000):
		self.env = env

		self.loops = loops
		self.max_depth = max_depth
		self.playouts = playouts




	def ucb(node):
		return node.value / node.visits + sqrt(log(node.parent.visits)/ node.visits)


	def combinations(space): #Complete This function
		if isinstance(space,gym.spaces.Discrete):
			return range(space.n)

	def print_stats(self,loop, score, avg_time):
		print("loop:", loop, "| score :", score, "| average time:", avg_time)



	def run(self):

		best_rewards = []
		start_time = time()
		
		for loop in xrange(self.loops):
			self.env.reset()

			root = MTCSTreeSearchNode(None,None)

			best_actions = []
			best_reward = float("-inf")

			for _ in xrange(self.playout):
				state = copy(self.enf)

				sum_rewards  = 0 
				node = root 
				terminal = False 
				actions = [] 

				#Selection step 

				while node.children :
					if node.explored_children < len(node.children):
						child = node.children[node.explored_children]
						node.explored_children += 1
						node = child
					else:
						node = max(node.children, key=ucb)
						_,reward,terminal,_ = self.env.step(node.action)
						sum_rewards += reward 
						actions.append(node.action)

				#expansion
				


