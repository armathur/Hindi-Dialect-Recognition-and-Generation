import sys
import math
from collections import defaultdict

f = open('hmmmodel.txt','rU')

transition_dict = {}
transition_list = {}
emission_dict = {}
possible_tags = {}

len_of_transition_dict = (int)(f.readline())
# print len_of_transition_dict
for i in range(0, len_of_transition_dict):
	l = f.readline()
	prev, tag, transition_prob = l.split("\t")
	#print prev, tag, transition_prob
	if prev not in transition_dict:
		transition_dict[prev] = {}
		transition_list[prev] = []
	transition_dict[prev][tag] = (float)(transition_prob.strip("\n"))
	
	transition_list[prev].append(tag)

# print transition_dict
# print transition_list

len_of_emission_dict = (int)(f.readline())
# print len_of_emission_dict
for i in range(0, len_of_emission_dict):
	l = f.readline()
	tag, word, emission_prob = l.split("\t")
	#print tag, word, emission_prob
	if tag not in emission_dict:
		emission_dict[tag] = {}
	emission_dict[tag][word] = (float)(emission_prob.strip("\n"))

#read from model all the possible tags for each word
for l in f:
	#list of all possible tags for a word in the training set
	l = l.rstrip()
	slices = l.split(" ")
	#print slices
	len_of_slices = len(slices)
	#print len_of_slices
	w = slices[0]
	#print w
	ls = set()
	for i in range(1, len_of_slices):
		ls.add(slices[i])
	if w not in possible_tags:
		possible_tags[w] = {}
	possible_tags[w] = ls
	
# print transition_dict
# print "\n"
# print emission_dict
# print "\n"
# print possible_tags
# print "\n"



output_file = open("hmmoutput.txt", "w")


test_file_path = sys.argv[1]
test_file = open(test_file_path,"rU")


for line in test_file:
	line = line.rstrip() # each sentence in the test file
		
	viterbi_probability = {}
	poss_tag_list = defaultdict(list)
	backptr = {}
	poss_tag_list[0] = {"q0"}
	viterbi_probability[0, "q0"] = 0.0 #viterbi_probability[t, state] = prob
	# print poss_tag_list
	# print viterbi_prob 
	# print "\n"
	words = line.split(" ")
	#print words
	prev_tags = poss_tag_list[0]
	# print prev_tags

	count = 1
	for word in words:
		#print word
		current_tag_list = []
		if possible_tags.has_key(word): #word is in training data
			# print "\nPOSSIBLE TAGS: "
			# print possible_tags[word]
			# print "\n"
			current_tag_list = possible_tags[word]
			# print current_tag_list
		else: #new word which is not present in the training set
			# print "NOT IN TRAINING SET#############"
			for prev_tag in prev_tags: #repeat for all previous tags
				# print "\n"
				# print prev_tag
				# print transition_list[prev_tag]
				if prev_tag in transition_list:
					for t in transition_list[prev_tag]: 
						#print t  
						if t not in current_tag_list:
						# t = transition_list[prev_tag]
						# print t
							if t!='qX':
								# print t
								current_tag_list.append(t) #add all the states to the current_tag_list which can be reached from the prev_tag
							
		# print current_tag_list    


		#check each tag in the current_tag_list to select the one with maximum probaility
		for current_tag in current_tag_list: #consider possible tags one by one
			max_prob = float('-inf')
			max_tag = ""
			# print current_tag
			for prev_tag in prev_tags:
				# print prev_tag

				if prev_tag in transition_dict:
					if current_tag in transition_dict[prev_tag]:
						p1 = transition_dict[prev_tag][current_tag] #p1 -> transition probability from prev_tag to current_tag
						# print p1
					else: p1 = transition_dict[prev_tag]["qX"]
				# else:
				# 	p1 = transition_dict[prev_tag]["qX"]

				if current_tag in emission_dict:
					if word in emission_dict[current_tag]:
						p2 = emission_dict[current_tag][word] #p2 -> emission probability of the word given current_tag
						# print p2
					else: p2 = 1.0
				else: p2 = 1.0 #no add-1 smoothing

				p3 = viterbi_probability[count-1, prev_tag] #p3 -> max probability of the previous tag at time (t-1)
				# print p3

				prob = math.log(p1)+math.log(p2)+(float)(p3) #lof probability
				# print prob
				# print max_prob
				if prob > max_prob:
					# print("Greater!")
					max_prob = prob
 					max_tag = prev_tag
 					#print maxprob, maxtag
 			
 			poss_tag_list[count].append(current_tag)
			viterbi_probability[count,current_tag] = max_prob
			backptr[count,current_tag] = max_tag

		prev_tags = poss_tag_list[count] #possible tags at given time t
		count = count+1 

	# print poss_tag_list
	# print viterbi_prob
	# print backptr
#------------------------------------------------------------------------------------------------------------

	max_prob = float('-inf')
	max_tag = ''


	#find the max_tag for the last word and then go in reverse to find the max_tag for the remaining words
	len_of_poss_tag_list = len(poss_tag_list) - 1
	# print len_of_poss_tag_list
	#print poss_tag_list[len_of_poss_tag_list]

	for poss_tag in poss_tag_list[len_of_poss_tag_list]: #iterate through the list of possible tags of the last word
		# print poss_tag
		if viterbi_probability[len_of_poss_tag_list,poss_tag] > max_prob:
			max_prob = viterbi_probability[len_of_poss_tag_list,poss_tag]
			max_tag = poss_tag
	# print max_tag

	# print "\nTagging"

	final_tag = {}
	for x in range(len_of_poss_tag_list, 0, -1): #traverse in reverse
		#print x
		final_tag[words[x-1]] = max_tag
		max_tag = backptr[x, max_tag]
		#print maxtag
	# print final_tag	

	for word in words:
		s = word + "/" + final_tag[word] + " "
		output_file.write(s)
	output_file.write("\n")