import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from ast import literal_eval
from numpy import asarray
from numpy import savetxt

pd.options.mode.chained_assignment = None

# Read datasets
metadata = pd.read_csv('datasets/final_dataset.csv', converters={'platform': literal_eval})
features = pd.read_csv('datasets/features.csv')

# Add features to metadata
metadata = metadata.join(features)
metadata = metadata.dropna(subset=['genre'])
metadata['genre'] = metadata['genre'].apply(literal_eval)


# Function that takes in game title as input and outputs most similar games


def create_soup(x):
    return ' '.join(x['platform']).lower() + ' ' + ''.join(str(x['developer']).split()) + ' ' + ' '.join(
        x['genre']) + ' ' + str(x['type']) + ' ' + str(x['rating'])


# Create a new soup feature
metadata['soup'] = metadata.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(metadata['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# Reset index of your main DataFrame and construct reverse mapping as before
metadata = metadata.reset_index()
indices = pd.Series(metadata.index, index=metadata['name_game'])


def get_recommendations(name_game, cosine_sim=cosine_sim2):
    # Get the index of the game thath matches the title
    idx = indices[name_game]

    # Get the pairwise similarity scores of all games with that game
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the games based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 8 most similar games
    sim_scores = sim_scores[1:13]

    # Get the games indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar games
    return metadata.iloc[movie_indices]
