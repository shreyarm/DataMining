import twitter
import json

# First: Go to http://twitter.com/apps/new to create an app and get values
# for these credentials that you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information
# on Twitter's OAuth implementation.

#FILL IN HERE
CONSUMER_KEY = "ubivw7i2kPGxxMbKMt2OejFuW"
CONSUMER_SECRET = "9xBD9SbUSXuLpbhNOxiE47zjR6aDOgj7ZdjypmfKl3uymsYTqd"
OAUTH_TOKEN = "350934778-mkFrVSTujkw4RZ0dzZiqfMJceOq1scLDYgBRFsSv"
OAUTH_TOKEN_SECRET = "OWX2GjjrBXmFBoaAt65QYFv9eqvdjqUxVyrIbRT8RDeK5"

def oauth_login():
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def play_around(twitter_api):
    WORLD_WOE_ID = 1
    US_WOE_ID = 23424977

    # Prefix ID with the underscore for query string parameterization.
    # Without the underscore, the twitter package appends the ID value
    # to the URL itself as a special case keyword argument.

    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    us_trends = twitter_api.trends.place(_id=US_WOE_ID)
    print world_trends
    print
    print us_trends
    print
    print json.dumps(world_trends, indent=1)
    print
    print json.dumps(us_trends, indent=1)

    world_trends_set = set([trend['name']
                        for trend in world_trends[0]['trends']])

    us_trends_set = set([trend['name']
                         for trend in us_trends[0]['trends']])

    common_trends = world_trends_set.intersection(us_trends_set)

    print common_trends


if __name__ == "__main__":
    twitter_api = oauth_login()
    play_around(twitter_api)