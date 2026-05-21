from collections import Counter
from matplotlib import pyplot
import argparse


# List of words that do not need to be count
STOPWORDS = {
    "the","a","an","and","or","but","in","on",
    "at","to","of","for","is","was","it","that",
    "this","with","he","she","i","you","we","they"
}


# Helper functions
def tokenize(text):
    return text.split()

def wordsAndFreqs(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = tokenize(raw)
    filtered = [w for w in tokens if w not in STOPWORDS]
    counts = Counter(filtered)

    return counts, len(filtered)


# Function for analyzing monograms
def analyzeWords(filepath, top_n=50):
    counter, total = wordsAndFreqs(filepath)
    words, freqs = zip(*counter.most_common(top_n))

    plt = pyplot
    plt.figure(figsize=(10, 5))
    plt.title("Top 20 Words in " + filepath)
    plt.bar(words, freqs, color="steelblue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# Command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze word frequencies in text files")
    parser.add_argument("filepath", help="Path to the text file to analyze")
    parser.add_argument("--function", choices=["words"], default="words", help="Analysis function to run")
    
    args = parser.parse_args()
    
    if args.function == "words":
        analyzeWords(args.filepath)