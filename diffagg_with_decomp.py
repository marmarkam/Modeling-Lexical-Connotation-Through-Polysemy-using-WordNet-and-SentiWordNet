from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
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

            parts = line.split(",")
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

#Helper function: helps to ascertain whether words differ in connotation
def synset_aggregrate_polarity(synset_list):
    if not synset_list:
        return None
    
    total_polarity = 0
    count = 0

    for synset in synset_list:
        try:
            senti =  swn.senti_synset(synset.name())
        except:
            continue

        #calculate polarity
        polarity = senti.pos_score() - senti.neg_score()
        
        #accumulate polarity & increment count
        total_polarity += polarity
        count +=1

    if count == 0:
        return None
    
    #dbug print
    print("Processed synsets:", count, "out of", len(synset_list))

    return total_polarity/count #aggregate polarity

def safe(x):
    return x if x is not None else ""

#main comparision function with sense decomposition
def compare_connotation(word1, word2, part_of_speech):
    #get synsets for each word
    synset1 = set(wn.synsets(word1, pos=part_of_speech))
    synset2 = set(wn.synsets(word2, pos=part_of_speech))

    #check if valid
    if not synset1 or not synset2:
        return None
    
    #partition synsets into shared and unique senses
    shared = synset1 & synset2
    unique1 = synset1 - synset2 #word1's unique senses
    unique2 = synset2 - synset1 #word2's unique senses

    #aggregate polarity for each component
    shared_polarity = synset_aggregrate_polarity(shared)

    unique1_polarity = synset_aggregrate_polarity(unique1)
    unique2_polarity = synset_aggregrate_polarity(unique2)

    total1_polarity = synset_aggregrate_polarity(synset1)
    total2_polarity = synset_aggregrate_polarity(synset2)

    #debug prints to check which words have synsets
    print("DEBUG:", word1, word2, part_of_speech)
    print("Synset counts:", len(synset1), len(synset2))
    print("Polarity totals:", total1_polarity, total2_polarity)

    if total1_polarity is None or total2_polarity is None:
        return None

    #delta aggregate
    delta_total = total1_polarity - total2_polarity

    #check if safe for csv output
    shared_polarity  = safe(shared_polarity)
    unique1_polarity = safe(unique1_polarity)
    unique2_polarity = safe(unique2_polarity)
    total1_polarity  = safe(total1_polarity)
    total2_polarity  = safe(total2_polarity)

    return {
        "word1:":word1,
        "word2:":word2,
        "word1_total:":total1_polarity,
        "word2_total:":total2_polarity,
        "delta_total:":delta_total,
        "shared_polarity:" :shared_polarity,
        "word1_unique_polarity: ": unique1_polarity,
        "word2_unique_polarity: ":unique2_polarity,
        "num_shared: ":len(shared),
        "num_unqiue1: ":len(unique1),
        "num_unique2: ":len(unique2)
    }

def main():
    input_file = "pairs.txt"
    output_file = "results.csv"

    pairs = get_pairs(input_file)
    print("Pairs loaded:", pairs) #debug test
    all_results = []

    for w1, w2, pos in pairs:
        result = compare_connotation(w1, w2, pos)
        if result:
            all_results.append(result)

    if all_results:
        results_to_csv(all_results, output_file)
        print("Results written to", output_file)
    else:
        print("No valid results produced")

if __name__ == "__main__":
    main()