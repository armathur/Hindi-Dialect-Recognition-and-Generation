#HMM POS Tagger for Catalan
import io
from collections import defaultdict
import sys
import copy

#file_path = sys.argv[1]
#print file_path
#lines = [line.rstrip('\n') for line in open(file_path)]

transition_dict = {} #of the form: {q0: {{NN:2}. {VB,4}}....}
emission_dict = {}
trasition_count = {}
emission_count = {}
transition_prob = {}
emission_prob = {}
last = {}
possible_tags_dict = {}


#input_path="hmm_train.txt"
input_path = sys.argv[1]
with open(input_path, "r")  as training_data:
    for line in training_data:
        tokens = line.split()
        # print "\n"
        # print(tokens)
        prev="q0"
        
        #trasition_count[prev] += 1
       

        for token in tokens:

            if prev not in transition_dict:
              transition_dict[prev] = {}
              #print "make new tag entry for prev" + prev

            len_of_token=len(token)
            #print(token)
            #print(len_of_token)
            word=token[0:len_of_token-3]
            tag=token[len_of_token-2:len_of_token]
            # print "WORD: " + word
            # print "TAG: " + tag
            # print "PREV: " + prev

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
        #store the last tags
        if last.has_key(prev):
          last[prev]=last[prev]+1
        else:
          last[prev] = 1




# print transition_dict 
# print "\n"
# print trasition_count
# print "\n"
# print emission_dict
# print "\n"
# print last
# print "\n"

emission_count = copy.deepcopy(trasition_count)

for t in last:
  if t in trasition_count:
     emission_count[t] += last[t]

  else:
     if t not in emission_count:
        emission_count[t] = last[t]
     else:
        emission_count[t] += last[t]

     


# print trasition_count
# print "\n"
# print emission_count
# print "\n"

len_transition_dict = 0
len_emission_dict = 0

f = open('hmmmodel.txt','wb')
len_of_trans_count = len(trasition_count)
# print "\n TRns count "
# print  len_of_trans_count 

#f.write('Transmition\n')

for prev1 in transition_dict:
  for tag1 in transition_dict[prev1]:
    #print prev1, tag1
    if prev1 not in transition_prob:
      transition_prob[prev1] = {}
    transition_prob[prev1][tag1] = (float)((1 + (float)(transition_dict[prev1][tag1])) / ((float)(trasition_count[prev1]) + len_of_trans_count))  #add 1 smoothing

    #(no. of transitions from prev1->tag1)/(no. of prev1 tags)
    len_transition_dict += 1
  
  transition_prob[prev1]["qX"] = 1 / (((float)(trasition_count[prev1]) + len_of_trans_count))
#print transition_prob

#len_transition_dict = len(transition_dict)
# print "\n Length of transition dict: " + str(len_transition_dict + len_of_trans_count)

f.write(str(len_transition_dict + len_of_trans_count) + "\n")

for prev1 in transition_dict:
  for tag1 in transition_dict[prev1]:
    s = prev1 +'\t'+ tag1 + '\t' + str(transition_prob[prev1][tag1]);
    f.write(s+"\n")
  s = prev1 + '\t'+ "qX" + '\t' + str(transition_prob[prev1]["qX"]);
  f.write(s+"\n")



#f.write('Emission\n')

for tag2 in emission_dict:
  for word2 in emission_dict[tag2]:
    #print prev1, tag1
    if tag2 not in emission_prob:
      emission_prob[tag2] = {}
    emission_prob[tag2][word2] = (float)((float)(emission_dict[tag2][word2]) / emission_count[tag2])
    #(no. of transitions from prev1->tag1)/(no. of prev1 tags)
    len_emission_dict += 1
    
                    
#len_emission_dict = len(emission_dict)
# print "\n Length of emission dict: " + str(len_emission_dict)

f.write(str(len_emission_dict) + "\n")

for tag2 in emission_dict:
  for word2 in emission_dict[tag2]:
    s = tag2 +'\t'+ word2 + '\t' + str(emission_prob[tag2][word2]);
    f.write(s+"\n")

for key, value in possible_tags_dict.iteritems():
    f.write(key+' ')
    for all_tags in value:
        f.write(all_tags+' ')
    f.write('\n')



# print transition_prob
# print emission_prob
# print possible_tags_dict