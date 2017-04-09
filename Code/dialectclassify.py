import sys, math, ast, random

test_set = []

with open("dialectmodel.txt","r") as model_file:
    dialect_prior = ast.literal_eval(model_file.readline().rstrip())
    dialect_prob = ast.literal_eval(model_file.readline().rstrip())

token_set = dialect_prob[random.choice(dialect_prob.keys())].keys()

with open(sys.argv[1], "r") as test_file:
    for line in test_file:
        test_set.append(line.strip())

for i, dialogue in enumerate(test_set):
    tokens_present = dialogue.split()
    prob_list = {}

    for dialect in dialect_prob.keys():
        prob = 0
        for token in tokens_present:
            if token in token_set:
                prob += dialect_prob[dialect][token]
        prob_list[dialect] = prob

    (predicted_dialect, predicted_prob) = max(prob_list.items(), key = lambda k: k[1])
    test_set[i] = dialogue + " | " + predicted_dialect

with open("dialectresult.txt", "w") as result_file:
    for dialogue in test_set:
        result_file.write(dialogue + "\n")
