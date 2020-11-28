import pandas as pd
import re
import unicodedata
import nltk
from unidecode import unidecode
from nltk.tokenize import TweetTokenizer
import pymongo

tknzr = TweetTokenizer()

from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()

def _removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

def remove_accents(input_str): 
	nfkd_form = unicodedata.normalize('NFKD', input_str) 
	return u"".join([c for c in nfkd_form])

def check_bts_words(token_words, wordlist):
	for word in token_words:
		if word in wordlist:
			return "True"
	return "False"

def check_unicode(sentence):
	checked_words = ""
	for word in sentence.split(" "):
		if word[:2] != '\\u':
			checked_words = checked_words + " " + word
	return checked_words


df=pd.read_csv("retweet_12349_5columns.csv", sep=r'\s\s*,\s\s*', header=0)

userBios=df['target_description'].astype(str)

nodes = df['target_user_id']

wordlist=[]
with open('wordlist.txt') as f:
    for line in f:
        wordlist.append(line.lower().rstrip())
f.close()

i = 0
check = 0 

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bts"]
mycol = mydb["fan_classification"]

print("Nodes length:")
print(len(nodes))

for i in range(0, len(nodes)):
	fan="true"
	user = nodes[i]
	line = userBios[i]

	bio = check_unicode(line.lower())

	tokenizer = nltk.RegexpTokenizer(r"\w+")
	bio_tokens = tokenizer.tokenize(bio)
	fan = check_bts_words(bio_tokens, wordlist)
	mydict = {'user': user, 'bio': bio, 'bio_tokens': bio_tokens, 'class': fan}
	x = mycol.insert_one(mydict)

	print(str(i) + "/" + str(len(nodes)))


	if fan == "True":
		check+=1

print(check)
