import sys, math, string

train_set = []
token_set = set()
dialect_prior = {}
dialect_prob = {}

print "Learning model..."

with open(sys.argv[1], "r") as text_file:
    for line in text_file:
        (dialogue, dialect) = line.strip().split(" | ")
        dialogue = dialogue.lower().translate(None, string.punctuation)
        train_set.append((dialogue, dialect))

for i, (dialogue, dialect) in enumerate(train_set):
    if dialect in dialect_prior:
        dialect_prior[dialect] += 1
    else:
        dialect_prior[dialect] = 1
    token_set.update(dialogue.split())

for dialect in dialect_prior.keys():
    dialect_prior[dialect] = math.log(dialect_prior[dialect] / float(len(train_set)))

for (dialogue, dialect) in train_set:
    tokens_present = dialogue.split()
    if dialect not in dialect_prob:
        dialect_prob[dialect] = {}
        for token in token_set:
            dialect_prob[dialect][token] = 1
    for token in tokens_present:
        dialect_prob[dialect][token] += 1

for dialect in dialect_prob.keys():
    dialect_total = sum(dialect_prob[dialect].values())
    for key in dialect_prob[dialect]:
        dialect_prob[dialect][key] = math.log(dialect_prob[dialect][key] / float(dialect_total))

with open("Code/dialectmodel.txt", "w") as model_file:
    model_file.write(str(dialect_prior) + "\n")
    model_file.write(str(dialect_prob) + "\n")

print "Learned model."
