import tkinter as tk
from tkinter import scrolledtext
from main import SearchEngine
from inverted_index import load_transcripts


class SearchEngineGUI:
    def __init__(self, root, search_engine):
        self.root = root
        self.root.title("Search Engine")
        self.search_engine = search_engine

        self.query_label = tk.Label(root, text="Enter Query:")
        self.query_label.pack()

        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.results_text.pack()

    def perform_search(self):
        query = self.query_entry.get()
        scores, similar_queries = self.search_engine.search(query)

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Search Results for '{query}':\n\n")
        for doc_id, score in scores:
            self.results_text.insert(tk.END, f"Document ID: {doc_id}, Score: {score}\n")
            self.results_text.insert(tk.END, f"Content: {self.search_engine.transcripts[doc_id]}\n\n")

        self.results_text.insert(tk.END, "\nSimilar Queries:\n")
        for token, closest_token, distance in similar_queries:
            self.results_text.insert(tk.END, f"Query Token: {token}, Closest Token: {closest_token}, Distance: {distance}\n")


if __name__ == "__main__":
    transcripts = load_transcripts('./data/transcript.txt')
    _search_engine = SearchEngine(transcripts)

    _root = tk.Tk()
    gui = SearchEngineGUI(_root, _search_engine)
    _root.mainloop()
