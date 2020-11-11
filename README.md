# TwitterStream
[![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiYzhsZ2dLMGVISmNHNlkvV2lKeXluOEhHeDlyRmNNMW1ESlA1Y1dOaEhZSDBZbDJWd1h4REFLV3p4dXN2OXFueldqQ1BJMElVT1Y2ZHB3WTV4ME5kUXY4PSIsIml2UGFyYW1ldGVyU3BlYyI6IlIrNktYQkc5V015NUM5WXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)]

A simple web server powered by [Flask](https://flask.palletsprojects.com/), created to recieve and process 10 latest tweets based on user query.

## Overview
* User enters a search term.
* Flask processes the request and extracts the query term.
* It uses Twitter API v2 [Filtered Stream](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/introduction) endpoint to filter the complete stream of real-time public Tweets and stores the response.
* Twitter's response is parsed and *author_id* and *id* are extracted from it.
* Using the extracted values, webserver submits requests to Twitter [oEmbed API](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-oembed) to recieve the URL of the Tweet to be embedded.
* Once all the embed URLs are created. Flask stores them in a list and pass them on to results page.
* Results page takes the URL list and by using Jinja2 creates the page, embeds all the tweets and display them to user.

### Flask
Although this is a simple app. I used Flask application factory to make it scalable. Using application factory approach allows creating Flask apps inside a function instead of  creating a global Flask instance directly at the top of your code.

* There is one blueprint and three view functions to handle:
  * index page (/)
  * results page (/results/<query>)
  * results page with no query (/results)
  * *404 error handling is addressed on application factory (__ init __ .py)* 
 
 
* HTTP methods:
  * index page recieves accepts both GET and POST methods:
    * GET: renders the template for index.html
    * POST: user has searched for a term > redirects to /results/<term> page
  * reults page (when recieving a search query)
    * GET
      * confirms the search term is not empty
      * converts search term to url friendly term (e.g. converts #NYC to %23NYC)
      * sends the request to Twitter and stores the response
      * converts the response from JSON to Python dictionary and stores data in a list
      * loops throught list values, extracts author_id and id, creates a string and submit it to oEmbed api to get embed URL
      * stores the embed URLs in a list, passes search term, results list and renders results.html
    * POST: should not accept receive requests, in case it does, renders index.html
 
 
 * Templates: used by Flask to render dynamic webpages. Base template holds links to stylesheets and scripts.
 
 
 #### At this point you might ask: what is the point? I created this little web app to use with a CI/CD pipeline on Amazon AWS. Here are the other pipeline related repos:
 * 
 * 
 * 
 
