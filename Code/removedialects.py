import sys

dialogues = []

with open(sys.argv[1], "rU") as text_file:
    for line in text_file:
    	print line
    	(dialogue, dialect) = line.split(" | ")
    	dialogues.append(dialogue)

with open(sys.argv[1][:-10] + "Untagged.txt", "w") as result_file:
	for dialogue in dialogues:
		result_file.write(dialogue + "\n")
