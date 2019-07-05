# dreamjobber (tech edition)
Haven't discovered your passion? Your dreamjob? Figure out what you were born to do with DreamJobber!


# Business Understanding
For a lot of people figuring out what you want to do as a career is a difficult task, most especially for young individuals graduating from high school or Military Veterans. There are many new jobs and fields emerging in tech world that many people may not be aware of. I want to create a simple application that requires a user to answer a few questions about their interest etc, and give recommendations of possible dream TECH jobs, this will give the user direction in making some important life decisions.  

# Data Understanding
My source of data will be from DICE. Dice is an online job search platform for TECH jobs only. I will aquire the data via web-scrape and store them as json files. 


# Data Preparation
1. Feature engineer (create df with job titles and job descriptions)
2. Remove job titles with no descriptions
3. Text Clean for job descriptions
    - Tokenize
    - Remove words with fewer than 3 characters
    - Remove stop words
    - Normalize words (Lemmetize)



# Modeling
- bag of words
- lda model for topic extraction
- coherence to find optimal number of topics
- label topics
- classification with nearest neighbors


# Evaluating


# Deployment
The model will be deployed as a Flask app with a user friendly interface. The user will simply answer a series of questions and it will output the top 10 recommended tech jobs. Bonus would be some job details like avg salary, education, and other useful info.

#add instructions to replicate project
