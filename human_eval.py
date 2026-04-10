import pandas as pd
from scipy.stats import spearmanr


human = pd.read_csv('connotation_scores.csv')
uniform = pd.read_csv('eval_results_60pairs.csv')
weighted = pd.read_csv('eval_weighted_results_60pairs.csv')

for col in ['w1', 'w2']:
    human[col] = human[col].str.strip().str.lower()
    uniform[col] = uniform[col].str.strip().str.lower()
    weighted[col]= weighted[col].str.strip().str.lower()

merged = human.merge(uniform, on=['w1', 'w2'], suffixes=('', '_uniform')) \
    .merge(weighted, on=['w1', 'w2'], suffixes=('', '_weighted'))

#normalize model output to numbers
score_map = {
    'word1_more_positive' : 1,
    'word2_more_positive': 0,
    'equal' : -1
}

merged['uniform_score'] = merged['dir_alg'].str.lower().map(score_map)
merged['weighted_score'] = merged['dir_alg_weighted'].str.lower().map(score_map)

#accuracy
uniform_acc = (merged['human_score'] == merged['uniform_score']).mean()
weighted_acc = (merged['human_score'] == merged['weighted_score']).mean()

#spearman
uniform_corr, uniform_p = spearmanr(merged['human_score'], merged['uniform_score'])
weighted_corr, weighted_p = spearmanr(merged['human_score'], merged['weighted_score'])

merged.to_csv('human_eval_results.csv', index=False)

print("Uniform accuracy: ", uniform_acc)
print("Uniform spearman correlation: ", uniform_corr)
print("Uniform p-val: ", uniform_p)
print("*****")
print("Weighted accuracy: ", weighted_acc)
print("Weighted spearman correlation: ", weighted_corr)
print("Weighted p-val: ", weighted_p)