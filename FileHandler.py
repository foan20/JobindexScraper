import re
import json
import pandas as pd
import matplotlib.pyplot as plt

wordlist_file = "wordlist.txt"


def plot_results(results):
    results.plot(y='count', kind='pie')
    plt.show()


def export_to_csv_to_excel(filename):
    with open(filename + ".json", 'r') as f:
        data = json.load(f)
    df = pd.DataFrame({'count': data})

    # Disregard words with count = 0.
    df = df[(df.T != 0).any()]

    plot_results(df)
    # df.to_csv(filename + ".xlsx")


def write_results_to_file(search_text, results):
    filename = "results/results_for_" + search_text
    with open(filename + ".json", "w") as f:
        f.write(json.dumps(results))
    export_to_csv_to_excel(filename)


def read_file_and_parse_lines():
    results = []

    with open(wordlist_file) as wordlist:
        lines = wordlist.readlines()
        for line in lines:
            if not re.search("//", line):
                results.append(line.strip())

        for word in results:
            if word == '':
                results.remove(word)

        return results


def get_word_dict():
    results = {}
    words = read_file_and_parse_lines()

    for word in words:
        results[word] = 0

    return results
