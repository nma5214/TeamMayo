'''
How to use this code
'''
#step 1: set up the enviroment
env = TwoSchechEnv()

#step 2: copy down the following code to run our Modified greedy algorithm
obs = env.reset()
time = 1000
step = 0
actions = []
img = []
window1 =7
window2 = 3
while step < time and env.current_day <=DAYS:
    action =  modGreedyStep(env,window1,window2)
    actions.append(action)
    env.step(action)
    step +=1

# output the figure for D1 stem collection stage
env.render(2,1.6)
# output the figure for D2 Prechemo stage
env.render(3,1.6)
# output the summary figure for Q1 and the dataset of Q1
env.render(4)
env.Q1

# Step3: You can run this step if you want to compare the modified greedy algorithm results
# ... with the greedy algorithm

obs = env.reset()
done = False
step = 0
while ((not done) and step < 5000):
    step += 1
    action = env.action_space.sample()
    env.step(action)
    done = env.done()

# output the figure for D1 stem collection stage
env.render(2,1.6)
# output the figure for D2 Prechemo stage
env.render(3,1.6)
# output the summary figure for Q1 and the dataset of Q1
env.render(4)
env.Q1
