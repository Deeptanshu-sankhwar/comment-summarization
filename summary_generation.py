#using SBS(Summation-Based Selection)

from representative_score import rep_score_sentence
import config
import os
import nltk.data

#fetching scraped txt blogs
blogs = []
for file in os.listdir():
    if file.endswith(".txt"):
        blogs.append(str(file))

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
for blog in blogs:
    file = open(blog)
    summary = open(blog[:-4] + '_summary.txt', 'w+')
    data = file.read()
    sentences = tokenizer.tokenize(data)
    #successfully split blog into smart sentences

    for sentence in sentences:
        sbs_score = rep_score_sentence(sentence, config.tau)
        if sbs_score > config.selection_threshold:
            summary.write(sentence)

    summary.close()
    file.close()

