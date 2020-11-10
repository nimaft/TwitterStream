from flask import (Blueprint, render_template, redirect, request, url_for, flash)
import requests
from urllib.parse import quote_plus
import os

bp = Blueprint('apiCall', __name__)


@bp.route('/', methods=('GET', 'POST'))
def getApi():

    if request.method == 'POST':
        term = request.form['query']
        return redirect(url_for('apiCall.results',term=term))

    return render_template('index.html')

#Route to redirect empty result requests to the main page
@bp.route('/results')
def rediHome():
    return redirect(url_for('apiCall.getApi'))


@bp.route('/results/<term>', methods=('GET', 'POST'))
def results(term=None):
    
    if request.method == 'GET' and term:
        
        #Getting search term from form field @ '/' route and converting it to url friendly string
        query = quote_plus(term)

        #Requesting tweets from Streaming API, returns 10 tweets
        bt = os.environ.get("BEARER")

        headers = {'Authorization': 'Bearer '+bt}
        query = "https://api.twitter.com/2/tweets/search/recent?query="+query+"&tweet.fields=author_id"
        response = requests.get(query,headers=headers)

        #Converting response to dictionary
        jsonResp = response.json()

        #Extracting data from dictionary (data would be a list of dictionaries)
        data = jsonResp["data"]


        #Looping through data dictionaries to get author_id and id
        #Using author_id and id to get embeded links for tweets
        embDict = []
        for x in data:
            urlReq = "https://publish.twitter.com/oembed?url=https://twitter.com/" + x["author_id"] + "/status/" + x["id"]
            embUrlReq = requests.get(urlReq,verify=False)
            embUrl = embUrlReq.json()

            #Storing embedded links in a list
            embDict.append(embUrl["html"].replace("\n",""))
        
        return render_template('results.html', rDict = embDict, term = term.upper())
    
    return render_template('index.html')
        

