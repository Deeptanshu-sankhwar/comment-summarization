#constructing reader graph
import csv
from collections import Counter
from decimal import Decimal

user_comment = dict()
users = []

with open ('database.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter = ',')
    for row in readcsv:
        blog_post = row[1]
        user_comment.setdefault(row[2], []).append(row[3])
        users.append(row[2])   

users = list(dict.fromkeys(users))
users.pop(0)

for user in users:
    user_comment[user] = list(dict.fromkeys(user_comment[user]))


def get_weights():
    
    #search for presence of other reader in a reader's comment
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
    mod_r = len(users)
    sum = 0
    num = users.index(reader)
    weights = get_weights()
    for i in range(len(users)):
        if i != num:
            sum = sum + weights[num][i]

    A = Decimal((1/mod_r)) + Decimal(sum)
    return A

# print(reader_authority('Kyle Pflug [MSFT]'))