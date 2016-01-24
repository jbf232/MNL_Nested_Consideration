

#Function that returns MNL purchase probabilities
def PurchaseProbMNL(v, S, j):

	denom  = sum([v[i] for i in S])

	return v[j]/denom
