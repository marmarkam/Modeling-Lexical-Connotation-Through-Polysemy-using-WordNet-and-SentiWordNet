from aggregate_utils import compare_connotation
from io_utils import get_pairs, results_to_csv

def main():
    input_file = "1st_20_pairs.txt"
    output_file = "1st_20_weighted_results.csv"

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