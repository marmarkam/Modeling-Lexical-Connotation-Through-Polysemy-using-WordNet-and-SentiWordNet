from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn

word = input("Enter a word: ")
synsets = wn.synsets(word)

with open("sentiwordnet_synsets_outputs.txt", "w") as f:
    for syn in synsets:
        senti_syn = swn.senti_synset(syn.name()) #convert synset into sentisynset
        
        f.write("Synset: " + syn.name() + "\n")
        f.write("Definition: " + syn.definition() + "\n")

        f.write("Postive Score: " + str(senti_syn.pos_score()) + "\n")
        f.write("Negative Score: " + str(senti_syn.neg_score()) + "\n")
        f.write("Objective Score: " + str(senti_syn.obj_score()) + "\n")



        examples = syn.examples()
        if examples:
            f.write("Example: " + examples[0] + "\n")

        f.write("\n")