import sys

predictions = []
answers = []

correct_lines = 0

print("Calculating Accuracy...")

with open(sys.argv[1], "r") as prediction_file:
    for line in prediction_file:
        (_, dialect) = line.strip().split(" | ")
        predictions.append(dialect)
#    	predictions.append(line.strip().split(" | "))

with open(sys.argv[2], "r") as answer_file:
    for line in answer_file:
        (_, dialect) = line.strip().split(" | ")
        answers.append(dialect)
#		answers.append(line.strip().split(" | "))

total_lines = len(predictions)



# HUM
# STD
# BOM
# DEL
# EUP
# WUP



std_true_positive = 0
std_false_positive = 0
std_false_negative = 0



hum_true_positive =0
hum_false_positive = 0

hum_false_negative = 0

bom_true_positive =0
bom_false_positive = 0
bom_false_negative = 0

wup_true_positive =0
wup_false_positive = 0
wup_false_negative = 0


eup_true_positive =0
eup_false_positive = 0
eup_false_negative = 0

del_true_positive = 0
del_false_positive = 0
del_false_negative = 0






for i in range(total_lines):
    if(predictions[i][1] == "STD" and answers[i][1]=="STD"):
        std_true_positive +=1
    else:
        if(predictions[i][1] == "STD" and answers[i][1] != "STD"):
            std_false_positive +=1
        else:
            if(predictions[i][1] != "STD" and answers[i][1] == "STD"):
                std_false_negative += 1


std_precision = std_true_positive / float(std_false_positive + std_true_positive)
std_recall = std_true_positive/float(std_true_positive + std_false_negative)

print(std_precision)
print(std_recall)


for i in range(total_lines):
    if(predictions[i][1] == "HUM" and answers[i][1]=="HUM"):
        hum_true_positive +=1
    else:
        if(predictions[i][1] == "HUM" and answers[i][1] != "HUM"):
            hum_false_positive +=1
        else:
            if(predictions[i][1] != "HUM" and answers[i][1] == "HUM"):
                hum_false_negative = 0

hum_precision = hum_true_positive / float(hum_false_positive + hum_true_positive)
hum_recall = hum_true_positive/float(hum_true_positive + hum_false_negative)


print(hum_precision)
print(hum_recall)


for i in range(total_lines):
    if(predictions[i][1] == "BOM" and answers[i][1]=="BOM"):
        bom_true_positive +=1
    else:
        if(predictions[i][1] == "BOM" and answers[i][1] != "BOM"):
            bom_false_positive +=1
        else:
            if(predictions[i][1] != "BOM" and answers[i][1] == "BOM"):
                bom_false_negative = 0

bom_precision = bom_true_positive / float(bom_false_positive + bom_true_positive)
bom_recall = bom_true_positive/float(bom_true_positive + bom_false_negative)


print(bom_precision)
print(bom_recall)


for i in range(total_lines):
    if(predictions[i][1] == "WUP" and answers[i][1]=="WUP"):
        wup_true_positive +=1
    else:
        if(predictions[i][1] == "WUP" and answers[i][1] != "WUP"):
            wup_false_positive +=1
        else:
            if(predictions[i][1] != "WUP" and answers[i][1] == "WUP"):
                wup_false_negative = 0

wup_precision = wup_true_positive / float(wup_false_positive + wup_true_positive)
wup_recall = wup_true_positive/float(wup_true_positive + wup_false_negative)


print(wup_precision)
print(wup_recall)

for i in range(total_lines):
    if(predictions[i][1] == "EUP" and answers[i][1]=="EUP"):
        eup_true_positive +=1
    else:
        if(predictions[i][1] == "EUP" and answers[i][1] != "EUP"):
            eup_false_positive +=1
        else:
            if(predictions[i][1] != "EUP" and answers[i][1] == "EUP"):
                eup_false_negative = 0

eup_precision = eup_true_positive / float(eup_false_positive + eup_false_positive)

eup_recall = eup_true_positive/float(eup_true_positive + eup_false_negative)


print(eup_precision)
print(eup_recall)


for i in range(total_lines):
    if(predictions[i][1] == "DEL" and answers[i][1]=="DEL"):
        del_true_positive +=1
    else:
        if(predictions[i][1] == "DEL" and answers[i][1] != "DEL"):
            del_false_positive +=1
        else:
            if(predictions[i][1] != "DEL" and answers[i][1] == "DEL"):
                del_false_negative = 0

del_precision = del_true_positive / float(del_false_positive + del_true_positive)

del_recall = del_true_positive/float(del_true_positive + del_false_negative)


print(del_precision)
print(del_recall)




# for i in range(total_lines):
#     if predictions[i][1] == answers[i][1]:
#         correct_lines += 1
# #	else:
# #		print "prediction: " + predictions[i][1] + " actual: " + answers[i][1] + " for " + predictions[i][0]
#
# accuracy = float(correct_lines) / float(total_lines) * 100.0
# print("Accuracy = " + str(accuracy))