from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

#word-level wrapper 
def word_aggregate_polarity(word, pos):
    synsets = wn.synsets(word, pos=pos)
    if not synsets:
        return None
    return synset_aggregate_polarity(synsets)

#Helper function: helps to ascertain whether words differ in connotation
def synset_aggregate_polarity(synset_list, weighted=False):
    
    if not synset_list:
        return None
    
    #convert to list for indexing so that weighing words correctly
    synset_list = list(synset_list)

    total_polarity = 0
    count = 0

    total_weighted = 0
    total_weight = 0

    for i, synset in enumerate(synset_list):
        try:
            senti =  swn.senti_synset(synset.name())
        except:
            continue

        print("Word synsets: ", len(synset_list), "Used: ", count)

        #calculate polarity
        polarity = senti.pos_score() - senti.neg_score()

        if weighted:
            weight = 1/(i + 1) #rank based weight
            total_weighted += polarity * weight
            total_weight += weight
        else:
            total_polarity += polarity
            count += 1

    if weighted:
        if total_weight == 0:
            return None
        return total_weighted/total_weight #aggregate weighted polarity
    else:
        if count == 0:
            return None
        return total_polarity/count #aggregate uniform polarity
    # #dbug print
    # print("Processed synsets:", count, "out of", len(synset_list))

def safe(x):
    return x if x is not None else ""

#main comparision function with sense decomposition
def compare_connotation(word1, word2, part_of_speech):
    #get synsets for each word
    synset1_list = wn.synsets(word1, pos=part_of_speech)
    synset2_list = wn.synsets(word2, pos=part_of_speech)

    synset1_set = set(synset1_list)
    synset2_set = set(synset2_list)

    #check if valid
    if not synset1_list or not synset2_list:
        return None
    
    #partition synsets into shared and unique senses
    shared = synset1_set & synset2_set
    unique1 = synset1_set - synset2_set #word1's unique senses
    unique2 = synset2_set - synset1_set #word2's unique senses

    #aggregate polarity for each component
    shared_polarity = synset_aggregate_polarity(shared, weighted=False)

    unique1_polarity = synset_aggregate_polarity(unique1, weighted=False)
    unique2_polarity = synset_aggregate_polarity(unique2, weighted=False)

    total1_polarity = synset_aggregate_polarity(synset1_list, weighted=True)
    total2_polarity = synset_aggregate_polarity(synset2_list, weighted=True)

    #debug prints to check which words have synsets
    # print("DEBUG:", word1, word2, part_of_speech)
    # print("Synset counts:", len(synset1), len(synset2))
    # print("Polarity totals:", total1_polarity, total2_polarity)

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