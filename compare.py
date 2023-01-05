import argparse
import re
from collections import Counter
from typing import List, Callable

import numpy as np
from numpy.linalg import norm


def clean(s: str) -> str:
    s = re.sub(r"#.", "", s)
    s = re.sub(r"'''.*?'''", "", s)
    s = re.sub(r'""".*?"""', "", s)
    s = re.sub(r'".*?"', "", s)
    s = re.sub(r"'.*?'", "", s)
    return s


class TfidfVectorizer:
    def __init__(self, preprocessor: Callable[[str], str] = None):
        self.preprocessor = preprocessor
        self.corpus = None
        self.norm_corpus = None
        self._df = None
        self._tf = None
        self._tfidf = None
        self._idf = None

    def fit_transform(self, corpus: List[str]) -> np.ndarray:
        self.corpus = corpus
        self.preprocessing_text()
        self.tf()
        self.df()
        self.idf()
        self.tfidf()
        return self._tfidf

    def __normalize_corpus(self, d: str) -> str:
        if self.preprocessor is not None:
            d = self.preprocessor(d)
        d = re.sub(r"[^a-zA-Z0-9\s]", "", d, re.I | re.A)
        d = d.lower().strip()
        tks = d.split()
        return " ".join(tks)

    def preprocessing_text(self):
        n_c = np.vectorize(self.__normalize_corpus)
        self.norm_corpus = n_c(self.corpus)
        print(self.norm_corpus[0])

    def tf(self):
        words_array = [doc.split() for doc in self.norm_corpus]
        words = list(set([word for words in words_array for word in words]))
        features_dict = {w: 0 for w in words}
        tf = []
        for doc in self.norm_corpus:
            bowf_doc = Counter(doc.split())
            all_f = Counter(features_dict)
            bowf_doc.update(all_f)
            tf.append(bowf_doc)
        out = dict()
        for i in tf:
            for feature, value in i.items():
                out[feature] = out.get(feature, []) + [value]
        self._tf = np.column_stack(list(out.values()))

    def df(self):
        self._df = 1 + np.sum(self._tf, axis=0)

    def idf(self):
        N = 1 + len(self.norm_corpus)
        idf = 1.0 + np.log(float(N) / self._df)
        self._idf = idf

    def tfidf(self):
        tfidf = self._tf * self._idf
        norms = norm(tfidf, axis=1)
        self._tfidf = tfidf / norms[:, None]


parser = argparse.ArgumentParser(
    prog="Plagiarism Doctor", description="Yes, it is like Plague Doctor"
)
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()
input_path, output_path = args.input, args.output
vectorizer = TfidfVectorizer(preprocessor=clean)
with open(input_path, encoding="UTF-8") as inp, open(
    output_path, encoding="UTF-8", mode="w"
) as out:
    for line in inp.readlines():
        first_file, second_file = line.split()
        try:
            with open(first_file, encoding="UTF-8") as x, open(
                second_file, encoding="UTF-8"
            ) as y:
                x = x.read()
                y = y.read()
                tfidf = vectorizer.fit_transform([x, y])
                pairwise_similarity = tfidf @ tfidf.T
                score = round(pairwise_similarity[0][1], 2)
                out.write(f"{score}\n")
        except FileNotFoundError:
            out.write(f"It appears files {first_file} or {second_file} are missing.\n")
        except BaseException as e:
            out.write(
                f"There's been a problem (namely {e}) with analyzing {first_file} and {second_file} files.\n"
            )
