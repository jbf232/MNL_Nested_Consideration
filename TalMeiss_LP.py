from MNL import *
from Assortment_Functions import *
from Opt import *
import numpy as np
import math
from gurobipy import *
import xlwt



def SolveLP(v, v_0, r, lam):
	"""Solves the LP.  Make sure both v and r have the no purchase option.
	"""

	#Assumes v includes the no purchase option
	n = len(v)
	fullAssortDict = customerAssortDict(n) 
	

	m=Model("LP")

	#Create 
	h={}
	for g in range(1, n+1):

		assortDict=fullAssortDict[g]
		for key in assortDict:

			S = assortDict[key]
			revS=0
			for j in S:
				revS+=lam[g-1]*PurchaseProbMNL([v_0[g-1]]+v,S,j)*r[j]
		
			h[g,key]=m.addVar(0,1,-revS,  GRB.CONTINUOUS,"h_%d%d" %(g,key))

    #Update new variables
	m.update()

	#Constraints that the sum of the variables has to be less than 1
	for g in range(1, n+1):
		m.addConstr(LinExpr([1]*(2**g -1),[h[g,assortNum] for assortNum in range(1, 2**g)]),GRB.LESS_EQUAL,1)

	#The 1-product cuts
	for g in range(1,n+1):
		assortDictG=fullAssortDict[g]

		for j in range(1, g+1):
			
			gList=getAssortmentKeys(assortDictG, j)
			for k in range(j, n+1):
				if k != g:

					assortDictK=fullAssortDict[k]
					KList=getAssortmentKeys(assortDictK, j)
					m.addConstr(LinExpr([1 for i in range(len(gList))] + [-1 for i in range(len(KList))],\
					[h[g,assortNum] for assortNum in gList] + [h[k,assortNum] for assortNum in KList]),GRB.EQUAL,0)


	#The 2-product cuts
	for g in range(1,n+1):
		assortDictG=fullAssortDict[g]
		for j in range(1, g+1):
			for i in range(j+1,g+1):

				gList=getAssortmentKeysTwo(assortDictG, [j,i])
				for k in range(j, n+1):
					if k != g:

						assortDictK=fullAssortDict[k]
						KList=getAssortmentKeysTwo(assortDictK, [j,i])
						if KList != []:

							m.addConstr(LinExpr([1 for q in range(len(gList))] + [-1 for w in range(len(KList))],\
							[h[g,assortNum] for assortNum in gList] + [h[k,assortNum] for assortNum in KList]),GRB.EQUAL,0)


	m.setParam( 'OutputFlag', False )
	m.optimize()

	# LPSol={}
	# assortNum=0
	# for v in m.getVars():
	# 	if v.X>0:
	# 		LPSol[assortNum]=v.X
	# 	assortNum+=1


	return -m.objVal

if __name__ == '__main__':

	numTestCase=10
	numProds=10
	text_file = open("Data.txt", "r")
	lines = text_file.readlines()


	book = xlwt.Workbook()

	sheet1 = book.add_sheet("Sheet 1")


	for t in range(numTestCase):
		dataString  = lines[t].split(" ")
		rVec = [0]+[float(r) for r in dataString[1:1+numProds]]
		vVec = [float(v) for v in dataString[2 + numProds:2 + 2*numProds ]]
		v_0Vec = [float(v_0) for v_0 in dataString[3 + 2*numProds: 3 + 3*numProds ]]
		lamVec = [float(l) for l in dataString[4 + 3*numProds: 4 + 4*numProds ]]
		UB = SolveLP(vVec, v_0Vec, rVec, lamVec)
		sheet1.write(t, 0, UB)

	book.save("Tal_Meis_UB.xls")
	
