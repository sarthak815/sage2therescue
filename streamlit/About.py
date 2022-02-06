import streamlit as st

def app():
	st.title("About")
	st.markdown('''
		During the Cyclone Fani which hit Odisha in 2019 a lot of places ran out of electricity, water and other basic necessities. During this period most of the rescue workers relied on data accumulated pre disaster to guide rescue services but this was far off from the on ground reality where many places were in much worse of a situation than what was predicted. This is why we have developed this application to help guide rescue services in realtime using data from twitter. Even during the cyclone many parts of the city had mobile data running even though electricity and satellite television was not available. This is where our application comes into use by accessing the data posted to twitter we help guide rescue services towards the areas that need it the most.
## What it does
The application uses tweepy to retrieve tweets in real time using keywords given by the user. At the time of a disaster the city or state can be entered by the user into our application. Using the keyword received it retrieves all the tweets available, giving priority to the most recent tweets. These tweets we then run through a disaster prediction SVC model which was built using sagemaker. This model helps to eliminate tweets that are not disaster-related so that we only account for valid tweets. The newly generated set of tweets which contain only disaster related tweets is now run through a sentiment analysis model to determine the negativity or positivity of a tweet. Using the sentiment analysis model we assign a float value score between -1 and 1 to each tweet. Now we use NLTK to extract the locations present in each of the tweets and add the score from the tweet to determine a total score for each location based on the sentiment of the tweets describing these places. This is used to finally display a list of locations along with a score for each of them describing the severity of their situation.  We then use the names of the locations obtained and look up their coordinates using HERE api to plot them on a map with appropriate markings visually describing the severity of each of the locations.
## How we built it
1)SVC model from sklearn to determine whether a tweet is disaster-related
2)BERT model to determine sentiment behind each of the tweets
3)AWS Sagemaker to train both the SVC and BERT models
3)NLTK to extract the location keywords from the tweets
4)Tweepy to extract the tweets
5)Streamlit to deploy the app with an UI
6)HERE api to obtain the coordinates of each of the locations
## Challenges we ran into

## Accomplishments that we're proud of

## What we learned

## What's next for Sage Rescuer''')