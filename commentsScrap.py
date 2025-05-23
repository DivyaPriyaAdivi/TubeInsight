from googleapiclient.discovery import build
import os
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
from transformers import pipeline
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

positive=0
negative =0
netural =0
count =0
def scrapfyt(url):
	count =0
	end =url.index("?")
	video_id=url[17:end]

	youtube =build('youtube','v3',developerKey=api_key)
	response =youtube.commentThreads().list(part='snippet',videoId=video_id,maxResults=100,textFormat='plainText').execute()
	commentList=[]

	full_comments=[]


	while response:
		for items in response['items']:
			comment = items['snippet']['topLevelComment']['snippet']['textDisplay']
			commentList.append(comment)

		if 'nextPageToken' in response:
			response=youtube.commentThreads().list(part='snippet',videoId=video_id,maxResults=100,textFormat='plainText',pageToken=response['nextPageToken']).execute()
		else:
			break


	def clean_comment(comment):
	    comment = re.sub(r'http\S+', '', comment)  # Remove URLs
	    comment = re.sub(r'[^\w\s]', '', comment)  # Remove special characters
	    comment = comment.lower()  # Convert to lowercase
	    return comment

	cleaned_comments = [clean_comment(comment) for comment in commentList]
	


	analyzer = SentimentIntensityAnalyzer()

	def sentimentanalysis(comment):
		global negative , positive ,netural,count
	

		vs = analyzer.polarity_scores(comment)
		
		if vs['compound']>=0.5:
			positive =positive+1
			tags = "positive"
		elif vs['compound']>-0.5 and vs['compound']< 0.5:
			netural = netural+1
			tags="netural"
		elif vs['compound']<=-0.5:
			negative = negative+1
			tags="negative"
		dict_list={ 'comment':comment,'sentiment':tags}
		full_comments.insert(count-1,dict_list)


	for comment in cleaned_comments:
		sentimentanalysis(comment)

	
	return full_comments