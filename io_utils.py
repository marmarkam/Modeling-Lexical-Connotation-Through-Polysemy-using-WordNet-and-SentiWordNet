from nltk.corpus import wordnet as wn
import csv

#get pairs from txt file
def get_pairs(filename):
    POS_MAP = {
    "n": wn.NOUN,
    "v": wn.VERB,
    "a": wn.ADJ,
    "r": wn.ADV
    }
    pairs = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) != 3:
                continue

            w1 = parts[0].strip()
            w2 = parts[1].strip()
            pos_tag = parts[2].strip().lower()

            if pos_tag in POS_MAP:
                pairs.append((w1, w2, POS_MAP[pos_tag]))
    return pairs

#write results to csv
def results_to_csv(results, filename):
    headers = results[0].keys()

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in results:
            writer.writerow(row)