import twitter_access_DM
import argparse
import json

#Code based on
## https://rawgit.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition/master/ipynb/html/Chapter%209%20-%20Twitter%20Cookbook.html
def twitter_search(twitter_api, q, max_results=200, **kw):

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and
    # https://dev.twitter.com/docs/using-search for details on advanced
    # search criteria that may be useful for keyword arguments

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)

    statuses = search_results['statuses']

    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.

    # Enforce a reasonable limit
    max_results = min(1000, max_results)

    for _ in range(10):  # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:  # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=')
                        for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)

        print json.dumps(search_results['statuses'])

        statuses += search_results['statuses']

        if len(statuses) > max_results:
            break

    return statuses



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("search_terms", help="Base search term string", type=str)
    parser.add_argument("-m", help="Max number of results to return, default 1000", type=int)
    args = parser.parse_args()

    max = 1000
    if args.m:
        max = args.m

    twitter_api = twitter_access_DM.oauth_login()
    results = twitter_search(twitter_api, args.search_terms, max_results=max)
    # You can also save the results here if you want
    # print json.dumps(results)
