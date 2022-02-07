# SAGE2TheRescue

## Inspiration
During Cyclone Fani, which hit Odisha in 2019, a lot of places ran out of electricity, water, and other basic necessities. During this period, most of the rescue workers relied on data accumulated pre-disaster to guide rescue services, but this was far off from the on-ground reality where many places were in much worse of a situation than what was predicted. This is why we have developed this application to help guide rescue services in real-time using data from Twitter. Even during the cyclone, many parts of the city had mobile data running even though electricity and satellite television were not available. This is where our application comes into use; by accessing the data posted to Twitter, we help guide rescue services towards the areas that need it the most.


## What it does
The application uses tweepy to retrieve tweets in real-time using keywords given by the user. At the time of a disaster, the city or state can be entered by the user into our application. Using the keyword received it retrieves all the tweets available, giving priority to the most recent tweets. These tweets we then run through a disaster prediction SVC model which was built using sagemaker. This model helps to eliminate tweets that are not disaster-related so that we only account for valid tweets. The newly generated set of tweets that contain only disaster-related tweets is now run through a sentiment analysis model to determine the negativity or positivity of a tweet. Using the sentiment analysis model we assign a float value score between -1 and 1 to each tweet. Now we use Spacy to extract the locations present in each of the tweets and add the score from the tweet to determine a total score for each location based on the sentiment of the tweets describing these places.

## Execution:

1. Within SageMaker (Clean Environment: GPU-instance), open a default:Python Console Terminal and enter:
```py
get_ipython().system_raw('git clone https://github.com/sarthak815/AWS_Tweets_Project.git')
```
&nbsp;&nbsp;&nbsp; to clone the GitHub Repository.

2. Once cloned, use the commands:
```py
get_ipython().system_raw('cp ./AWS_Tweets_Project/setup.ipynb ./setup.ipynb')
get_ipython().system_raw('cp ./AWS_Tweets_Project/streamlit.ipynb ./streamlit.ipynb')
```

3. Restart and run all cells within setup.ipynb notebook and wait for complete execution.

4. Restart and run all cells within streamlit.ipynb notebook and wait for complete execution.

#### To restart:
![restart](/images/restart.png)

#### In case of the following Error:
![ngrok-error](/images/error.jpg)

Please restart and run-all, the error happens due to latency and will recover.

## How we built it
1. SVC model from sklearn to determine whether a tweet is disaster-related
2. BERT model to determine sentiment behind each of the tweets
3. AWS Sagemaker to train both the SVC and BERT models
4. Spacy to extract the location keywords from the tweets
5. Tweepy to extract the tweets
6. Streamlit to deploy the app with a UI
7. HERE API to obtain the coordinates of each of the locations


## Challenges we ran into
1. The biggest challenge we faced was to find the right datasets for each of the models. When looking for a dataset to check whether the tweet is disaster-related or not, most of the datasets were very biased, so we couldn't combine multiple datasets.
2. Normalizing and scaling the scores in an appropriate fashion to adequately score the severity of disaster in each location


## Accomplishments that we're proud of
1. Obtaining map markers that are appropriately scaled and are a good representation of the actual scenario
2.  We made an original contribution to the HuggingFace Community. We employed our fine-tuned DistilBERT model


## What we learned
1. Classification of textual data from tweets between disaster or not using sklearn
1. Distilled BERT transformer model for sentiment analysis
2. Using Spacy NER to extract location data from the tweets, which helps us find the location of those in need
3. Using HERE API integration for geocoding 
4. Using folium, a python library for maps to plot the map and find a graphical representation of those in need


## What's next for Sage2TheRescue
1. Implementation on a larger scale, taking older tweets into account as well
2. Deploying on a host server accessible to all those who need it
3. Making the disaster identification model more accurate using a larger dataset

## Images:

![1](/images/1.png)
![2](/images/2.png)
![3](/images/3.png)
![4](/images/4.png)

## API Modifications:
### To Modify Tweepy API:

In the [functions.py](https://github.com/sarthak815/sage2therescue/blob/main/streamlit/functions.py), modify:

```py
class TweetScraper:
    def __init__(self):
        self.consumer_key = NONE
        self.consumer_secret = NONE
        self.access_key= NONE
        self.access_secret = NONE
```
