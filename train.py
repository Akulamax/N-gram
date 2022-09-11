from collections import defaultdict, Counter
import numpy as np
import re
import random
import io
import pickle
import argparse


def get_tokens(text):
    tokens = list()
    alphabet = re.compile(u'[а-яА-Я0-9-]+|[.]+')
    with io.open(text, encoding='utf-8') as data:
        for line in data:
            for token in alphabet.findall(line.lower()):
              tokens += {token}
    return tokens


def get_ngrams_from_tokens(tokens, n):
  ngrams = zip(*[tokens[i:] for i in range(n)])
  return ngrams


def get_start_ngram(n, text):
    tokens = get_tokens(text)
    n_grams = get_ngrams_from_tokens(tokens, n)
    return random.choice(list(n_grams))


def prefix_to_tuple(prefix):
    return tuple(item for item in prefix.split(' '))


class NgramModelTextGeneration:
    dict_counter = defaultdict(lambda: Counter())

    def __init__(self, text, number_of_words = 7):
        self.text = text
        self.number_of_words = number_of_words + 1

    def fit(self):
        tokens = get_tokens(self.text)
        for i in range(self.number_of_words - 1):
            num = self.number_of_words - i
            n_grams = get_ngrams_from_tokens(tokens, num)
            for n_token in n_grams:
              self.dict_counter[n_token[:num - 1]][n_token[num - 1]] += 1

    def get_k_most_popular_endings(self, n_gram):
        return list(self.dict_counter[n_gram])

    def next_word(self, n_gram):
        words = Counter()
        for length in range(len(n_gram)):
            endings = self.get_k_most_popular_endings(n_gram[length:])
            for i in range(len(endings)):
                words[endings[i]] = self.dict_counter[n_gram[length:]][endings[i]]
            if (len(words) > 2 or ( length > 3 and len(words) > 0)):
              return random.choice(list(words)[-3:])
            else:
              words.clear()
        return get_start_ngram(1, self.text)[0]

    def generate(self, length, prefix = ''):
        result_text = list()
        result_text += prefix
        if (len(prefix) > 0):
            if (type(prefix) != tuple):
                prefix = prefix_to_tuple((prefix))
            else:
                for i in range(length - len(prefix)):
                    word = self.next_word(prefix)
                    result_text += [word]
                    if (len(prefix) < self.number_of_words):
                        prefix = prefix + tuple([word])
                    else:
                      prefix = prefix[1:] + tuple([word])
        else:
            if (length < self.number_of_words):
                return list(get_start_ngram(length, self.text))
            else:
                prefix = get_start_ngram(self.number_of_words - 1, self.text)
                result_text += prefix
                for i in range(length - self.number_of_words):
                    word = self.next_word(prefix)
                    prefix = prefix[1:] + tuple([word])
                    result_text += [word]
        return result_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    if (args.input_dir):
        model = NgramModelTextGeneration(args.input_dir)
    else:
        model = NgramModelTextGeneration(input())
    model.fit()
    pkl_filename = args.model
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

if __name__ == "__main__":
    main()
