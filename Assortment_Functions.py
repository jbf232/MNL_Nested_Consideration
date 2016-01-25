import itertools as it  

#Function that gives all assortment in dictionary for specific customer class
def getAssortments(g):

	assortDict={}
	assortCount=1
	N=[i for  i in range(1,g+1)]
	for m in range(1,g+1):

		listAssorts = list(it.combinations(N,m))
		for assort in listAssorts:
			assortDict[assortCount] = [0] + list(assort)
			assortCount+=1

	return assortDict

def customerAssortDict(n):

	fullDict = {}
	for g in range(1, n+1):
		assortDict = getAssortments(g)
		fullDict[g] =assortDict

	return fullDict 

#Function that returns all assortment numbers for a customer types that have a product
def getAssortmentKeys(assortDict, j):

	listKeys = []
	for key in assortDict:

		assort = assortDict[key]
		if j in assort:
			listKeys+=[key]

	return listKeys





if __name__ == '__main__':
	assortDict =  getAssortments(3)
	print assortDict
	print getAssortmentKeys(assortDict, 1)
