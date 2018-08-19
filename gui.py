from guizero import App, PushButton, Slider,Text
from pymongo import MongoClient
#https://lawsie.github.io/guizero/alerts/

c = MongoClient()
db=c["mydatabase"]
article = db.articles
app = App(title="PosNews")
i = 0;
find_data = article.find({'source':'CNBC'})
obj = next(find_data,None)
while(obj):
    Text(app, text=obj['title'])
    obj = next(find_data,None)
    i = i+1
    if(i==11):
        break
#message = Text(app, text="Welcome to the Hello world app!")
app.display()

