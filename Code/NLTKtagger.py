# # -*- coding: utf-8 -*-
#
# from nltk.corpus import indian
# from nltk.tag import tnt
# import nltk
#
# train_data = indian.tagged_sents('hindi.pos')
# tnt_pos_tagger = tnt.TnT()
# tnt_pos_tagger.train(train_data) #Training the tnt Part of speech tagger with hindi data
#
# with open("devnagri_untagged","r") as untagged:
#     for line in untagged:
#         print(tnt_pos_tagger.tag(nltk.word_tokenize(unicode(line,"utf-8"))))
#
#
#

# -*- coding: utf-8 -*-

from nltk.corpus import indian
from nltk.tag import tnt
import nltk


train_data = indian.tagged_sents('hindi.pos')
tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(train_data) #Training the tnt Part of speech tagger with hindi data
list_tagged = []

with open("devnagri_untagged","r") as untagged:
    for line in untagged:
        list_tagged.append(tnt_pos_tagger.tag(nltk.word_tokenize(unicode(line,"utf-8"))))

file = open("out.txt","w")
for each in list_tagged:
    l = ""
    for i in each:
        l += i[0]+"/"+ i[1] + " "
    file.write(l.encode("utf-8"))
    file.write("\n")






        # print(unicode(each,"utf-8"))