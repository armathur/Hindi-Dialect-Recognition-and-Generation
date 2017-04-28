import sys, math
from collections import defaultdict

f = open("hmmmodel.txt", "rU")

transition_dict = {}
transition_list = {}
emission_dict = {}
possible_tags = {}

len_of_transition_dict = (int)(f.readline())
for i in xrange(0, len_of_transition_dict):
	l = f.readline()
	prev, tag, transition_prob = l.split("\t")

	if prev not in transition_dict:
		transition_dict[prev] = {}
		transition_list[prev] = []
	transition_dict[prev][tag] = (float)(transition_prob.strip("\n"))
	transition_list[prev].append(tag)

len_of_emission_dict = (int)(f.readline())
for i in xrange(0, len_of_emission_dict):
	l = f.readline()
	tag, word, emission_prob = l.split("\t")
	if tag not in emission_dict:
		emission_dict[tag] = {}
	emission_dict[tag][word] = (float)(emission_prob.strip("\n"))

for l in f:
	l = l.rstrip()
	slices = l.split(" ")
	len_of_slices = len(slices)

	w = slices[0]
	ls = set()
	for i in xrange(1, len_of_slices):
		ls.add(slices[i])
	if w not in possible_tags:
		possible_tags[w] = {}
	possible_tags[w] = ls
	
output_file = open("hmmoutput.txt", "w")

test_file_path = sys.argv[1]
test_file = open(test_file_path,"rU")

for line in test_file:
	line = line.rstrip()	
	viterbi_probability = {}
	poss_tag_list = defaultdict(list)
	backptr = {}
	poss_tag_list[0] = {"q0"}
	viterbi_probability[0, "q0"] = 0.0 
	words = line.split(" ")
	prev_tags = poss_tag_list[0]

	count = 1
	for word in words:
		current_tag_list = []
		if possible_tags.has_key(word):
			current_tag_list = possible_tags[word]
		else:
			for prev_tag in prev_tags:
				if prev_tag in transition_list:
					for t in transition_list[prev_tag]: 
						if t not in current_tag_list:
							if t != "qX":
								current_tag_list.append(t)

		for current_tag in current_tag_list:
			max_prob = float("-inf")
			max_tag = ""
			for prev_tag in prev_tags:
				if prev_tag in transition_dict:
					if current_tag in transition_dict[prev_tag]:
						p1 = transition_dict[prev_tag][current_tag]
					else:
						p1 = transition_dict[prev_tag]["qX"]

				if current_tag in emission_dict:
					if word in emission_dict[current_tag]:
						p2 = emission_dict[current_tag][word]
					else:
						p2 = 1.0
				else:
					p2 = 1.0

				p3 = viterbi_probability[count - 1, prev_tag]

				prob = math.log(p1) + math.log(p2) + (float)(p3)
				if prob > max_prob:
					max_prob = prob
 					max_tag = prev_tag
 			
 			poss_tag_list[count].append(current_tag)
			viterbi_probability[count,current_tag] = max_prob
			backptr[count,current_tag] = max_tag

		prev_tags = poss_tag_list[count]
		count = count + 1 

	max_prob = float("-inf")
	max_tag = ""
	len_of_poss_tag_list = len(poss_tag_list) - 1

	for poss_tag in poss_tag_list[len_of_poss_tag_list]:
		if viterbi_probability[len_of_poss_tag_list,poss_tag] > max_prob:
			max_prob = viterbi_probability[len_of_poss_tag_list,poss_tag]
			max_tag = poss_tag

	final_tag = {}
	for x in xrange(len_of_poss_tag_list, 0, -1):
		final_tag[words[x - 1]] = max_tag
		max_tag = backptr[x, max_tag]

	for word in words:
		s = word + "/" + final_tag[word] + " "
		output_file.write(s)
	output_file.write("\n")
	