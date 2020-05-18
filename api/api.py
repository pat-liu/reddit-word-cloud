import time
from flask import Flask, request, send_file
import praw
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import requests
import prawcore as prawcore
from io import BytesIO

app = Flask(__name__)

@app.route('/result', methods = ['GET', 'POST'])
def result():
    if request.method == 'GET':
        subreddit = request.args.get('subreddit', None)
        if subreddit:
           image = getImage(subreddit)
           return image
        return "No place information is given"

import praw
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import requests
from io import BytesIO

def getImage(subredditInput):
    reddit = praw.Reddit(client_id='AibGRssNGr9zOA', client_secret='VUc8jZJWx9_ERc5Yx8IHws0LgGM', user_agent='dont_judge_mee')

    subreddit = subredditInput
    try:
        reddit.subreddit(subreddit)._fetch()
    except prawcore.exceptions.Forbidden:
        return 'Subreddit not found–please enter a valid subreddit!'
    except prawcore.exceptions.Redirect:
        return 'Subreddit not found–please enter a valid subreddit!'

    
    text=''
    stopwords = ['and', 'the', 'for', 'of', "http", "https",  "to", "it", "in", "not", "but",
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
                 "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 
                 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
                 "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
                 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 
                 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
                 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 
                 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 
                 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', 
                 "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 
                 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', 
                 "weren't", 'won', "won't", 'wouldn', "wouldn't", "college", "student", "really", "also", "com", "to", "like"
                  "may", "to", "imgur", "reddit"]

    url=''
    if subreddit == 'upenn':
        url = 'https://66.media.tumblr.com/avatar_dd11bac58f1d_512.pnj'
    if subreddit == 'stanford':
        url = 'https://hoopdirt.com/wp-content/uploads/2018/07/61-61244.jpg'
    if subreddit == 'yale':
        url = 'https://content.sportslogos.net/logos/35/920/full/4132_yale_bulldogs-alternate-0.png'
    if subreddit == 'harvard':
        url = 'https://cdn10.bigcommerce.com/s-2hqm4/products/3050/images/52455/ncaa0130__50885.1544238872.1280.1280.jpg?c=2'
    if subreddit == 'princeton':
        url = 'https://www.nj.com/resizer/P9qyzbLwp46BtpEBP-3NOCXsSKU=/1280x0/smart/advancelocal-adapter-image-uploads.s3.amazonaws.com/image.nj.com/home/njo-media/width2048/img/princeton_main/photo/princeton-logojpg-62f8bfe7d4328c6f.jpg'
    if subreddit == 'brownu':
        url = 'https://wpcdn.us-east-1.vip.tn-cloud.net/www.abc6.com/content/uploads/2017/05/7199569_G-1024x686.jpg'
    if subreddit == 'dartmouth': 
        url = 'https://assets.website-files.com/5d7a471526acc60066ee1bf2/5d88f7a66ef0a1ebeb7ba023_LonePine_RGB.png'
    if subreddit == 'cornell': 
        url = 'https://i.redd.it/2dx1u8mfle941.jpg'
    if subreddit == 'columbia':
        url = 'https://images-na.ssl-images-amazon.com/images/I/61IWspKT-JL._AC_SL1375_.jpg'
    if subreddit == 'berkeley':
        url = 'https://www.logolynx.com/images/logolynx/22/2211ce0a4ea591651132553e0ca0932c.jpeg'
    if subreddit == 'ucla':
        url = 'https://static.uclabruins.com/custompages/Logo_Library/UCLA_OnWhite.jpg'

    stop_words = set(stopwords)

    mask = None

    if url is not '':
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        mask = np.array(img)


    top_posts = reddit.subreddit(subreddit).top()
    for post in top_posts:

        text += post.title.lower() + " "

    #wordcloud = WordCloud(collocations=False).generate(text)
    try:
        wordcloud = WordCloud(width=800, height=800, stopwords=stop_words, background_color="white", mode="RGBA", max_words=1000, collocations=False, mask=mask).generate(text)
    except ValueError: 
        return 'Subreddit is empty!'
    plt.switch_backend('agg')
    plt.figure(figsize=[16,9])
    if url is not '':
        image_colors = ImageColorGenerator(mask)
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight', interpolation='bilinear')
    return send_file('./wordcloud.png', attachment_filename='wordcloud.png')



if __name__ == '__main__':
    app.run(debug = True)