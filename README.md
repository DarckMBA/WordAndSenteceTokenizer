# WordAndSentenceTokenizer
A Python text analysis tool for tokenizing and analyzing word and sentence frequencies in text files.


## Features
- **Word Frequency Analysis**: Identify and visualize the most frequent words in a text
- **Sentence Frequency Analysis**: Extract and rank sentences by how often they appear
- **Stopword Filtering**: Remove common words to focus on meaningful content
- **Abbreviation Handling**: Correctly merges abbreviations (`Mr.`, `Mrs.`, `Dr.`) so they are not mistaken for sentence boundaries
- **Visualization**: Generate bar charts for easy pattern identification


## Installation
Requires Python 3.7+ with the following dependencies:

```bash
pip install matplotlib
```

### Quick Start
```bash
# Analyze word frequencies in a text file (top 10 by default)
python tokenizer.py frankenstein.txt

# Analyze top 20 words
python tokenizer.py frankenstein.txt -n 20

# Analyze top 10 sentences
python tokenizer.py frankenstein.txt --function sentences
```


## Usage
### Command-Line Interface
```bash
python tokenizer.py <filepath> [--function <function_name>] [-n <number>]
```

### Options
- `filepath`: Path to the text file to analyze (required)
- `--number, -n`: Number of top items to display (default: 10)
- `--function, -f`: Analysis function to run (default: `words`)

### Available Functions
#### Word Analysis
**`words`** (default) - Analyze top 10 most frequent words
```bash
python tokenizer.py frankenstein.txt
```

Analyze top 20 words:
```bash
python tokenizer.py frankenstein.txt -n 20
```

#### Sentence Analysis
**`sentences`** - Analyze top 10 most frequent sentences
```bash
python tokenizer.py frankenstein.txt --function sentences
```

Analyze top 5 sentences:
```bash
python tokenizer.py frankenstein.txt -f sentences -n 5
```


## How It Works
### Word Processing Pipeline
1. **Reading**: Opens and reads the entire text file
2. **Tokenization**: Splits text into tokens using regex (handles contractions, acronyms, decimals)
3. **Filtering**: Removes stopwords (common words like "the", "and", "is")
4. **Counting**: Tallies word frequencies using `Counter`
5. **Visualization**: Generates a bar chart of top word frequencies

### Sentence Processing Pipeline
1. **Reading**: Opens and reads the entire text file
2. **Normalization**: Replaces newlines with spaces for uniform processing
3. **Tokenization**: Splits on sentence-ending punctuation (`.`, `?`, `!`)
4. **Abbreviation merging**: Re-joins any sentence fragment that follows `Mr.`, `Mrs.`, or `Dr.`
5. **Counting**: Tallies sentence frequencies using `Counter`
6. **Visualization**: Displays results in the console and as a horizontal bar chart

### Stopwords
The tool filters words like:
```python
the, a, an, and, or, but, in, on, at, to, of, for, is, was, it, that, this, with, he, she, i, you, we, they
```

To modify stopwords, edit the `STOPWORDS` set in `tokenizer.py`.

### Abbreviations
The following abbreviations are handled by default and will not be treated as sentence boundaries:
```python
Mr, Mrs, Dr
```

To add more, edit the `ABBREVIATIONS` set in `tokenizer.py`.


## Function Reference
### Core Functions
- `tokenize_words(text)` - Splits text into word tokens using regex
- `words_and_freqs(filepath)` - Returns word frequency counter and total filtered word count
- `tokenize_sentences(text)` - Splits text into raw sentence tokens
- `merge_abbreviations(sentences)` - Re-joins sentence fragments split on abbreviation periods
- `sentences_and_freqs(filepath)` - Returns sentence frequency counter and total sentence count

### Analysis Functions
- `tokenized_words(filepath, top_n=50)` - Display word frequency bar chart
- `tokenized_sentences(filepath, top_n=20)` - Print sentence frequency table and display horizontal bar chart

**Note**: The `-n` or `--number` command-line flag overrides function defaults.


## Examples
### Analyze Frankenstein (top 10 words, default)
```bash
python tokenizer.py frankenstein.txt
```

### Analyze top 25 words in Frankenstein
```bash
python tokenizer.py frankenstein.txt -n 25
```

### Analyze top 15 sentences
```bash
python tokenizer.py frankenstein.txt --function sentences -n 15
```


## Output
- **Word Analysis**: Interactive matplotlib bar chart with top word frequencies
- **Sentence Analysis**: Ranked table printed to the console, plus a horizontal bar chart
- Charts are displayed in a window that allows zoom, pan, and save operations


## Notes
- Word analysis is case-sensitive by default; tokens are matched as they appear in the source text
- Non-word characters (except those in contractions and acronyms) are excluded from word tokens
- The tool processes entire files into memory; very large files may require significant RAM
- Charts can be saved from the matplotlib interface using the Save icon
- Short forms: `-n` for `--number`, `-f` for `--function`