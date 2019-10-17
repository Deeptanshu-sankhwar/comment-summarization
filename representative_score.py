#fetch Representative score
from topic.py import topic_measure
from quotation.py import quotation_measure
from reader.py import reader_measure
import argparse

#prone to optimisation changes
alpha = 0.33
beta = 0.33
gamma = 0.33

def score(word):
    Rep = alpha * reader_mesure