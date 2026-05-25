import re
from collections import Counter
from matplotlib import pyplot as plt
import argparse


# List of words that do not need to be count
STOPWORDS = {
    "the","a","an","and","or","but","in","on",
    "at","to","of","for","is","was","it","that",
    "this","with","he","she","i","you","we","they"
}

# List of abreviations
ABREVIATIONS = {
    "Mr","Mrs","Dr"
}


# Helper functions
def wordTokenizer(text):
    return re.findall(r"(?:[A-Z]\.)+|\d+\.\d+|\w+(?:'\w+)?|[^\w\s]", text)

def wordsAndFreqs(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = wordTokenizer(raw)
    filtered = [w for w in tokens if w not in STOPWORDS]
    counts = Counter(filtered)

    return counts, len(filtered)

def sentenceTokenizer(text):
    normalized = text.replace("\n", " ")
    raw = re.findall(r".+?[.?!](?=[\'\"]*\s[\'\"]*[A-Z]|[\'\"]*$)", normalized)

    return raw

def mergeAbbreviations(text):
    mergedText = []
    i = 0
    while i < len(text):
        lastWord = text[i].strip('.?!\"\'').split()[-1]
        lastWord = lastWord.strip('\"\'\"\'')
        if (lastWord in ABREVIATIONS):
            if (i+1 < len(text)):
                mergedText.append(text[i] + text[i+1])
                i += 2
            else:
                mergedText.append(text[i])
                i += 1
        else:
            mergedText.append(text[i])
            i += 1

    cleanedMergedText = []
    j = 0
    while j < len(mergedText):
        cleanedMergedText.append(mergedText[j].strip(' \"\'\"\''))
        j += 1

    return cleanedMergedText

def sentecesAndFreqs(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = mergeAbbreviations(sentenceTokenizer(raw))
    counts = Counter(tokens)

    return counts, len(tokens)


# Function for tokenizing words
def tokenizedWords(filepath, top_n=50):
    counter, total = wordsAndFreqs(filepath)
    words, freqs = zip(*counter.most_common(top_n))

    plt.figure(figsize=(10, 5))
    plt.title(f"Top {top_n} Words in {filepath}")
    plt.bar(words, freqs, color="steelblue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# Function for tokenizing sentences
def tokenizedSentences(filepath, top_n=20):
    counter, total = sentecesAndFreqs(filepath)
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
        tokenizedWords(args.filepath, top_n=args.number)
    elif args.function == "sentences":
        tokenizedSentences(args.filepath, top_n=args.number)