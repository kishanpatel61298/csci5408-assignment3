#The positive and negative words are downloaded from belowed link.
#http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html

import json
import math

positive_list = []
negative_list = []

#read positive words
positive_files = open("positive_words.txt")
positive_lines = positive_files.readlines()
for line in positive_lines:
    line = line.rstrip('\n')
    positive_list.append(line)

#read negative words
negative_files = open("negative_words.txt")
negative_lines = negative_files.readlines()
for line in negative_lines:
    line = line.rstrip('\n')
    negative_list.append(line)

text_tweets = []
all_tweets_json = []

#this will read 10 json files each with 200 tweets inside it and convert it into bucket-of-words
for i in range(1,10):
    file = open('tweets/file'+str(i)+'.json')
    json_of_file = json.load(file)

    for each_tweet in json_of_file:
        temp_json = {}
        temp_json['tweet_text'] = each_tweet['text']
        text_tweets.append(each_tweet['text'])
        counts = dict()
        words = each_tweet['text'].split()
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        word_dict = counts
        temp_token_json = json.dumps(word_dict, indent = 4)
        temp_json['tokens'] = temp_token_json
        all_tweets_json.append(temp_json)

count = -1
print("No   Tweet               Polarity     Match")
print("-------------------------------------------------")

#this for loop iterate on each tweet and compnare each word from tweet to positive and neative words
for each_tweet in all_tweets_json:
    count = count + 1
    positive_count = 0
    negative_count = 0
    positive_encountered_list = []
    negative_encountered_list = []
    each_tweet_dict = json.loads(each_tweet['tokens'])
    #take all the keys, which are words, and store it in items. Later, iterate on item to compare each word
    items = each_tweet_dict.keys()

    for positive_index in positive_list:
        if str(positive_index) in items:
            positive_encountered_list.append(str(positive_index))
            positive_count = positive_count+1

    for negative_index in negative_list:
        if str(negative_index) in items:
            negative_encountered_list.append(str(negative_index))
            negative_count = negative_count+1

    if positive_count > negative_count:
        print(str(count)+"   "+text_tweets[count][:15]+"...   positive    "+str(positive_encountered_list))
    elif positive_count < negative_count:
        print(str(count)+"   "+text_tweets[count][:15]+"...   negative    "+str(negative_encountered_list))
    elif positive_count == negative_count and positive_count > 0:
        print(str(count)+"   "+text_tweets[count][:15]+"...   neutral    "+str(negative_encountered_list)+str(positive_encountered_list))
    elif positive_count == negative_count and positive_count == 0:
        print(str(count)+"   "+text_tweets[count][:15]+"...   "+"neutral")


#============================= Problem 3 ======================================
# Problem 3 uses the tweets stored in bag-of-words from Problem 2. 

n = len(all_tweets_json)
words = ["flu","snow","cold"]
flu_count = 0
snow_count = 0
cold_count = 0
article_with_cold = []
article_with_cold_text = []

for each_tweet in all_tweets_json:
    each_tweet_dict = json.loads(each_tweet['tokens'])
    items = each_tweet_dict.keys()
    for each_word in words:
        if str(each_word) in items:
            if str(each_word) == "flu":
                flu_count = flu_count + 1
            elif str(each_word) == "snow":
                snow_count = snow_count + 1
            elif str(each_word) == "cold":
                cold_count = cold_count + 1
                article_with_cold.append(each_tweet)

print()
print("Query |  df  |  n/df  |  Log10(n/df)")
print("--------------------------------------")
if flu_count > 0:
    print("flu   |  "+str(flu_count)+"   |  "+str(round(n/flu_count,2))+"  |  "+str(round(math.log10(n/flu_count),2)))

if snow_count > 0:
    print("snow  |  "+str(snow_count)+"   |  "+str(round(n/snow_count,2))+"  |  "+str(round(math.log10(n/snow_count),2)))

if cold_count > 0:
    print("cold  |  "+str(cold_count)+"   |  "+str(round(n/cold_count,2))+"  |  "+str(round(math.log10(n/cold_count),2)))

print()
print("Tweet                |   m   |   f")
print("--------------------------------------")
relative_frequency_list = []
for each_article in article_with_cold:
    each_tweet_dict = json.loads(each_article['tokens'])
    items = each_tweet_dict.keys()
    cold_count_temp = 0

    print(each_article['tweet_text'][:15]+"...   |   "+str(len(each_tweet_dict))+"  |  "+str(each_tweet_dict['cold']))
    relative_frequency = int(each_tweet_dict['cold'])/len(each_article)
    each_article['rf'] = relative_frequency
    relative_frequency_list.append(each_article)

#getting highest relative frequency
max_count = -1
highest_rf = None
for i in relative_frequency_list:
    if float(i['rf']) > max_count:
        max_count = float(i['rf'])
        highest_rf = i

print()
print("Highest relative frequency: "+str(highest_rf['rf']))
print("Tweet: "+highest_rf['tweet_text'])
