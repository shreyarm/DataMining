__author__ = 'shreyarajani'

import sys
from collections import Counter
import json


def top_ten(tweet_file):
    file_name = tweet_file.name
    f = open(file_name)
    file_read = f.read()
    tweet_data = json.loads(file_read)

    top_dict = {}

    #Getting the individual hashtags from the json file
    for i in range(0, len(tweet_data)):
        temp = tweet_data[i]["entities"]["hashtags"]
        for j in temp:
            if "text" in j:
                hashtag = j["text"]
                #counting the hashtags
                if hashtag in top_dict:
                    top_dict[hashtag] += 1.0
                else:
                    top_dict[hashtag] = 1.0

    #Getting the top 10 values of the hashtags
    final_dict = dict(Counter(top_dict).most_common(10))
    t_tuple = sorted(final_dict.items(), reverse=True, key=lambda x: x[1])

    for t in range(0, len(t_tuple)):
        print t_tuple[t][0], t_tuple[t][1]

def main():
    tweet_file = open(sys.argv[1])
    top_ten(tweet_file)


if __name__ == '__main__':
    main()