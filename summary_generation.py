#using SBS(Summation-Based Selection)

from representative_score import rep_score_sentence
import config
import os
import nltk.data
import time
from decimal import Decimal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
	'-f',
	'--factor',
	default = 1,
	help = 'factor of threshold for summary'
	)
args = parser.parse_args()


start_time = time.time()
#fetching scraped txt blogs
blogs = []
for file in os.listdir():
    if file.endswith(".txt"):
        blogs.append(str(file))

sentence_sbs = dict()

overall_sbs = 0
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
for blog in blogs:
    file = open(blog)
    summary = open(blog[:-4] + '_summary.txt', 'w+')
    data = file.read()
    sentences = tokenizer.tokenize(data)
    #successfully split blog into smart sentences

    file = open("sbs_score.txt", "w+")
    for sentence in sentences:
        print("Old sentence : " + sentence)
        sbs_score = rep_score_sentence(sentence, config.tau)
        file.write(str(sbs_score) + '\n')
        overall_sbs = overall_sbs + sbs_score
        sentence_sbs[sentence] = sbs_score
        
    threshold = overall_sbs/len(sentences)
    
    for key in sentence_sbs:
    	if sentence_sbs[key] >= Decimal(args.factor) * threshold:
    		summary.write(key)

    summary.close()
    file.close()

end_time = time.time()
print("Execution time : " + str(end_time - start_time))
