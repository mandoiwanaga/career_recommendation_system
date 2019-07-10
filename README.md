# DreamJobber (tech edition)
### Recommendations System for Tech Jobs


# Business Understanding
Have you ever asked yourself what tech job should I pursue? Maybe even what kind of tech jobs are out there today? (2019). I sure have and its not an easy task considering there are new tech jobs and fields emerging that some people may not be aware of. So I've made a Tech Job specific Recommendation System that will find jobs based on your preferences. 

## Product: [dreamjobber.online](www.dreamjobber.online)

# Data Understanding
My source of data is [dicejobs](www.dice.com), an online job search platform for Tech jobs. 
The data consisted of about 20,000 job titles and descriptions. Data was obtained via web-scrape using selenium and stored as json files. 

Example of data scraped:

![Alt text](images/dice.png?raw=true "Title")


# Data Preparation
1. Feature engineer (create a dataframe with job titles and job descriptions)
2. Text Clean 
    - Remove punctuations, numbers, and lowercase all words
    - Tokenize
    - Remove words with fewer than 3 characters
    - Remove stop words
    - Normalize words (Lemmetize and Stem)


# Modeling
After data preparation, I implemented Bag of Words for term frequency and gensim's bow2doc function to count the number of occurrences of each distinct word, convert the word to its integer word id and return the result as a sparse vector. I then used an LDA (Latent Dirichlet Allocation) model to classify job descriptions to 9 different topic groups. I chose 9 topic groups because it best represents the job groups in the Tech Job market. Next I created a dataframe with topic scores and their corresponding job titles and descriptions. 
The next step was to tie in a user's input to make recommendations. Because my data is text data, I used an unsupervised learning model, Nearest Neighbors using Euclidean Distance metric. A user can input probabilities based on the 9 topics and will calculate the closest instances the model has been fitted on. 

# Evaluating
Because I don't have user data prior to modeling and deployment, I am collecting feedback evaluations from users. I will store the user's inputs, recommendation outputs, and feedback of whether they liked their recommendations or not. These are being stored in mongodb atlas. 


# Future Work
- Add links to the output of recommendations in order to provide details about each recommendation, ex.    description or avg salary. 
- Classify job titles.
- After collecting sufficient user feedback, create an ALS recommendation model.