import pandas as pd

  # Load metadata (no header)
meta_cols = ["wikipedia_id", "freebase_id", "title", "release_date",
               "box_office", "runtime", "languages", "countries", "genres"]
meta = pd.read_csv("data/movie.metadata.tsv", sep="\t", header=None, names=meta_cols)

  # Load plot summaries
plots = pd.read_csv("data/plot_summaries.txt", sep="\t", header=None,
                      names=["wikipedia_id", "plot_summary"])

print(f"Loaded {len(meta)} movies and {len(plots)} plot summaries.")

  # Merge on Wikipedia ID
df = meta.merge(plots, on="wikipedia_id")
print(f"After merge: {len(df)} movies.")

  # Filter out US films
df = df[~df["countries"].str.contains("United States of America", na=False)]
print(f"After excluding US films: {len(df)} movies.")

  # Keep and rename relevant columns
df = df[["title", "countries", "plot_summary"]].rename(columns={"countries": "country"})

  # Drop rows with missing data
df = df.dropna()
print(f"After dropping missing data: {len(df)} movies.")

df.to_csv("data/foreign_films.csv", index=False)
print("Saved to data/foreign_films.csv")