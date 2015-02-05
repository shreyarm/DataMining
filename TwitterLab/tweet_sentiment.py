import sys
import json
import string


def q2(sent_file, tweet_file):
    '''
    The method fins the tweets from the given file by using json
    :param sent_file: sentiment file, here AFINN-111.txt
    :param tweet_file: I have used top-1-output.txt file
    '''
    # TODO Fill me in!
    sent_file_name = sent_file.name
    sent_f = open(sent_file_name)
    sent_file_lines = sent_f.readlines()
    non_blank_count = 0
    single_tweet_dict = {}

    #Counts the number of non-blank lines from the sent_file
    with open(sent_file_name) as xyz:
        for line in xyz:
            if line.strip():
                non_blank_count += 1

    file_name = tweet_file.name
    f = open(file_name)
    file_read = f.read()
    tweet_data = json.loads(file_read)

    #loops around the tweet_file and gets the individual tweet
    for i in range(0, len(tweet_data)):
        single_tweet = tweet_data[i]["text"]
        single_tweet_dict[i] = single_tweet
        #removes the extra not needed character like ,./;:'"><
        for char in string.punctuation:
            single_tweet = single_tweet.replace(char, ' ')
        word_list = single_tweet.split()  # words of the tweets
        sent_value = 0
        #checks the word with the sentiment and calues the sentiment value
        for tweet_word in word_list:
            for var in range(0, non_blank_count):
                sent_words = sent_file_lines[var]
                sent_word = sent_words.split("\t")
                try:
                    tweet_word_s = str(tweet_word)
                except UnicodeEncodeError:
                    pass
                if tweet_word_s == sent_word[0]:
                    sent_value += float(sent_word[1])
                else:
                    sent_value += float(0.0)

        print "Tweet: ", single_tweet, "Sent Value:", sent_value
        print "========================================================="

def main():
    """ given the name of the sentiment lexicon file and
    the tweet file, call the q2 method to compute tweet sentiment
    """
    #do not change these next two lines, but you may make other changes in this method
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    q2(sent_file, tweet_file)


if __name__ == '__main__':
    main()
