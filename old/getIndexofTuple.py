def getIndexOfTuple(l, index, value):
	for pos,t in enumerate(l):
		if t[index] == value:
			return pos
	raise ValueError("list.index(x): x not in list")
#getIndexOfTuple END