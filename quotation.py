import csv
from decimal import Decimal
from collections import Counter

quotation_graph = dict()
comments = []

with open('database.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter = ',')
    for row in readcsv:
        comments.append(row[3].lower().strip())
comments.pop(0)

#build the quoation graph Cj -> Ci
for j in range(len(comments)):
    comment_j = comments[j]
    for i in range(len(comments)):
        if j != i:
            comment_i = comments[i]
            if (str(comment_j).find(str(comment_i))) != -1:
                quotation_graph.setdefault(comment_j, []).append(comment_i)

def get_weights():
    """
    Search for presence of other comment quoted in a reader's comment and return a genrated metric pointing to the relation
    """
    weights = [[0 for x in range(len(comments))] for y in range(len(comments))]

    for i in range(len(comments)):
        for j in range(len(comments)):
            if i != j:

                pointed = quotation_graph.get(comments[i])

                if (pointed is not None) and (comments[j] in pointed):
                    n = Counter(pointed)
                    weights[i][j] = Decimal(n[comments[j]]/len(pointed))
                    weights[i][j] = round(weights[i][j], 4)

    return weights



def quotation_degree(comment):
    """
    Implementing PageRank algorithm to get the quotation degree for a given comment mentioned in some other comment on the blog post.
    """
    comment = comment.lower().strip()
    mod_r = len(comments)
    sum = 0
    num = comments.index(comment)
    weights = get_weights()

    #setting initial probability distribution function
    #No damping exists in the paper for quotaion_degree
    PR = [round(Decimal(1/mod_r), 4)] * mod_r
    for i in range(len(comments)):
        if i != num:
            sum = sum + weights[num][i] * PR[i]

    D = Decimal((1/mod_r)) + Decimal(sum)
    return round(D, 10)


def count_occurances(comment, word):
    """
    A helper function to count the number of words in a comment.
    """
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

def quotation_measure(word):
    """
    This method takes in a word and returns the expected value of quotation measures for the word from all the comments written on the blog post.
    """
    word = word.lower()
    QM = Decimal(0)
    
    for sentence in comments:
        D_ci = quotation_degree(sentence)
        count = count_occurances(sentence, word)
        QM = QM + D_ci * count

    return (QM/len(comments))
    
