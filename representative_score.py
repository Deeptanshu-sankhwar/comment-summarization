#using SBS(Summation-Based Selection)

from reader import reader_measure
from quotation import quotation_measure
from topic import topic_measure
import config
from decimal import Decimal
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer

def rep_score_word(word):
    """
    Function, returns the representative score of a word considering the hyper parameters aplha, beta and gamma.
    """
    
    return (reader_measure(word.lower()) * Decimal(config.alpha)) + (quotation_measure(word.lower()) * Decimal(config.beta)) + (topic_measure(word.lower()) * Decimal(config.gamma))

def rep_score_sentence(sentence, tau):
    """
    Function receives a sentence from blog and removes stopwords and punctuations that comprise of noise for the algorithm.
    """
    keywords = word_tokenize(sentence)
    stop_words = stopwords.words('english')
    regx = RegexpTokenizer(r'\w+')
    words_temp = [w for w in keywords if not w in stop_words]
    temp_sentence = ''
    for temp in words_temp:
        temp_sentence += temp + ' '
    words = regx.tokenize(temp_sentence)

    print("New sentence : ")
    print(words)
    word_count = len(words)
    rep_sentence = 0
    for word in words:
        print(word)
        rep_sentence = rep_sentence + rep_score_word(word) ** Decimal(tau)

    rep_sentence = rep_sentence ** Decimal(1/tau)
    rep_sentence = Decimal(rep_sentence/word_count)

    return rep_sentence

