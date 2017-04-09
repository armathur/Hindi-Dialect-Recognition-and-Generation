import sys

dialogues = []

with open(sys.argv[1], "rU") as text_file:
    for line in text_file:
    	(dialogue, dialect) = line.split(" | ")
    	dialogues.append(dialogue)

with open("Unt" + sys.argv[1][1:-10] + "Untagged.txt", "w") as result_file:
	for dialogue in dialogues:
		result_file.write(dialogue + "\n")
