from topic import topic_cluster

#creating a list of lists, with each sub list containing a cluster sequence with key thread added
cluster = []
for thread in topic_cluster.keys():
    temp_list = []
    temp_list.append(thread)
    for text in topic_cluster[thread]:
        temp_list.append(text)
    cluster.append(temp_list)

#removing exact same sub clusters in the list of clusters
for pos1 in range(len(cluster)):
    for pos2 in range(pos1+1, len(cluster)):
        list1 = cluster[pos1]
        list2 = cluster[pos2]
        list1.sort()
        list2.sort()
        if list1 == list2:
            cluster.pop(pos1)
            pos1 = pos1 - 1

#the cluster of differnt discussions is ready here

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx






