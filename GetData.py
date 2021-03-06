import praw
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime as dt
from datetime import datetime
import numpy as np
import pandas as pd
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import *
from matplotlib.figure import Figure

class mclass:
	def __init__(self, root):
		self.root = root
		
		root.title("Reddit Scrape")
		
		
		self.l1=Label(root,text="Subreddits to Search")
		self.l2=Label(root,text="Keyword to Search")
		self.l3=Label(root,text="Max Number of Entries")
		self.e1 = Entry(root, width = 40)
		self.e2 = Entry(root, width = 40)
		self.e3 = Entry(root, width = 40)

		self.t1 = self.e1.get()
		self.t2 = self.e2.get()
		self.t3 = self.e3.get()

		self.l1.pack()
		self.e1.pack()
		self.l2.pack()
		self.e2.pack()
		self.l3.pack()
		self.e3.pack()

		self.e1.focus_set()
		
		b=Button(root, text="Run", width=20, command = self.run)
		b.pack()
		
	def plot (self):
		
		file = open("data.txt", "r")
		holder = file.read()
		
		holder = [x for x in  re.split(' ', holder) if x]
		
		dates = []
		values = []

		

		for x in range(int(len(holder)/3)):
			dates.append(holder[(3*x)])
		dates=[re.compile(r"-").sub("", m) for m in dates]
		for x in range(int(len(holder)/3)):
			values.append(float(holder[(3*x)+2]))
		
		sorted_values = [x for _,x in sorted(zip(dates,values))]
		dates.sort()
		
		
		#dates.sort()
		#values.sort()
		x = [datetime.strptime(d, '%Y%m%d').strftime('%m/%d/%Y') for d in dates]
		#y = [data_values[]]
		
		fig = Figure(figsize=(10,6))
		a = fig.add_subplot(111)
		a.scatter(x,sorted_values)
		a.set_title ("Sentiment vrs Time", fontsize=16)
		a.set_ylabel("Sentiment", fontsize=14)
		a.set_xlabel("Date", fontsize=14)
		
		#a.set_xticks(x[::20]) 
		
		canvas = FigureCanvasTkAgg(fig, master=self.root)
		canvas.get_tk_widget().pack()
		canvas.draw()
		

	def run(self):
		file_input = open('input.txt', 'w')

		file_input.write(self.e1.get())
		file_input.write("\n")
		file_input.write(self.e2.get())
		file_input.write("\n")
		file_input.write(self.e3.get())
		file_input.close()
		
		
		reddit = praw.Reddit(client_id='SU3DL2_kxAdtqw',
						client_secret="hq0dRanTH4gmFcN4tfbFXcAcKeA",
						user_agent='RamhacksMW')
					 
		file_input = open('input.txt', 'r')
	
		sin = file_input.read()
		sf = sin.split('\n')
		sub_name = sf[0]
		sub_search = sf[1]
		limit_num = int(float(sf[2]))

		subreddit = reddit.subreddit(sub_name)

		data_subreddit = subreddit.search(sub_search,limit=limit_num)

		file_data = open("data.txt", 'w')

		for submission in data_subreddit:
	
			def get_date(created):
				return dt.datetime.fromtimestamp(created)
	
	
			dataT=submission.title
			dataB=submission.selftext
			dataC=submission.comments.list()
			dataD=submission.created
			dataTD=get_date(dataD)
	
			file_data.write(" ")
			file_data.write(str(dataTD))
			file_data.write(" ")
	
			sid = SentimentIntensityAnalyzer()
			infull = ""
			infullc = ""
		
			infull += dataT
			if dataB != "":
				infull += " "
				infull += dataB
	
			submission.comments.replace_more()
			l = submission.comments.list()
			for x in range(len(l)):
				infullc += l[x].body
				infullc += " "
	
			infullc = infullc.lower()
	
			setToken = sent_tokenize(infull)
			setTokenc = sent_tokenize(infullc)
	
			ogpost_score = 0
			total_score = 0
			counter = 0
	
			for sen in setToken:
				ss=sid.polarity_scores(sen)
				s=ss['compound']
		
				ogpost_score += s
				total_score += s
				counter += 1
		
			print(ogpost_score)
			for sen in setTokenc:
				ss=sid.polarity_scores(sen)
				s=ss['compound']
				if ogpost_score < 0:
					s = -s
				if s == 0.0:
					continue
				total_score += s
				counter += 1
	
			average_score = total_score / counter
			file_data.write(str(average_score))

		file_data.close()
		self.plot()
	
	
	

	
	
	
root=Tk()
start=mclass(root)
mainloop()
