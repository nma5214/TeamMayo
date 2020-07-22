"""
only simulate 2 patients over 2 weeks
Assume that number of nurses and spaces are fixed 
for D1 and D2
"""

import gurobipy
import numpy as np


C = [3,2] #number of collections 
P = [10,4] #number of nurses available for D1, D2
S = [10,4] #number of spaces available for D1, D2
tend = 14 #number of days for scheduling
W = [14,3] #target number of patients in any given days for D1, D2

# Create model
model = gurobipy.Model()

### Decision variables
D1 = model.addVars(len(C),lb = 0, ub = 13, vtype=gurobipy.GRB.INTEGER, name='D1_start')
D2 = model.addVars(len(C),lb = 0, ub = 13, vtype=gurobipy.GRB.INTEGER, name='D2')

### Constraints

# define variables
    #D1 daily counts
D1_ij = np.zeros([len(C),tend], dtype = int)
for i in range(len(C)):
    #lastday = D1[i]+C[i]-1+(D1[i]%7+C[i])//7*2
    lhs = gurobipy.LinExpr()
    lhs.add(D1[i],C[i],-1,(D1[i]%7+C[i])//7*2)
    for j in range(tend):
        if (D1[i]<=j and j<=lhs and j%7!=0 and j%7!=1):
            D1_ij[i][j] = 1

T1J = D1_ij.sum(axis=0) #column sum gives the total patients in one day, 1 x tend vector

#D2 daily counts
D2_ij = np.zeros([len(C),tend],dtype=int)
for i in range(len(C)):
    for j in range(tend):
        if (j==D2[i]):
            D2_ij[i][j] = 1
            
T2J = D2_ij.sum(axis=0) #column sum 

# add constraints: we cannot have more patients than spaces for each procedure
model.addConstrs((T1J[j]<=S[0] for j in range(tend)), name='D1Capacity')
model.addConstrs((T2J[j]<=S[1] for j in range(tend)), name='D2Capacity')

# add constraint: D2 only happens after D1 finishes
model.addConstrs((D1[i]+C[i]-1+(D1[i]%7+C[i])//7*2 < D2[i] \
                  for i in range(len(C))), name='flowOrder')

### Objective function
    #define varibles   
Q = gurobipy.quicksum(D2[i]-(D1[i]+C[i]-1+(D1[i]%7+C[i])//7*2) for i in range(len(C))) #wait time between D1 and D2
sigma1 = gurobipy.quicksum(abs(W[1]-T1J[j]) for j in range(tend)) #variation for D1 daily patients
sigma2 = gurobipy.quicksum(abs(W[2]-T2J[j]) for j in range(tend)) #variation for D2 daily patients

VN = np.zeros(len(C), dtype=int) #nursing violations for D1, D2
T = np.stack((T1J,T2J),axis=0) #combine T1J and T2J into one matrix
# calculate VN1 and VN2
for i in range(len(T)):
    for j in range(tend):
        if(T[i][j]>=P[i]):
            VN[i] += 1


model.setObjective(Q+sigma1+sigma2+VN[1]+VN[2], sense=gurobipy.GRB.MINIMIZE)
 
model.optimize() #optimize the model

# check the status to see if there is a solution
status = model.getAttr("Status")
if status == 2:
    for j in range(len(C)):
        print("Patient "+str(j)+"schedule (D1,D2):(", D1[j].getAttr("X"), D2[j].getAttr("X"),")")
    print(model.getAttr("ObjVal"))
else:
    print("No optimal solution found.")

