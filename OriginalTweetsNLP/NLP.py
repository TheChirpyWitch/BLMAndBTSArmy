#
# Read text (tweet) and userdescription from CSV file using Pandas
# timestamp , text , user_id , user_description ,  
import pandas as pd
df=pd.read_csv("originalTweet_841_4columns.csv", sep=r'\s*,\s*', header=0, encoding='utf8')
#print(df.shape)
#print(df.columns.tolist())
tweets=df['text']
#print(tweets)


# 
# clean text using NLTK
import nltk
#nltk.download()
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()
#s0 = "This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--"
#print(tknzr.tokenize(s0))
#for tweet in tweets:
#    print(tknzr.tokenize(tweet))

#
# compute embedding vectors from text
from embedding_as_service.text.encode import Encoder  
en = Encoder(embedding='word2vec', model='google_news_300')
#vecs = en.encode(texts=['hello aman', 'how are you?'])  
#for tweet in tweets:
#    vec = en.encode([tweet], is_tokenized=True)
#    print(vec)
vecs = en.encode(tweets, is_tokenized=True)
vecs = np.squeeze(vecs) 

#
# compute cos similarity between two tweets
from sklearn.metrics.pairwise import cosine_similarity
tw1=vecs[0].reshape(1,-1)
tw2=vecs[100].reshape(1,-1)
print('CosSim(Tweet[0], Tweet[100])', cosine_similarity(tw1, tw2))

