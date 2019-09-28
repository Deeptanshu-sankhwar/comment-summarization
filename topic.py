#Topic clustering
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from decimal import Decimal

topic_cluster = dict()
comments = []

with open('database.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter = ',')
    i = 0
    for row in readcsv:
        comments.append(row[3].lower().strip())
comments.pop(0)

word_count = 0 #sum of total number of words in all comments

#to get cosine similarity between two comments
def cosine_similarity(thread, text):
    #tokenize comment into words
    thread_list = word_tokenize(thread)
    text_list = word_tokenize(text)

    #getting stopwords in english
    stop_words = stopwords.words('english')
    l1 = []
    l2 = []

    #remove stopwords from tokenized list of words
    thread_set = {w for w in thread_list if not w in stop_words}
    text_set = {w for w in text_list if not w in stop_words}

    union_vector = thread_set.union(text_set)
    for word in union_vector:
        if word in thread_set:
            l1.append(1)
        else:
            l1.append(0)
        if word in text_set:
            l2.append(1)
        else:
            l2.append(0)

    c = 0

    for i in range(len(union_vector)):
        c += l1[i]*l2[i]

    cosine = c / float((sum(l1)*sum(l2))**0.5)

    return cosine, len(thread_list)

#Single-Pass Incremental Clustering
for i in range(len(comments)):
    thread = comments[i]
    count = 0
    for j in range(len(comments)):
        if j != i:
            text = comments[j]
            similarity, count = cosine_similarity(thread, text)
            if similarity >= 0.5:   #similarity metric can be altered
                topic_cluster.setdefault(thread, []).append(text)
    word_count += count

#returns importance metric of a built thread in a topic clutser
def topic_importance(thread):
    metric = 0
    thread = thread.lower().strip()
    for comment in topic_cluster[thread]:
        sim, cmt_word_count = cosine_similarity(comment, thread)
        metric += sim * cmt_word_count
    
    T = Decimal(1/word_count) * Decimal(metric)

    return round(T, 10)

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

#return topic measure of a word
def topic_measure(word, thread):
    T_tu = topic_importance(thread)
    count = 0
    for comment in topic_cluster[thread]:
        count += count_occurances(comment, word)
    print(count)
    TM = T_tu * count

    return TM 
