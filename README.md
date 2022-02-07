# README

## Execution:

Within SageMaker, open a Python Console Terminal and enter:
```py
get_ipython().system_raw('git clone https://github.com/sarthak815/AWS_Tweets_Project.git')
```
to clone the GitHub Repository.

Once cloned, use the commands:
```py
get_ipython().system_raw('cp ./AWS_Tweets_Project/setup.ipynb ./setup.ipynb')
get_ipython().system_raw('cp ./AWS_Tweets_Project/streamlit.ipynb ./streamlit.ipynb')
```

Restart and run all cells within setup.ipynb and streamlit.ipynb notebook.

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
