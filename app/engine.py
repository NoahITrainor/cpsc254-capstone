import pickle
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

# Load the local index built by the data script
index = faiss.read_index("data/films.index")
with open("data/films_meta.pkl", "rb") as f:
    meta = pickle.load(f)

def extract(movie_title: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0, # <-- THIS IS THE SECRET WEAPON! It stops hallucinations.
        messages=[
            {"role": "system", "content": "You are a strict cinema verification bot. If the movie provided by the user does NOT exist in real life, you must reply with ONLY the word FAKE. If the movie is real, list exactly 3 core themes and 1 emotional tone, comma-separated."},
            {"role": "user", "content": f"Extract themes for the movie: '{movie_title}'"}
        ],
    )
    return resp.choices[0].message.content.strip()

def retrieve(query: str, k: int = 5) -> list[dict]:
    vec = client.embeddings.create(model="text-embedding-3-small", input=[query])
    q = np.array([vec.data[0].embedding], dtype="float32")
    _, indices = index.search(q, k)
    return [meta[i] for i in indices[0]]

def synthesize(movie_title: str, candidates: list[dict]) -> list[dict]:
    films_text = "\n".join(
        f"{i+1}. {c['title']} ({c['country']})" for i, c in enumerate(candidates)
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content":
            f"A user loves '{movie_title}'. For each film below, write exactly one sentence "
            f"explaining why it's a good cross-cultural recommendation.\n\n{films_text}"}],
    )
    lines = [l.strip() for l in resp.choices[0].message.content.strip().split("\n") if l.strip()]
    for i, c in enumerate(candidates):
        # Clean up bullet points if the AI added them
        clean_line = lines[i] if i < len(lines) else ""
        c["explanation"] = clean_line.lstrip("0123456789. ") 
    return candidates

def recommend(movie_title: str) -> list[dict]:
    query = extract(movie_title)
    
    # THE FIX: Check if the word FAKE is anywhere in the string, ignoring case
    if "FAKE" in query.upper():
        return [] 

    candidates = retrieve(query)
    return synthesize(movie_title, candidates)