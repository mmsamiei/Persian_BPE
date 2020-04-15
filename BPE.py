from collections import Counter, defaultdict
from pprint import pprint
import re

END_OF_WORD_SIGN = '</w>'

def read_text_file(path: str)-> str:
    f = open(path, "r")
    contents = f.read()
    return contents

def build_vocab(corpus: str) -> dict:
    """Step 1. Build vocab from text corpus"""

    # Separate each char in word by space and add mark end of token
    tokens = [" ".join(word) + END_OF_WORD_SIGN for word in corpus.split()]

    # Count frequency of tokens in corpus
    vocab = Counter(tokens)

    return vocab


def get_stats(vocab: dict) -> dict:
    """Step 2. Get counts of pairs of consecutive symbols"""

    pairs = defaultdict(int)
    for word, frequency in vocab.items():
        symbols = word.split()

        # Counting up occurrences of pairs
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += frequency

    return pairs


def merge_vocab(pair: tuple, v_in: dict) -> dict:
    """Step 3. Merge all occurrences of the most frequent pair"""

    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')

    for word in v_in:
        # replace most frequent pair in all vocabulary
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]

    return v_out

def vocab_to_set(vocab: dict) -> set:
    vocab_set = set()
    for v in vocab.keys():
        for w in v.split():
            if w not in vocab_set:
                vocab_set.add(w)
    return vocab_set

def write_vocabset(path: str, vocab_set: set) -> bool:
    f = open(path, 'w')
    for index, vocab in enumerate(vocab_set):
        refined_vocab = vocab.replace(END_OF_WORD_SIGN, '')
        f.write(str(index)+'\t'+refined_vocab+'\n')
    return True


if __name__ == '__main__':
    corpus = read_text_file('persian.txt')
    vocab = build_vocab(corpus)
    num_merges = 100  # Hyperparameter
    for i in range(num_merges):

        pairs = get_stats(vocab)  # Step 2

        if not pairs:
            break

        # step 3
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)

    vocab_set = vocab_to_set(vocab)
    write_vocabset('output.txt', vocab_set)