from __future__ import print_function
import sys, math, codecs
#import tensorflow as tf
import numpy as np

class HMM(object):
    def __init__(self, P, initial=None):
        self.K = P.shape[0]

        self.P = P
        self.logP = np.log(self.P)

        if initial is None:
            self.initial = np.ones(self.K)
            self.initial /= sum(self.initial)
        elif len(initial) != self.K:
            raise ValueError(
                'dimensions of initial {} must match P[0] {}'.format(
                    initial.shape, P.shape[0]))
        else:
            self.initial = initial
        self.loginitial = np.log(self.initial)

class HMMNumpy(HMM):
    def _viterbi_partial_forward(self, scores):
        tmpMat = np.zeros((self.K, self.K))
        for i in range(self.K):
            for j in range(self.K):
                tmpMat[i, j] = scores[i] + self.logP[i, j]
        return tmpMat

    def viterbi_decode(self, y):
        y = np.array(y)

        nT = y.shape[0]

        pathStates = np.zeros((nT, self.K), dtype=np.int)
        pathScores = np.zeros((nT, self.K))

        # initialize
        pathScores[0] = self.loginitial + np.log(y[0])

        for t, yy in enumerate(y[1:]):
            # propagate forward
            tmpMat = self._viterbi_partial_forward(pathScores[t])

            # the inferred state
            pathStates[t + 1] = np.argmax(tmpMat, 0)
            pathScores[t + 1] = np.max(tmpMat, 0) + np.log(yy)

        # now backtrack viterbi to find states
        s = np.zeros(nT, dtype=np.int)
        s[-1] = np.argmax(pathScores[-1])
        for t in range(nT - 1, 0, -1):
            s[t - 1] = pathStates[t, s[t]]

        return s, pathScores

def split_line(line):
	words_and_tags = line.strip().split(' ')
	for i in range(len(words_and_tags)):
		word_and_tag = words_and_tags[i].split('/')
		tag = word_and_tag[-1]
		if len(word_and_tag) > 2:
			word = '/'.join(word_and_tag[:-1])
		else:
			word = word_and_tag[0]
		words_and_tags[i] = [word, tag]
#	print words_and_tags
	return words_and_tags

def smooth(matrix, col):
	for row in matrix.keys():
		matrix[row][col] = 1.0

def add_to_transitions(matrix, row, col):
	if row not in matrix:
		matrix[row] = {}
	if col not in matrix[row]:
		smooth(matrix, col)
	matrix[row][col] = matrix[row][col] + 1.0

def add_to_emissions(matrix, row, col):
	if row not in matrix:
		matrix[row] = {}
	if col not in matrix[row]:
		matrix[row][col] = 0.0
	matrix[row][col] = matrix[row][col] + 1.0

def update_transitions(words_and_tags, transition_matrix):
	add_to_transitions(transition_matrix, 'q0', words_and_tags[0][1])
	for i in range(len(words_and_tags) - 1):
		add_to_transitions(transition_matrix, words_and_tags[i][1], words_and_tags[i + 1][1])

def update_emissions(words_and_tags, emission_matrix, word_set):
	for i in range(len(words_and_tags)):
		add_to_emissions(emission_matrix, words_and_tags[i][1], words_and_tags[i][0])
		word_set.add(words_and_tags[i][0])

def calculate_probabilities(matrix):
	for x in matrix.keys():
		total = sum(matrix[x].values())
		for y in matrix[x].keys():
			matrix[x][y] = math.log(matrix[x][y] / total)

def write_model(hmmmodel, matrix):
	for d in matrix.items():
		hmmmodel.write(str(d[0]) + '\n')
		hmmmodel.write(str(d[1]) + '\n')
	hmmmodel.write('*****\n')

def dptable(V, pathScores, states):
    print(" ".join(("%10d" % i) for i in range(V.shape[0])))
    for i, y in enumerate(pathScores.T):
        print("%.7s: " % states[i])
        print(" ".join("%.7s" % ("%f" % yy) for yy in y))

if __name__ == '__main__':

	transition_matrix = {}
	emission_matrix = {}
	states = {}
	obs = {}
	reverse_obs = {}
	initial = []
	transitions = []
	emissions = []
	word_set = set()

	with codecs.open(sys.argv[1], 'r', 'utf-8') as tagged_file:
		for line in tagged_file:
			words_and_tags = split_line(line)
			update_transitions(words_and_tags, transition_matrix)
			update_emissions(words_and_tags, emission_matrix, word_set)

	calculate_probabilities(transition_matrix)
	calculate_probabilities(emission_matrix)

	i = 0
	for state in transition_matrix.keys():
		if state != 'q0':
			states[i] = state
			i += 1

	for i in xrange(len(states.keys())):
		if transition_matrix['q0'][states[i]]:
			initial.append(transition_matrix['q0'][states[i]])
		else:
			initial.append(0.0)

	for i in xrange(len(states.keys())):
		row = [0.0] * len(states.keys())
		if states[i] in transition_matrix.keys():
			for j in xrange(len(states.keys())):
				if states[j] in transition_matrix[states[i]].keys():
					row[j] = transition_matrix[states[i]][states[j]]
		transitions.append(row)

	j = 0
	for word in word_set:
		obs[j] = word
		reverse_obs[word] = j
		row = [0.0] * len(states.keys())
		for i in xrange(len(states.keys())):
			if states[i] in emission_matrix.keys() and word in emission_matrix[states[i]].keys():
				row[i] = emission_matrix[states[i]][word]
		emissions.append(row)

	p0 = np.array(initial)
	trans = np.array(transitions)
	emi = np.array(emissions)

	np_model = HMMNumpy(trans, p0)

	hmmoutput = codecs.open('hmmoutput.txt','w', 'utf-8')

	with codecs.open(sys.argv[2], 'r', 'utf-8') as untagged_file:
		for line in untagged_file:
			words = line.strip().split()
			line = []

			for word in words:
				if word in word_set:
					line.append(reverse_obs[word])

			obs_seq = np.array(line)
			y = emi[obs_seq]
			np_states, np_scores = np_model.viterbi_decode(y)
			pathScores = np.array(np.exp(np_scores))

			pathScores = np.array(np.exp(np_scores))
    		dptable(pathScores, pathScores, states)
			


#	hmmmodel = codecs.open('hmmmodel.txt','w', 'utf-8')
#	write_model(hmmmodel, transition_matrix)
#	write_model(hmmmodel, emission_matrix)
