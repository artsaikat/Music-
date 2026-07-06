import streamlit as st

from text.text_inference import predict_emotion
import pickle


st.header('Music Recommendation system')
user_text = st.text_input('Write your situation')

with open(r"C:\Users\Saikat Maiti\Desktop\Music recommendation\music\musicdata.pkl", "rb") as f:
    df = pickle.load(f)
    
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import CountVectorizer


with open(r"C:\Users\Saikat Maiti\Desktop\Music recommendation\count_vectorizer.pkl",'rb') as f:
    cv = pickle.load(f)
    
def similar(text1,text2):
    v1 = cv.transform([text1])
    v2 = cv.transform([text2])

    score = cosine_similarity(v1, v2)

    return float(score[0][0])

def recommend_songs(user_context,
                    final_emotion,
                    music_df):

    filtered = music_df[
        music_df["emotion"] == final_emotion
    ]

    scores = []

    for _, row in filtered.iterrows():

        score = similar(
            user_context,
            row["description"]
        )

        scores.append(
            (
                row["song"],
                row['Artist(s)'],
                score
            )
        )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores[:10]


if st.button("Emotion"):

    if user_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        emotion, confidence = predict_emotion(user_text)

        st.success(f"Emotion is {emotion}")
        st.success(f"Confidence: {confidence}")

        recommendations = recommend_songs(
            user_context=user_text,
            final_emotion=emotion,
            music_df=df
        )

        st.subheader("Recommended Songs")

        for rank, (song, artist ,score) in enumerate(recommendations, start=1):
            st.write(f"{rank}. {song} - {artist}")