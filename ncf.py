import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

def ncf_recommended(input_user, users_path='dataset/users.csv', user_with_games_path='dataset/user_with_games.csv', model_path='model/model.h5'):
    
    users_df = pd.read_csv(users_path)
    user_with_games_df = pd.read_csv(user_with_games_path)
    model = load_model(model_path, compile=False)
    
    # users_df = users_df[users_df['Playtime'] != 0.0]

    users_df = users_df.fillna(0.1)

    user_encoder = LabelEncoder()
    users_df['user'] = user_encoder.fit_transform(users_df['UserID'])
    user_ids = user_encoder.classes_
    n_users = len(user_ids)

    app_encoder = LabelEncoder()
    users_df['app'] = app_encoder.fit_transform(users_df['AppID'])
    app_ids = app_encoder.classes_
    n_app = len(app_ids)

    user_encoded = dict(zip(user_encoder.classes_, user_encoder.transform(user_encoder.classes_)))
    back_user_encoded = dict(zip(user_encoder.transform(user_encoder.classes_), user_encoder.classes_))

    app_encoded = dict(zip(app_encoder.classes_, app_encoder.transform(app_encoder.classes_)))
    back_app_encoded = dict(zip(app_encoder.transform(app_encoder.classes_), app_encoder.classes_))

    user_games = users_df[users_df.UserID == input_user]['AppID'].values

    all_games = set(user_with_games_df['AppID'])
    unplayed_games = all_games - set(user_games)

    user_encoder = user_encoded.get(input_user)
    unplayed_game_encoders = [[app_encoded.get(x)] for x in unplayed_games if x in app_encoded]

    user_game_array = np.hstack(([[user_encoder]] * len(unplayed_game_encoders), unplayed_game_encoders))
    user_game_array = [user_game_array[:, 0], user_game_array[:, 1]]

    recommendations = model.predict(user_game_array).flatten()

    top_recommendations = (-recommendations).argsort()[:10]

    recommended_games_ids = [back_app_encoded.get(unplayed_game_encoders[top_recommendations[x]][0]) for x in range(len(top_recommendations)) if unplayed_game_encoders[top_recommendations[x]][0] in back_app_encoded]

    results = []
    top_recommendations_ids = []
    for index, game_encoder in enumerate(unplayed_game_encoders):
        game_id = back_app_encoded.get(game_encoder[0])
        if game_id in recommended_games_ids:
            top_recommendations_ids.append(game_id)
            try:
                game_info = user_with_games_df[user_with_games_df.AppID == game_id].iloc[0]
                results.append({
                    'name': game_info['Name'],
                    'price': game_info['Price'],
                    'publisher': game_info['Publishers'],
                    'developer': game_info['Developers'],
                    'categories': game_info['Categories'],
                    'genres': game_info['Genres'],
                    'tags': game_info['Tags'],
                    'score': recommendations[index]
                })
            except Exception as e:
                print(f"Error processing game {game_id}: {e}")
                continue

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by='score', ascending=False)
    # print(results_df)
    return results_df

    
if __name__ == "__main__":

    users_df = pd.read_csv('dataset/users.csv')
    recommendation_per_user = users_df.groupby('UserID').size()
    input_user =  recommendation_per_user[recommendation_per_user > 1].sample(1).index[0]

    ncf_recommended(input_user)