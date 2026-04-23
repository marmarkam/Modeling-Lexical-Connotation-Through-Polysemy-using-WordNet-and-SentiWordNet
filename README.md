# Modeling Lexical Connotation Through Polysemy using WordNet and SentiWordNet

## Overview

This senior research project explores whether lexical resources such as WordNet and SentiWordNet can be used to model and distinguish connotative differences between near-synonyms. The system aggregates sentiment across word senses (synsets) and compares words using both uniform and weighted aggregation strategies.

The goal is to evaluate whether sense-level sentiment representations can approximate human judgments of connotation.


## Methodology

The pipeline consists of the following steps:

1. Word Sense Retrieval  
   Words are mapped to their corresponding WordNet synsets using part-of-speech filtering.

2. Sentiment Extraction  
   Each synset is mapped to a SentiWordNet sentiment score (positive and negative polarity).

3. Aggregation Strategies  
   Two aggregation methods are used:
   - Uniform averaging across synsets (primary method)
   - Rank-weighted averaging (biasing earlier synsets as more frequent senses) (experimental)

4. Synset Decomposition  
   Synsets are partitioned into:
   - Shared senses (common between synonyms)
   - Unique senses (word-specific meanings)

5. Evaluation  
   Word pairs are compared using:
   - Differential polarity scores  
   - Human evaluation dataset  
   - Lexicon-proxy comparison


## Files

### Core Pipeline
- `aggregate_utils.py` – Synset aggregation and polarity computation  
- `io_utils.py` – Input/output handling for word pairs and results  
- `eval_utils.py` – Evaluation metrics and scoring functions  
- `main.py` – Runs full aggregation pipeline  

### Evaluation
- `eval_driver.py` – Automated evaluation against datasets  
- `human_eval.py` – Human judgment comparison pipeline  


## Key Idea

Instead of treating words as single semantic units, this project models words as distributions over senses. Each sense contributes a sentiment signal, and final polarity is computed as an aggregation over these signals.


## Key Findings

- SentiWordNet provides partial and uneven sentiment coverage across synsets  
- Many synsets contribute weak or neutral polarity signals  
- Weighted and uniform aggregation produce similar results due to low variance in effective signal  
- Lexical models align more closely with lexicon-proxy evaluation than human judgment


## Limitations

- Sparse sentiment annotations across WordNet synsets  
- Weak differentiation between near-synonyms in SentiWordNet  
- Limited contextual awareness (no sentence-level semantics)  
- Human connotation is influenced by context not captured in static lexical resources


## Requirements

- Python 3.9+
- NLTK
- SentiWordNet corpus
- WordNet corpus
