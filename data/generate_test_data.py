import pandas as pd
import os

data = {
    "title": ["Seven Samurai", "Pan's Labyrinth", "Amélie", "City of God", "Parasite"],
    "country": ["Japan", "Mexico", "France", "Brazil", "South Korea"],
    "plot_summary": [
        "A veteran samurai gathers six others to protect a village from bandits.",
        "In post-Civil War Spain, a girl finds a mythical labyrinth and meets a faun.",
        "An innocent and naive girl in Paris decides to help those around her.",
        "Two boys growing up in a violent neighborhood of Rio de Janeiro take different paths.",
        "A poor family schemes to become employed by a wealthy family by infiltrating their household."
    ]
}

pd.DataFrame(data).to_csv("data/foreign_films.csv", index=False)
print("Test CSV created!")