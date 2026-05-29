import re
from collections import Counter
from matplotlib import pyplot as plt
import argparse


# List of words that do not need to be count
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
    'you', 'your', 'yours', 'he', 'him', 'his', 'she',
    'her', 'it', 'its', 'they', 'them', 'what', 'which',
    'who', 'this', 'that', 'am', 'is', 'are', 'was',
    'were', 'be', 'have', 'has', 'had', 'do', 'does',
    'did', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
    'because', 'as', 'until', 'while', 'of', 'at', 'by',
    'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'any', 'both', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 'can', 'will', 'just', 'should', 'now'
}

# List of abreviations
ABREVIATIONS = {
    "Mr","Mrs","Dr"
}


# Helper functions
def tokenize_words(text):
    return re.findall(r"(?:[A-Z]\.)+|\d+\.\d+|\w+(?:'\w+)?|[^\w\s]", text)

def words_and_freqs(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = tokenize_words(raw)
    filtered = [w for w in tokens if w not in STOPWORDS]
    counts = Counter(filtered)

    return counts, len(filtered)

def tokenize_sentences(text):
    normalized = text.replace("\n", " ")
    raw = re.findall(r".+?[.?!](?=[\'\"]*\s[\'\"]*[A-Z]|[\'\"]*$)", normalized)

    return raw

def merge_abbreviations(text):
    merged_text = []
    i = 0
    while i < len(text):
        last_word = text[i].strip('.?!\"\'').split()[-1]
        last_word = last_word.strip('\"\'\"\'')
        if (last_word in ABREVIATIONS):
            if (i+1 < len(text)):
                merged_text.append(text[i] + text[i+1])
                i += 2
            else:
                merged_text.append(text[i])
                i += 1
        else:
            merged_text.append(text[i])
            i += 1

    cleaned_merged_text = []
    j = 0
    while j < len(merged_text):
        cleaned_merged_text.append(merged_text[j].strip(' \"\'\"\''))
        j += 1

    return cleaned_merged_text

def sentences_and_freqs(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = merge_abbreviations(tokenize_sentences(raw))
    counts = Counter(tokens)

    return counts, len(tokens)


# Function for tokenizing words
def tokenized_words(filepath, top_n=50):
    counter, total = words_and_freqs(filepath)
    words, freqs = zip(*counter.most_common(top_n))

    plt.figure(figsize=(10, 5))
    plt.title(f"Top {top_n} Words in {filepath}")
    plt.bar(words, freqs, color="steelblue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# Function for tokenizing sentences
def tokenized_sentences(filepath, top_n=20):
    counter, total = sentences_and_freqs(filepath)
    sentences, freqs = zip(*counter.most_common(top_n))

    # Results printed in the console
    print(f"\nTop {top_n} Most Frequent Sentences")
    print("=" * 100)

    for rank, (sentence, freq) in enumerate(counter.most_common(top_n), start=1):
        shortened = sentence[:80] + "..." if len(sentence) > 80 else sentence
        print(f"{rank:>2}. {freq:>3}x | {shortened}")

    print("=" * 100)
    print(f"Total sentences: {total}")

    # Results displayed in a chart
    shortened = [
        s[:50] + "..." if len(s) > 50 else s
        for s in sentences
    ]

    plt.figure(figsize=(12, 6))
    plt.barh(shortened, freqs)
    plt.gca().invert_yaxis()
    plt.xlabel("Frequency")
    plt.title(f"Top {top_n} Sentences")
    plt.tight_layout()
    plt.show()


# Command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze word frequencies in text files")
    parser.add_argument("filepath", help="Path to the text file to analyze")
    parser.add_argument("--number", "-n", type=int, default=10, help="Number of words/sentences to tokenize (default: 10)")
    parser.add_argument("--function", "-f", choices=["words", "sentences"], default="words", help="Analysis function to run")
    
    args = parser.parse_args()
    
    if args.function == "words":
        tokenized_words(args.filepath, top_n=args.number)
    elif args.function == "sentences":
        tokenized_sentences(args.filepath, top_n=args.number)