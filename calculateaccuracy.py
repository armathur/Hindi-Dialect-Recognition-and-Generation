import sys

predictions = []
answers = []

correct_lines = 0

with open(sys.argv[1], "r") as prediction_file:
    for line in prediction_file:
    	(dialogue, dialect) = line.split(" | ")
    	predictions.append(dialogue)

with open(sys.argv[2], "r") as answer_file:
    for line in answer_file:
    	(dialogue, dialect) = line.split(" | ")
    	answers.append(dialogue)

total_lines = len(predictions)

for i in range(total_lines):
	if predictions[i] == answers[i]:
		correct_lines += 1

accuracy = correct_lines / total_lines * 100.0
print accuracy
