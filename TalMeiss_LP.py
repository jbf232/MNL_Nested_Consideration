from MNL import *
from Assortment_Functions import *
import numpy as np
import math
from gurobipy import *


def SolveLP(v,r):

	#Assumes v includes the no purchase option
	n = len(v)-1
	fullAssortDict = customerAssortDict(n) 
	

	m=Model("LP")

	#Create 
	h={}
	for g in range(1, n+1):

		assortDict=fullAssortDict[g]
		for key in assortDict:

			S = assortDict[key]
			revS=0
			for j in assort:

				revS+=PurchaseProbMNL(v,S,j)]*r[j]
		
			h[g,key]=m.addVar(0,1,-revS,  GRB.CONTINUOUS,"h_%d%d" %(g,key))

    #Update new variables
	m.update()

	#Constraints that the sum of the variables has to be less than 1
	for g in range(1, n+1):
		m.addConstr(LinExpr([1]*(2**(g-1)),[h[g,assortNum] for assortNum in range(1, 2**(g-1) + 1)]),GRB.LESS_EQUAL,1)

	#The cuts
	for g in range(1,n+1):
		assortDict=fullAssortDict[g]
		for j in range(1, g+1):
			
			gList=getAssortmentKeys(assortDict, j)
			for h in range(j, n+1):
				if h != g:
				assortDict=fullAssortDict[h]
				hList=getAssortmentKeys(assortDict, j)
				m.addConstr(LinExpr([1 for i in range(len(gList))] + [-1 for i in range(len(hList))],\
					[h[g,assortNum] for assortNum in gList] + [h[h,assortNum] for assortNum in hList]),GRB.EQUAL,0)


	m.setParam( 'OutputFlag', False )
	m.optimize()

	# LPSol={}
	# assortNum=0
	# for v in m.getVars():
	# 	if v.X>0:
	# 		LPSol[assortNum]=v.X
	# 	assortNum+=1


	return m.objVal