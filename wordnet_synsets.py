from nltk.corpus import wordnet as wn

word = input("Enter a word: ")
synsets = wn.synsets(word)

#write to output file all synsets for inputted word
with open("wordnet_synsets_outputs.txt", "w") as f:
    for s in synsets:
        f.write("Inputted word: " + word + "\n")
        f.write("Synset: " + s.name() + "\n")
        f.write("Definition: " + s.definition() + "\n")

        examples = s.examples()
        if examples:
            f.write("Example: " + examples[0] + "\n")
        
        lemmas = s.lemmas()
        lemma_names = []
        for lemma in lemmas:
            lemma_names.append(lemma.name())

        f.write("Synonyms (lemmas): " + ", ".join(lemma_names) + "\n")
        
        f.write("\n")