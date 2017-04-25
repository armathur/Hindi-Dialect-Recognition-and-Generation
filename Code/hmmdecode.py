import sys, copy, math, operator

def get_matrix(hmmmodel, matrix):
	k = hmmmodel.readline().rstrip()
	while k != "*****":
		line = hmmmodel.readline().rstrip()
		matrix[k] = eval(line)
		k = hmmmodel.readline().rstrip()

if __name__ == '__main__':

	transition_matrix = {}
	emission_matrix = {}

	hmmmodel = open('hmmmodel.txt','r')

	get_matrix(hmmmodel, transition_matrix)
	get_matrix(hmmmodel, emission_matrix)

	labels = transition_matrix.keys()
	labels.remove("q0")

	hmmoutput = open('hmmoutput.txt','w')

	with open(sys.argv[-1]) as f:
		for line in f:
			words = line.strip().split(' ')
			tags = ['' for i in range(len(words))]
			prev_labels = {}
			prev_labels[-1] = {}
			prev_labels[-1]["q0"] = [0, ""]

			for i, word in enumerate(words):
				prev_labels[i] = {}
				possible_labels = []

				for label in labels:
					if word in emission_matrix[label].keys():
						possible_labels.append(label)

				if not possible_labels:
					for prev_label in prev_labels[i - 1].keys():
						for label in transition_matrix[prev_label].keys():
							if label not in prev_labels[i].keys():
								prev_labels[i][label] = [prev_labels[i - 1][prev_label][0] + transition_matrix[prev_label][label], prev_label]
							else:
								prob = prev_labels[i - 1][prev_label][0] + transition_matrix[prev_label][label]
								if prob > prev_labels[i][label][0]:
									prev_labels[i][label] = [prob, prev_label]
				else:
					for possible_label in possible_labels:
						for prev_label in prev_labels[i - 1].keys():
							if possible_label in transition_matrix[prev_label].keys():
								if possible_label not in prev_labels[i].keys():
									prev_labels[i][possible_label] = [prev_labels[i - 1][prev_label][0] + transition_matrix[prev_label][possible_label] + emission_matrix[possible_label][word], prev_label]
								else:
									prob = prev_labels[i - 1][prev_label][0] + transition_matrix[prev_label][possible_label] + emission_matrix[possible_label][word]
									if prob > prev_labels[i][possible_label][0]:
										prev_labels[i][possible_label] = [prob, prev_label]

			tags[i] = max(prev_labels[i], key=prev_labels[i].get)

			while i > 0:
				i = i - 1
				tags[i] = prev_labels[i + 1][tags[i + 1]][1]

			for i in range(len(words)):
				hmmoutput.write(words[i] + '/' + tags[i] + ' ')
			hmmoutput.write('\n')
