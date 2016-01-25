from MNL import *
from Assortment_Functions import *
import numpy as np
import math
from gurobipy import *


def Opt(v,r, lam):
	"""Solves the LP.  Make sure both v and r have the no purchase option. Pad lam with one entry since first customer
		type has index 1.
	"""

	#Assumes v includes the no purchase option
	n = len(v)-1
	fullAssortDict = customerAssortDict(n) 
	

	m=Model("LP")

	#Create 
	h={}

	assortDict=fullAssortDict[n]
	for key in assortDict:

		S = assortDict[key]
		revS=0
		for g in range(1,n+1):
			for j in S:
				revS+=lam[g]*PurchaseProbMNLOpt(v,S,g,j)*r[j]

	
		h[key]=m.addVar(0,1,-revS,  GRB.BINARY,"h_%d%d" %(g,key))

	#Update new variables
	m.update()

	#Constraints that the sum of the variables has to be less than 1
	
	m.addConstr(LinExpr([1]*(2**n -1),[h[assortNum] for assortNum in range(1, 2**n )]),GRB.LESS_EQUAL,1)



	m.setParam( 'OutputFlag', False )
	m.optimize()

	# LPSol={}
	# assortNum=0
	# for v in m.getVars():
	# 	if v.X>0:
	# 		LPSol[assortNum]=v.X
	# 	assortNum+=1


	return m.objVal