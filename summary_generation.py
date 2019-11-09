#using SBS(Summation-Based Selection)

from representative_score import rep_score_sentence
import config
import os
import nltk.data
import time

start_time = time.time()
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

    file = open("sbs_score.txt", "w+")
    for sentence in sentences:
        print("Old sentence : " + sentence)
        sbs_score = rep_score_sentence(sentence, config.tau)
        file.write(str(sbs_score) + '\n')
        if sbs_score > config.selection_threshold:
            summary.write(sentence)

    summary.close()
    file.close()

end_time = time.time()
print("Execution time : " + str(end_time - start_time))
