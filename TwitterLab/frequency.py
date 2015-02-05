__author__ = 'shreyarajani'

import sys
import json
import string


def cal_freq(tweet_file):
    # Reading the tweet_file
    file_name = tweet_file.name
    f = open(file_name)
    file_read = f.read()
    tweet_data = json.loads(file_read)

    single_tweet_dict = {}
    tweet_ctr_dict = {}
    total_ctr = 0

    #loop to extract tweet and then get individual tweets
    for i in range(0, len(tweet_data)):
        single_tweet = tweet_data[i]["text"]
        single_tweet_dict[i] = single_tweet
        for char in string.punctuation:
            single_tweet = single_tweet.replace(char, ' ')
        word_list = single_tweet.split() #  words of the tweets

        # counting the number words and its frequency
        for tweet_word in word_list:
            if tweet_word in tweet_ctr_dict:
                tweet_ctr_dict[tweet_word] += 1
                total_ctr += 1
            else:
                tweet_ctr_dict[tweet_word] = 1
                total_ctr += 1

    #finding the final frequency by dividing it with the total number of words
    for i in tweet_ctr_dict:
        freq = float(tweet_ctr_dict[i])/float(total_ctr)
        tweet_ctr_dict[i] = freq
        print i, " ", tweet_ctr_dict[i]


def main():
    tweet_file = open(sys.argv[1])
    cal_freq(tweet_file)


if __name__ == '__main__':
    main()