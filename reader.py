import csv
from collections import Counter
from decimal import Decimal

user_comment = dict()
users = []

with open ('database.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter = ',')
    i = 0
    for row in readcsv:
        blog_post = row[1]
        user_comment.setdefault(row[2], []).append(" " + row[3].lower())    #ensuring every comment begins with a space to maintain ease in reader_measure & neglect differentiation on the basis of cases of word
        users.append(row[2])
        
users = list(dict.fromkeys(users))
users.pop(0)
for user in users:
    user_comment[user] = list(dict.fromkeys(user_comment[user]))
    user_comment[user].pop(0)

def get_weights():
    """
    Search for presence of other reader in a reader's comment and return a genrated metric pointing to the relation
    """
    reader_graph = dict()

    for i in range(len(users)):
        sentences = user_comment[users[i]]
        
        for j in range(len(users)):
            if i != j:
                res = [k for k in sentences if ('@'+users[j]+' ' in k) or ('@'+users[j]+',' in k) or ('@'+users[j]+'-' in k)]
                if len(res) != 0:
                    reader_graph.setdefault(users[i], []).append(users[j])

    weights = [[0 for x in range(len(users))] for y in range(len(users))]   #2D matrix containing weights of reader b pointing to reader a 

    for i in range(len(users)):
        for j in range(len(users)):
            if i != j:

                pointed = reader_graph.get(users[i])

                if (pointed is not None) and (users[j] in pointed):
                    n = Counter(pointed)
                    weights[i][j] = Decimal(n[users[j]]/len(pointed))
                    weights[i][j] = round(weights[i][j], 4)

    return weights

def reader_authority(reader):
    """
    Implementing PageRank algorithm to get the reader authority value for a given reader who commented on the blog post.
    """
    mod_r = len(users)
    sum = 0
    num = users.index(reader)
    weights = get_weights()

    #setting initial probability distribution
    d = 0.31    #Bayesian value of damping factor
    PR = [round(Decimal(1/mod_r), 4)] * mod_r
    for i in range(len(users)):
        if i != num:
            sum = sum + weights[num][i] * PR[i]

    A = Decimal(d) * Decimal((1/mod_r)) + Decimal(1-d) * Decimal(sum)
    return round(A, 10)

def count_occurances(comment, word):
    """
    A helper function to get number of words in a comment.
    """
    a = comment.split(" ")
    count = 0
    for i in range(len(a)):
        if (word == a[i]):
            count = count + 1
    return count

def reader_measure(word):
    """
    This method takes in a word and returns the expected value of reader measures for the word from all the readers commenting on the blog post.
    """
    word = word.lower()
    RM = 0
    for reader in users:
        res = [k for k in user_comment[reader] if (' ' + word + ' ') in k]
        word_count = 0
        for i in range(len(res)):
            word_count = word_count + count_occurances(res[i], word)
        RM = RM + reader_authority(reader) * word_count
    
    return (RM/len(users))
