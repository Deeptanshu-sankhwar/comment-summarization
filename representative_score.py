#using SBS(Summation-Based Selection)

from reader import reader_measure
from quotation import quotation_measure
from topic import topic_measure
import config
from decimal import Decimal

def rep_score_word(word):
    #normalising score
    # rm = reader_measure(word.lower())
    # qm = quotation_measure(word.lower())
    # tm = topic_measure(word.lower())

    return (reader_measure(word.lower()) * Decimal(config.alpha)) + (quotation_measure(word.lower()) * Decimal(config.beta)) + (topic_measure(word.lower()) * Decimal(config.gamma))

def rep_score_sentence(sentence, tau):
    print(sentence)
    words = sentence.split(' ')
    word_count = len(words)
    rep_sentence = 0
    for word in words:
        print(word)
        rep_sentence = rep_score_word(word) ** tau

    rep_sentence = rep_sentence ** Decimal(1/tau)
    rep_sentence = Decimal(rep_sentence/word_count)

    return rep_sentence

