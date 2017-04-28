# -*- coding: utf-8 -*-

import sys
import codecs

file_to_untag = sys.argv[1]

file = open("UntaggedTrainingData/" + sys.argv[1].split("/")[1].split(".")[0] + "_untagged.txt" ,"w")

with codecs.open(file_to_untag,"r", encoding="utf-8") as file_untag:

    for line in file_untag:
        j = ""

        for i in line.split(" "):
            j += i.split("/")[0] + " "
        file.write(j.encode("utf-8") + "\n")