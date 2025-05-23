import os
import pandas as pd
from flaskr import commentsScrap
from flask import Flask,render_template, request
import csv

def create_app(test_config=None):
	app = Flask(__name__,instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
		)

	if test_config is None:
		app.config.from_pyfile('config.py',silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/hello')
	def hello():
		return 'hello, world'

	@app.route('/')
	def home():
		return render_template('index.html')

	@app.route('/scrap',methods=['POST'])
	def scrap_comments():
		url=request.form.get('youtubeurl')
		get_full_comment =commentsScrap.scrapfyt(url)
		fields=['comment','sentiment']
		filename = "fullcomments.csv"

		with open(filename,'w',encoding="utf-8") as csvfile:
			writer =csv.DictWriter(csvfile,fieldnames=fields)

			writer.writeheader()
			writer.writerows(get_full_comment)

		full_comments_csv =pd.read_csv('fullcomments.csv')

		full_comments_csv.reset_index(drop=True, inplace=True)
		full_comments_csv.index = full_comments_csv.index + 1
		full_comments_csv.index.name='Index'
		full_comments_csv.reset_index(inplace=True)
    

		after_complete_message = "Your file is ready and sent to your mail id"

		df_empty = pd.DataFrame()
		df_empty.to_csv(filename, index=False)

		return render_template("index.html",after_complete_message=after_complete_message,full_comments_csv=[full_comments_csv.to_html(index=False)])

	return app

