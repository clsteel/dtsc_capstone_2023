"""
This file contains analytical code used in the film success predictor web app.

That comes down to two things mainly:
 * Taking the form data from the web app and formatting it for model prediction
    e.g. in Modeling/modeling.ipynb, we define the model's input/output vectors:
        X = data[['runtime','Documentary','action_adv_war_west','horror_thriller',
            'family_animate','scifi_fantasy','hist_drama','crime_mystery',
            'comedy_romance_music','release_month','common_word_count']]
        y = data['adj_revenue_millions']
 * Preparing a response useful response.
    - The model's only output prediction is adj_revenue_millions, but we'll calculate this
    with 12 different release months and present the user with the 'winning' release month.
    - We could also present some example similar movies alongside this.

"""
import pickle
import pandas as pd
import numpy as np
from typing import Optional

from sklearn.ensemble import RandomForestRegressor

genres = ["action", "adventure", "war", "western", "horror", "thriller", "family",
          "animation", "sciencefiction", "fantasy", "history", "drama", "comedy",
          "romance", "music", "documentary", "crime", "mystery"]

months_dict = {0:"January", 1: 'February', 2: "March", 3: 'April', 4: 'May', 5: 'June', 6: "July",
               7: "August", 8: "September", 9: "October", 10: "November", 11: "December"}

months_df = pd.DataFrame(np.diag(np.ones(12)), columns=['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                                        'August', 'September', 'October', 'November', 'December'])
model: Optional[RandomForestRegressor] = None
MODEL_FNAME = "../Modeling/model.pkl"
COMMON_WORDS_FNAME = "../data_cleaning/words.pkl"
POSTER_FNAME = "../data_cleaning/posters.pkl"


def initialize_model():
    global model
    print('Loading trained model...')
    model = pickle.load(open(MODEL_FNAME, 'rb'))
    print('Loading model complete')


def analyze_form_data(form):
    if not model:
        raise Exception("ERROR: model not yet initialized")
    elif type(model) != RandomForestRegressor:
        raise TypeError(f"ERROR: model type is incorrect: {type(model)}")

    month_releases = dict()
    for month in range(0, 12):
        x_input = _create_model_inputs(form)
        x_input = x_input.join(months_df.iloc[[month]].reset_index(drop=True))
        y_i = model.predict(x_input)
        month_releases[month] = y_i

    # Results of our analysis: 12 different box office predictions.
    best_month = [m for m in month_releases.keys() if month_releases[m] == max(month_releases.values())][0]
    gross_earnings = np.round(month_releases[best_month], 2)
    output = f"This film is predicted to gross ${gross_earnings[0]} million if released in: {months_dict[best_month]}"
    print(output)
    return output


def _analyze_common_word_count(synopsis):
    common_word_count = 0
    with open(COMMON_WORDS_FNAME, 'rb') as fpickle:
        common_words = pickle.load(fpickle)

        # now lowercase all the synopsis words and use trim/strip etc
        synopsis_words = synopsis.replace('+', ' ').strip().lower().split(' ')
        for word in synopsis_words:
            if word in common_words:
                common_word_count += 1
    return common_word_count


def _create_model_inputs(form, release_month=12):
    """
    Need to create an array of these values:
    X = data[['runtime','Documentary','action_adv_war_west','horror_thriller',
            'family_animate','scifi_fantasy','hist_drama','crime_mystery',
            'comedy_romance_music','common_word_count','January','February','March','April','May','June','July',
            'August','September','October','November','December']]
    """
    # Grab the runtime input
    runtime = form['runtime']

    # Grab *and* combine the genres inputs...
    genres_on = [g for g in genres if g in form.keys()]

    # 1. documentary input value
    documentary = 1 if 'documentary' in genres_on else 0

    # 2. extract and combine the values for action, adventure, war, west,...
    action = 1 if 'action' in genres_on else 0
    adventure = 1 if 'adventure' in genres_on else 0
    war = 1 if 'war' in genres_on else 0
    western = 1 if 'western' in genres_on else 0
    action_adv_war_west = action | adventure | war | western

    # 3. Extract/combine for horror/thriller
    horror = 1 if 'horror' in genres_on else 0
    thriller = 1 if 'thriller' in genres_on else 0
    horror_thriller = horror | thriller

    # 4. Extract/combine for family/animated
    family = 1 if 'family' in genres_on else 0
    animated = 1 if 'animated' in genres_on else 0
    family_animate = family | animated

    # 5. Extract/combine for scifi/fantasy
    sciencefiction = 1 if 'sciencefiction' in genres_on else 0
    fantasy = 1 if 'fantasy' in genres_on else 0
    scifi_fantasy = sciencefiction | fantasy

    # 6. Extract/combine for history/drama
    history = 1 if 'history' in genres_on else 0
    drama = 1 if 'drama' in genres_on else 0
    hist_drama = history | drama

    # 7. Extract/combine for crime/mystery
    crime = 1 if 'crime' in genres_on else 0
    mystery = 1 if 'mystery' in genres_on else 0
    crime_mystery = crime | mystery

    # 8. Extract/combine for comedy/romance/music
    comedy = 1 if 'comedy' in genres_on else 0
    romance = 1 if 'romance' in genres_on else 0
    music = 1 if 'music' in genres_on else 0
    comedy_romance_music = comedy | romance | music

    # 3. get the common word count from the synopsis
    common_word_count = _analyze_common_word_count(form['synopsis'])

    input_vector = [int(runtime), documentary, action_adv_war_west, horror_thriller, family_animate,
                     scifi_fantasy, hist_drama, crime_mystery, comedy_romance_music, common_word_count]
    columns = ['runtime', 'Documentary', 'action_adv_war_west', 'horror_thriller', 'family_animate',
               'scifi_fantasy', 'hist_drama', 'crime_mystery', 'comedy_romance_music', 'common_word_count']
    input_df = pd.DataFrame([input_vector], columns=columns)

    return input_df


if __name__ == "__main__":
    # This only gets run if we run analysis.py in order to test its functionality
    form_data_tst = "action=on&runtime=69&synopsis=mission+life+action"
    form = {'runtime': '210', 'synopsis': 'mission+life+action', 'action': 'on', 'western': 'on'}
    # form = {'runtime': '210', 'synopsis': '', 'action': 'on', 'western': 'on'}
    initialize_model()
    analyze_form_data(form) # This film is predicted to gross: [57.9809891] if released in: Month #11
