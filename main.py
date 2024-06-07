from inverted_index import InvertedIndex, load_transcripts, tokenize
from distance import levenshtein_distance


class SearchEngine:
    def __init__(self, transcript):
        self.index = InvertedIndex(transcript)
        self.transcripts = transcript

    def search(self, query):
        scores = self.index.search(query)
        similar_queries = self.find_similar_queries(query)
        return scores, similar_queries

    def find_similar_queries(self, query):
        query_tokens = tokenize(query)
        similar_queries = []
        for token in query_tokens:
            min_distance = float('inf')
            closest_token = token
            for term in self.index.index.keys():
                distance = levenshtein_distance(token, term)
                if distance < min_distance:
                    min_distance = distance
                    closest_token = term
            similar_queries.append((token, closest_token, min_distance))
        return similar_queries


if __name__ == "__main__":
    transcripts = load_transcripts('./data/transcript.txt')
    search_engine = SearchEngine(transcripts)
    query1 = 'sample data'
    score, similar_query = search_engine.search(query1)
    print(f"Search results: {score}")
    print(f"Similar queries: {similar_query}")
