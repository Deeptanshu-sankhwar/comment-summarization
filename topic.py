import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from decimal import Decimal
import config

topic_cluster = dict()
comments = []

with open('database.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter = ',')
    for row in readcsv:
        comments.append(row[3].lower().strip())
comments.pop(0)

word_count = 0 #sum of total number of words in all comments

def cosine_similarity(thread, text):
    """
    Get cosine similarity between two comments.
    """

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

    if (sum(l1)*sum(l2))**0.5 != 0:
        cosine = c / float((sum(l1)*sum(l2))**0.5)
    else:
        return 0, len(thread_list)

    return cosine, len(thread_list)

#Single-Pass Incremental Clustering
for i in range(len(comments)):
    thread = comments[i]
    count = 0
    for j in range(len(comments)):
        if j != i:
            text = comments[j]
            similarity, count = cosine_similarity(thread, text)
            if similarity >= config.topic_similarity:   #similarity metric can be altered
                topic_cluster.setdefault(thread, []).append(text)
    word_count += count

def topic_importance(thread):
    """
    Returns topic importance value of a built thread in a topic clutser.
    """
    metric = 0
    thread = thread.lower().strip()
    for comment in topic_cluster[thread]:
        sim, cmt_word_count = cosine_similarity(comment, thread)
        metric += sim * cmt_word_count
    
    T = Decimal(1/word_count) * Decimal(metric)

    return round(T, 10)

def count_occurances(comment, word):
    """
    A helper function to get the number of words in a comment.
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

def topic_measure(word):
    """
    This method takes in a word and returns the expected value of topic measures for the word from all the topic clusters constructed in the given blog.
    """
    word =  word.lower()
    TM = 0
    for thread in topic_cluster.keys():
        T_tu = topic_importance(thread)
        count = 0
        for comment in topic_cluster[thread]:
            count += count_occurances(comment, word)
        TM = TM + T_tu * count

    return (TM/len(comments)) 
