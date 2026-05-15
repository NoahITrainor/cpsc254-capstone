import pickle
import pandas as pd
import numpy as np
import faiss
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = OpenAI()

# Load the CSV
df = pd.read_csv("data/foreign_films.csv")

def embed(texts):
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [e.embedding for e in response.data]

# Embed in batches of 100
embeddings = []
print(f"Starting to read {len(df)} movies. This might take a few minutes...")

for i in range(0, len(df), 100):
    batch = df["plot_summary"].iloc[i:i+100].tolist()
    
    # The "Polite" loop: Keep trying until OpenAI lets us through
    while True:
        try:
            embeddings.extend(embed(batch))
            print(f"Successfully processed movies {i} through {i+len(batch)}...")
            break # It worked! Break out of the while loop and move to next batch
        except RateLimitError:
            print("Hit the OpenAI speed limit! Pausing for 5 seconds to cool down...")
            time.sleep(5) 

vectors = np.array(embeddings, dtype="float32")
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# Save files locally for the grader
faiss.write_index(index, "data/films.index")
with open("data/films_meta.pkl", "wb") as f:
    pickle.dump(df[["title", "country"]].to_dict("records"), f)

print(f"Database upgrade complete! Indexed {len(df)} films successfully.")