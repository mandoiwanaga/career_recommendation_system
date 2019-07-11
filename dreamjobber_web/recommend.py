import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk
import pymongo

from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary


with open(".secrets/mongodb_credentials.txt", "r") as f:
    conn_string = f.read().strip()

mc = pymongo.MongoClient(conn_string)
jobrec_db = mc["job_recommendation_db"]
user_coll = jobrec_db["user_collection"]


def input_user_scores():
    """Collect user score"""

    print(
        """Scale of 0-10.
    0 is Do NOT agree and 10 is agree"""
    )

    # col_names=['Analyst', 'Security', 'Leadership', 'Software/Web Dev',
    #      'Cloud Computing', 'Computer Network', 'Database Admin', 'Computer Support', 'WebDev']

    topics = [
        "Analyst",
        "Security",
        "Leadership",
        "Software/Web Dev",
        "Cloud Computing",
        "Computer Network",
        "Database Admin",
        "Computer Support",
        "WebDev",
    ]

    user_scores = [
        float(input(f"Agree or Disagree: I am/I like {topic}: ")) / 10
        for topic in topics
    ]
    print("\n")
    user = np.array(user_scores).reshape(1, -1)
    return user


def make_recommendation(nn_model, df, user=None):
    """Return top 10 recommended jobs based off user input"""
    if user is None:
        user = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(1, -1)

    distances, indices = nn_model.kneighbors(user)

    job_recs = []
    for index in indices[0]:
        job_recs.append(df.iloc[index])

    # similarity = []
    # for distance in distances[0]:
    #   similarity.append(round(distance, 8))

    rec = []
    for index, value in enumerate(job_recs[:10], 1):
        rec.append("{}. {}".format(index, value))

    return list(rec)
    # return list(zip(rec, similarity[:10]))


def collect_score_and_recommend(nn_model, df):
    """Collect user score then output top 10 recommendations"""
    user = input_user_scores()
    return user, make_recommendation(nn_model, df, user)


def collect_feedback(result, user):
    """Collect user feedback and store it in mongodb atlas"""
    user_input = input("""How did you like your recommendations? bad, okay, or good""")

    user_feedback = {"result": result, "user_input": user.tolist()}

    if user_input == "bad":
        user_feedback["feedback"] = "bad"
    elif user_input == "okay":
        user_feedback["feedback"] = "okay"
    elif user_input == "good":
        user_feedback["feedback"] = "good"

    user_coll.insert_one(user_feedback)


def show_to_user(nn_model, df):
    """Collect user score, make recommendation, collect feedback, and store in mongodb atlas"""
    user, result = collect_score_and_recommend(nn_model, df)
    print(result)
    collect_feedback(result, user)
