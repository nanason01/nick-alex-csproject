import sqlite3
import pandas as pd
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
#ts = int("1284101485")
#print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
#

con = sqlite3.connect("redditPosts.db")

# Print table columns
cur = con.cursor()
data = cur.execute('''SELECT * FROM posts''')
#for row in data.description:
#    print(row)


postDict = Counter()
for gme in cur.execute('SELECT * FROM posts WHERE title LIKE "gme"'):
        #print(datetime.utcfromtimestamp(gme[1]).strftime('%Y-%m-%d %H:%M:%S'))
        postDict[(datetime.utcfromtimestamp(gme[1]).strftime('%Y-%m-%d'))] +=1

for gme in cur.execute('SELECT * FROM posts WHERE title LIKE "gamestop"'):
        #print(datetime.utcfromtimestamp(gme[1]).strftime('%Y-%m-%d %H:%M:%S'))
        postDict[(datetime.utcfromtimestamp(gme[1]).strftime('%Y-%m-%d'))] +=1

cum = postDict.items()
x,y = zip(*cum)

plt.plot(x,y)
index = pd.date_range(start = "2018-07-01", end = "2022-12-12", freq = "D")
index = [pd.to_datetime(date, format='%Y-%m-%d').date() for date in index]


#ax = plt.gca()
#ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gcf().autofmt_xdate() # Rotation
#plt.show()

plt.show()
#print(postDict)


