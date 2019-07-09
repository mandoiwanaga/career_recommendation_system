import random
import pandas as pd
import pickle
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
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




with open('dreamjobber_tech/webapp/pickled_models/nn_model.pkl', 'rb') as f:
    nn_model = pickle.load(f)
app = Flask(__name__, static_url_path="")

with open('dreamjobber_tech/webapp/pickled_models/jobs.pkl', 'rb') as g:
    jobs = pickle.load(g)

#create session for feedback
app.config['SESSION_TYPE'] = 'mongodb'
Session(app)


@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')





with open('.secrets/mongodb_credentials.txt', 'r') as f:
   conn_string = f.read().strip()

mc = pymongo.MongoClient(conn_string)
jobrec_db = mc['job_recommendation_db']
user_coll = jobrec_db['user_collection']
feedback_coll = jobrec_db['user_feedback']

    
    
# def input_user_scores():
#     """Collect user score"""
    
   
#     print('''Scale of 0-10.
#     0 is Do NOT agree and 10 is agree''')

#     #col_names=['Analyst', 'Security', 'Leadership', 'Software/Web Dev', 
       #    'Cloud Computing', 'Computer Network', 'Database Admin', 'Computer Support', 'WebDev']
        
#        topics=['Analyst', 'Security', 'Leadership', 'Software/Web Dev', 
 #          'Cloud Computing', 'Computer Network', 'Database Admin', 'Computer Support', 'WebDev']
        
            
#     #user_scores = [float(input(f"Agree or Disagree: I am/I like {topic}: ")) / 10
#      #              for topic in topics]

#     user_scores = data['user_input1', 'user_input2', 'user_input3', 'user_input4', 
#     'user_input5', 'user_input6', 'user_input7', 'user_input8', 'user_input9'] 
#     print('\n')
#     user = np.array(user_scores).reshape(1, -1)
#     return user
    

def user_input(data):
    user_scores = data['user_inputs'] 
    print('\n')
    user = np.array(user_scores).reshape(1, -1)
    return user

    
    

def make_recommendation(nn_model, df, user=None):
    """Return top 10 recommended jobs based off user input"""
    if user is None:
        user = np.array([0,0,0,0,0,0,0,0,0]).reshape(1,-1)
    
    distances, indices = nn_model.kneighbors(user)
    
    job_recs = []
    for index in indices[0]:
        job_recs.append(df.iloc[index])

        
    # rec = []    
    # for index, value in enumerate(job_recs[:10], 1):
    #     rec.append("{}. {}".format(index, value))

   
    user_feedback = {'result': job_recs[:10],
                     'user_input': user.tolist()}
    user_coll.insert_one(user_feedback)

    return list(job_recs[:10])
    


    
    
# def collect_score_and_recommend(nn_model, df):
#     """Collect user score then output top 10 recommendations"""
#     user = input_user_scores()
#     return user, make_recommendation(nn_model, df, user)
    



def collect_feedback():
    """Collect user feedback and store it"""
    # print("How did you like your recommendations? bad, okay, or good")

    feedback = session.get('feedback') 
    user_feedback = {}   
    if feedback=='1':
        user_feedback['feedback'] = 'bad'
    elif feedback=='2':
        user_feedback['feedback'] = 'okay'
    elif feedback=='3':
        user_feedback['feedback'] = 'good'

    feedback_coll.insert_one(user_feedback)
    
    
# def show_to_user(nn_model, df):
#     user, result = collect_score_and_recommend(nn_model, df)
#     print(result)
#     collect_feedback(result, user)
#     return result
    
    


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Return recommendations."""
    data = request.json
    user = user_input(data)
    recommendation = make_recommendation(nn_model, jobs, user)
    return jsonify({'recommendations': recommendation})
    


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Record feedback."""
    data1 = request.json
    data1 = list(data1.values())
    session['feedback'] = data1[0]
    collect_feedback()
    return ''
    