from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

#
def differential_aggregation(word1, word2, part_of_speech):
    #get synsets for each word
    synsets1 = wn.synsets(word1, pos=part_of_speech)
    synsets2 = wn.synsets(word2, pos=part_of_speech)

    #sort out the shared and unique synsets per word
    set1 = {s.name() for s in synsets1}
    set2 = {s.name() for s in synsets2}
    # shared = set1 & set2
    unique1 = set1 - set2
    unique2 = set2 - set1

    #get sentiscores for each unique set
    neg_sum_1 = 0
    neg_sum_2 = 0
    if unique1:
        for syn in unique1:
            scores = swn.senti_synset(syn) 
            neg_sum_1 += scores.neg_score()

        neg1 = neg_sum_1/len(unique1)
    else:
        neg1 = 0
    print(word1 + " average neg_score: " + str(neg1) + "\n")

    if unique2:
        for syn in unique2:
            scores = swn.senti_synset(syn)
            neg_sum_2 += scores.neg_score()

        neg2 = neg_sum_2/len(unique2)
    else:
        neg2 = 0
    print(word2 + " average neg_score: " + str(neg2) + "\n")

    #get aggregate
    delta_neg = neg1 - neg2

    return delta_neg

def main():
    word1 = input("Enter synonym 1: ")
    word2 = input("Enter a synonym 2: ")
    pos_input= input("What is the part of speech (n, v, a, r)? ").lower()

    pos_map = {'n':wn.NOUN, 'v':wn.VERB, 'a':wn.ADJ, 'r':wn.ADV}
    part_of_speech = pos_map.get(pos_input)

    aggregate = differential_aggregation(word1, word2, part_of_speech)
    print("Aggregate: " + str(aggregate))

    if aggregate > 0:
        print(word1 + " is more negatively connotated than " + word2)
    elif aggregate < 0:
        print(word2 + " is more negatively connotated than " + word1)
    else:
        print(word1 + " and " + word2 + " have equal negative connotation")

if __name__ == "__main__":
    main()
