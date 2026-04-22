from aggregate_utils import compare_connotation
from io_utils import get_pairs, results_to_csv

def main():
    input_file = "pairs.txt"
    output_file = "uniform_results_60pairs.csv"

    pairs = get_pairs(input_file)
    # print("Pairs loaded:", pairs) #debug test
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

    avg_used = sum(r["word1_used_synsets"] + r["word2_used_synsets"] for r in all_results) / (2 * len(all_results))
    print("Average contributing synsets per word:", round(avg_used, 2))

if __name__ == "__main__":
    main()