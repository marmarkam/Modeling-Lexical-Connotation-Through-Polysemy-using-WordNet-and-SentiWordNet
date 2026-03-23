from evaluation_utils import *
from aggregate_utils import word_aggregate_polarity
import csv
from scipy.stats import spearmanr

#load lexicon proxy
lexicon = load_lexicon("connotation_lexicon_a.0.1.csv")

#num of cross_pol pairs
cross_total = 0
#num of cross_pol pairs that match expectation
cross_correct = 0

#num of words with signs
sign_total = 0
#num of correct signs
sign_correct = 0

#spearman ranking
model_scores = []
gold_scores = []
seen_words = set()


#main eval
with open("pairs.csv") as f,\
    open("eval_results_60pairs.csv", "w", newline="") as output:
    
    reader = csv.DictReader(f)
    writer = csv.writer(output)

    #headers
    writer.writerow([
        "w1","w2","score1","score2","dir_alg",
        "label1", "label2", "category", "gap"
    ])


    for row in reader:
        w1 = row["word1"].strip()
        w2 = row["word2"].strip()
        pos = row["pos"].strip().lower()

        #sanity check to avoid silent crashes
        #already got some :(
        valid_pos = {"n", "v", "a", "r", "s"}
        if pos not in valid_pos:
            print("Invalid POS detected: ", repr(pos))
            continue

        score1 = word_aggregate_polarity(w1, pos)
        score2 = word_aggregate_polarity(w2, pos)

        if score1 is None or score2 is None:
            continue

        #algorithm outputs
        sign1 = sign_of(score1)
        sign2 = sign_of(score2)

        alg_dir = compare_direction(score1, score2)

        #lexicon labels
        LEX_POS_MAP = {
            "a": "adjective",
            "n": "noun",
            "v": "verb",
            "r": "adverb"
        }
        lex_key1 = f"{w1}_{LEX_POS_MAP[pos]}"
        lex_key2 = f"{w2}_{LEX_POS_MAP[pos]}"
        label1 = lexicon.get(lex_key1)
        label2 = lexicon.get(lex_key2)

        category = pair_category(label1, label2)

        #word level validation
        if label1:
            sign_total += 1
            if sign1 == label1:
                sign_correct += 1

        if label2:
            sign_total += 1
            if sign2 == label2:
                sign_correct += 1

        #spearman ranking with labels
        LABEL_MAP = {"negative": -1,
                     "neutral": 0,
                     "positive":1}
        
        if(w1, pos) not in seen_words and label1 in LABEL_MAP:
            model_scores.append(score1)
            gold_scores.append(LABEL_MAP[label1])
            seen_words.add((w1,pos))
        if(w2, pos) not in seen_words and label2 in LABEL_MAP:
            model_scores.append(score2)
            gold_scores.append(LABEL_MAP[label2])
            seen_words.add((w2,pos))

        #pairwise direction validation
        if category == "cross_polarity":
            expected_dir = dir_from_labels(label1, label2)

            cross_total += 1
            if alg_dir == expected_dir:
                cross_correct += 1

        #logging results
        gap = confidence_gap(score1, score2)
        
        writer.writerow([
            w1, w2, score1, score2,
            alg_dir,
            label1, label2,
            category,
            gap
        ])

rho, p_value = spearmanr(model_scores, gold_scores)

print("word-level accuracy:", sign_correct/sign_total if sign_total else 0)
print("cross-pair accuracy:", cross_correct/cross_total if cross_total else 0)
print("spearman correlation:", rho)
print("p-value: ", p_value)