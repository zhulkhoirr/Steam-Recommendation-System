import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib

def cosine_recommended(input_game, user_preferences, steam_csv_path='dataset/steam.csv', similarity_file_path='model/cosine_similarity.npy'):
    
    steam_df = pd.read_csv(steam_csv_path)

    selected_columns_with_price = ['Name', 'Developers', 'Publishers', 'Categories', 'Genres', 'Tags', 'Price']
    
    steam_with_price_df = steam_df[selected_columns_with_price]

    selected_columns = ['Name', 'Developers', 'Publishers', 'Categories', 'Genres', 'Tags']
    
    steam_df = steam_df[selected_columns]
    steam_df.fillna('', inplace=True)

    features_combine = steam_df['Name'] + ' ' + steam_df['Developers'] + ' ' + steam_df['Publishers'] + ' ' + steam_df['Categories'] + ' ' + steam_df['Genres'] + ' ' + steam_df['Tags']

    vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    feature_vector = vectorizer.fit_transform(features_combine)

    similarity_matrix = np.load(similarity_file_path)

    if input_game:
        list_game = steam_df['Name'].tolist()
        find_close_match = difflib.get_close_matches(input_game, list_game)

        if not find_close_match:
            print(f"Game '{input_game}' tidak ditemukan dalam dataset!")
            return None, []

        close_match = find_close_match[0]
        game_index = steam_df[steam_df['Name'] == close_match].index[0]

    else:
        user_pref_vector = vectorizer.transform([user_preferences])
        similarity_score = list(enumerate(user_pref_vector.dot(feature_vector.T).toarray().flatten()))
        game_index = max(similarity_score, key=lambda x: x[1])[0]

    similarity_score = list(enumerate(similarity_matrix[game_index].flatten()))
    
    sorted_similar_game = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    # print(f"Game yang direkomendasikan untuk '{input_game}':\n")
    recommended_games = []

    

    for i, game in enumerate(sorted_similar_game[:10], 1):
        index = game[0]
        game_data = steam_with_price_df.iloc[index]
        recommended_games.append({
            'name': game_data['Name'],
            'price': game_data['Price'],
            'publisher': game_data['Publishers'],
            'developer': game_data['Developers'],
            'categories': game_data['Categories'],
            'genres': game_data['Genres'],
            'tags': game_data['Tags'],
            'score': game[1]
        })

    return game_index if input_game else user_preferences, recommended_games

# if __name__ == "__main__":
#     input_game = input("Masukkan judul game: ")
    
#     cosine_recommended(input_game)
