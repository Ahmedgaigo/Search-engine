import math
from collections import defaultdict, Counter
import re


def tokenize(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    tokens = text.split()
    return tokens


class InvertedIndex:
    def __init__(self, transcripts):
        self.transcripts = transcripts
        self.index = self.build_index()
        self.doc_count = len(transcripts)
        self.idf = self.compute_idf()
        self.tf_idf = self.compute_tf_idf()

    def build_index(self):
        index = defaultdict(list)
        for doc_id, transcript in enumerate(self.transcripts):
            tokens = tokenize(transcript)
            for token in set(tokens):
                index[token].append(doc_id)
        return index

    def compute_idf(self):
        idf = {}
        for term, doc_ids in self.index.items():
            idf[term] = math.log(self.doc_count / len(doc_ids))
        return idf

    def compute_tf_idf(self):
        tf_idf = defaultdict(lambda: defaultdict(float))
        for doc_id, transcript in enumerate(self.transcripts):
            tokens = tokenize(transcript)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                tf = count / len(tokens)
                tf_idf[doc_id][token] = tf * self.idf.get(token, 0)
        return tf_idf

    def search(self, query):
        query_tokens = tokenize(query)
        scores = Counter()
        for token in query_tokens:
            if token in self.index:
                for doc_id in self.index[token]:
                    scores[doc_id] += self.tf_idf[doc_id][token]
        return scores.most_common()


def load_transcripts(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    transcripts = load_transcripts('data/transcripts.txt')
    index = InvertedIndex(transcripts)
    print(index.search('your search query'))
