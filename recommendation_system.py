import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

metadata = pd.read_csv('final_dataset.csv', low_memory=False)

# Calculate mean of score average column
C_1 = metadata['meta_score'].mean()
C_2 = metadata['user_score'].mean()

# Calculate the minimum score required to be in the chart
m_1 = metadata['meta_score'].quantile(0.80)
m_2 = metadata['user_score'].quantile(0.80)

# Filter out all qualified games into a new DataFrame
best_games = metadata[(metadata.meta_score> m_1) & (metadata.user_score > m_2)]

# Sort games based on score calculated above

best_games = best_games.sort_values('meta_score', ascending=False)

# Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

# Replace NaN with an empty string
metadata['description'] = metadata['description'].fillna('')

# Construct the required TF_IDF matrix by fitting and transformating the data
tfidf_matrix = tfidf.fit_transform(metadata['description'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# # Construct a reverse map of indices and games titles
# indices = pd.Series(metadata.index, index=metadata['name_game'])



def create_soup(x):
    return ' '.join(x['platform'])


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" "," "))
        else:
            return ''


def get_list(x):
    if isinstance(x, list):  # For tested
        return 1
    else:
        x = x.replace(" ", "", ).replace(",", " ").replace("'", "").replace("[", "").replace("]", "").split()
        return list(dict.fromkeys(x))

    # Return empty list in case of missing/malformed data
    return []


# Convert string into list
metadata['platform'] = metadata['platform'].apply(get_list)

# Apply clean_data functions to your features.
features = ['platform']

for feature in features:
    metadata[feature] = metadata[feature].apply(clean_data)

# Create a new soup feature
metadata['soup'] = metadata.apply(create_soup, axis=1)

# Import CountVectorizer and create the count matrix
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(metadata['soup'])

# Compute the Cosine Similarity matrix based on the count_matrix
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# Reset index of your main DataFrame and construct reverse mapping as before
metadata = metadata.reset_index()
indices = pd.Series(metadata.index, index=metadata['name_game'])

# Function that takes in game title as input and outputs most similar games
def get_recommendations(name_game, cosine_sim=cosine_sim2):
    # Get the index of the game thath matches the title

    idx = indices[name_game]

    # Get the pairwise similarity scores of all games with that game

    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the games based on the similarity scores

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar games

    sim_scores = sim_scores[1:11]

    # Get the games indices

    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar games

    return metadata['name_game'].iloc[movie_indices]






