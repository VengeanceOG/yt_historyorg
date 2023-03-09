import json as js
import mysql.connector as mysql
import re
from tabulate import tabulate
import sys
#import all modules
db=mysql.connect(host='localhost',user='root',password='hvk33500')
if db.is_connected:
	print('database successfully connected')
else:
	print('database connection not successfull') #to see id database is connected
#define functions to parse through string and extract useful data
def ext(m,x):
	if x=='date':
		return re.findall('(.*)T',m)[0]
	if x=='time':
		return re.findall('T(.*)Z',m)[0]
	if x=='title':
		return re.findall(' (.*)',m)[0]
cur=db.cursor()
cur.execute('create database if not exists yt_history')
cur.execute('use yt_history')
cur.execute('drop table if exists video')
cur.execute('create table video(sr_no int(250) primary key unique not null auto_increment, title varchar(250), channel varchar(250), time varchar(250), date varchar(250))')
fname=input('enter file name\n')
try:
	f=open(fname,'r',encoding='utf-8')
except:
	sys.exit('the given file name is invalid')
f=js.load(f)
for video in f: #loop through each element in json and parse date time title and channel of the video
	title=ext(video['title'],'title')
	if 'time' in video:
		date=ext(video['time'],'date')
	else:
		date=None
	if 'time' in video:
		time=ext(video['time'],'time')
	else:
		time=None
	if 'subtitles' in video:
		channel=video['subtitles'][0]['name']
	else:
		channel=None
	cur.execute("insert into video(title,channel,time,date) values (%s,%s,%s,%s)",(title,channel,time,date))
	db.commit()
cur.execute('select * from video')
history=cur.fetchall()
#now display your history in python
print(tabulate(history,headers=['Sr_no','Title','Channel','Time','Date'], tablefmt="grid"))
