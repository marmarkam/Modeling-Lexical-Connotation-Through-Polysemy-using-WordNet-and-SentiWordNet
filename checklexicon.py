from evaluation_utils import load_lexicon
import csv

lexicon = load_lexicon("connotation_lexicon_a.0.1.csv")
print(len(lexicon))
print(list(lexicon.items()))[:5]
