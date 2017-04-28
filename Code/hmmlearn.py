import io, sys, copy
from collections import defaultdict

transition_dict = {}
emission_dict = {}
trasition_count = {}
emission_count = {}
transition_prob = {}
emission_prob = {}
last = {}
possible_tags_dict = {}

with open(sys.argv[1], "r")  as training_data:
    for line in training_data:
        tokens = line.split()
        prev = "q0"

        for token in tokens:
            if prev not in transition_dict:
                transition_dict[prev] = {}

            len_of_token = len(token)
            word = token.split("/")[0]
            tag = token.split("/")[1]

            if tag not in emission_dict:
                emission_dict[tag] = {}

            if trasition_count.has_key(prev):
                trasition_count[prev] += 1 
            else:
                trasition_count[prev] = 1

            if tag in transition_dict[prev]:
                transition_dict[prev][tag] += 1
            else:
                transition_dict[prev][tag] = 1

            if word in possible_tags_dict:
                possible_tags_dict[word].add(tag)
            else:
                possible_tags_dict[word] = set()
                possible_tags_dict[word].add(tag)

            if word in emission_dict[tag]:
                emission_dict[tag][word] += 1
            else:
                emission_dict[tag][word] = 1

            prev = tag

        if last.has_key(prev):
            last[prev] = last[prev] + 1
        else:
            last[prev] = 1

emission_count = copy.deepcopy(trasition_count)

for t in last:
    if t in trasition_count:
        emission_count[t] += last[t]
    else:
        if t not in emission_count:
            emission_count[t] = last[t]
        else:
            emission_count[t] += last[t]

len_transition_dict = 0
len_emission_dict = 0

f = open('hmmmodel.txt','wb')
len_of_trans_count = len(trasition_count)

for prev1 in transition_dict:
    for tag1 in transition_dict[prev1]:
        if prev1 not in transition_prob:
            transition_prob[prev1] = {}
        transition_prob[prev1][tag1] = (float)((1 + (float)(transition_dict[prev1][tag1])) / ((float)(trasition_count[prev1]) + len_of_trans_count))
        len_transition_dict += 1
    transition_prob[prev1]["qX"] = 1 / (((float)(trasition_count[prev1]) + len_of_trans_count))

f.write(str(len_transition_dict + len_of_trans_count) + "\n")

for prev1 in transition_dict:
    for tag1 in transition_dict[prev1]:
        s = prev1 +'\t'+ tag1 + '\t' + str(transition_prob[prev1][tag1]);
        f.write(s + "\n")
    s = prev1 + '\t'+ "qX" + '\t' + str(transition_prob[prev1]["qX"]);
    f.write(s + "\n")

for tag2 in emission_dict:
    for word2 in emission_dict[tag2]:
        if tag2 not in emission_prob:
            emission_prob[tag2] = {}
        emission_prob[tag2][word2] = (float)((float)(emission_dict[tag2][word2]) / emission_count[tag2])
        len_emission_dict += 1

f.write(str(len_emission_dict) + "\n")

for tag2 in emission_dict:
    for word2 in emission_dict[tag2]:
        s = tag2 + '\t' + word2 + '\t' + str(emission_prob[tag2][word2]);
        f.write(s + "\n")

for key, value in possible_tags_dict.iteritems():
    f.write(key + ' ')
    for all_tags in value:
        f.write(all_tags + ' ')
    f.write('\n')
