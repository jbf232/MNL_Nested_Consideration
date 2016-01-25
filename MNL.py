

#Function that returns MNL purchase probabilities
def PurchaseProbMNL(v, S, j):

	denom  = sum([v[i] for i in S])

	return float(v[j])/denom


#Function that returns MNL purchase probabilities
def PurchaseProbMNLOpt(v, S, g, j):

	if j > g:
		return 0
	else:
		denom  = sum([v[i] for i in S if i <=g])
		return float(v[j])/denom