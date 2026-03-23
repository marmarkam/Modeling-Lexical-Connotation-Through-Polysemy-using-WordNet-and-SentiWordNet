'''
Docstring for evaluation_utils

Three categories for evalution:
    Cat A: cross polarity pairs (pov vs neg) | (neutral vs pov|neg)
        Eval: direction must match
    Cat B: same polarity pairs (pov vs pov) | (neg vs neg) | (neutral vs neutral)
        Eval: direction is unvalidated, sign validated
    Cat C: missing labels
        Eval: skip or mark NA
'''
import csv

#load connotation lexicon
def load_lexicon(path):
    lex = {}
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            word = row[0].strip()
            label = row[1].strip()
            lex[word] = label
    return lex

SIGN_EPS = .02

#get polarity score sign
def sign_of(score):
    if score > SIGN_EPS:
        return "positive"
    if score < SIGN_EPS:
        return "negative"
    else:
        return "neutral"

DIR_EPS = .02

#Compare direction of algorithm output
def compare_direction(score1, score2):
    diff = score1 - score2

    if diff > DIR_EPS:
        return "word1_more_positive"
    if diff < -DIR_EPS:
        return "word2_more_positive"
    return "equal"

#get direction from lexicon labels
RANK = {
    "positive":1,
    "neutral": 0,
    "negative": -1
}
def dir_from_labels(label1, label2):
   if label1 not in RANK or label2 not in RANK:
       return "unknown"
   if RANK[label1] > RANK[label2]:
       return "word1_more_positive"
   if RANK[label2] > RANK[label1]:
       return "word2_more_positive"
   return "equal"

#confidence gap analysis: how strongly the algorithm prefers one word over another
def confidence_gap(score1, score2):
    return abs(score1 - score2)

#determine pair category
def pair_category(label1, label2):
    if label1 is None or label2 is None:
        return "unknown"
    if label1 != label2:
        return "cross_polarity"
    return "same_polarity"

    