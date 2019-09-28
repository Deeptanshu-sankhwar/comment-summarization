#Quotation Graph
import csv
from decimal import Decimal

quotation_graph = dict()
comments = []

with open('database.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter = ',')
    for row in readcsv:
        comments.append(row[3].lower().strip)
comments.pop(0)

#build the quoation graph Cj -> Ci
for j in range(len(comments)):
    comment_j = comments[j]
    for i in range(len(comments)):
        if j != i:
            comment_i = comments[i]
            if (str(comment_j).find(str(comment_i))) != -1:
                quotation_graph.setdefault(comment_j, []).append(comment_i)

# def quotation_degree()    #to be completed


#to count total occurances of a given word in a comment
def count_occurances(comment, word):
    comment = comment.replace('?', ' ')
    comment = comment.replace('.', ' ')
    comment = comment.replace('-', ' ')
    comment = comment.replace('/', ' ')
    a = comment.split(" ")
    count = 0
    for i in range(len(a)):
        if (word == a[i]):
            count = count + 1
    return count

def quotation_measure(word, sentence):
    D_ci = quotation_degree(sentence)
    count = count_occurances(sentence, word)
    QM = D_ci * count

    return QM
    



