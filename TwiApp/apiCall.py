from flask import (Blueprint, render_template, redirect, request, url_for, flash)
import requests

bp = Blueprint('apiCall', __name__)


@bp.route('/', methods=('GET', 'POST'))
def getApi():

    if request.method == 'POST':
        term = request.form['query']
        return redirect(url_for('apiCall.results',term=term))

    return render_template('index.html')


@bp.route('/results/<term>', methods=('GET', 'POST'))
def results(term=None):
    
    if request.method == 'GET' and term:
        
        #Getting form field from '/' route 
        #query = term

        #Requesting tweets from Streaming API, returns 10 tweets
        bt = 'AAAAAAAAAAAAAAAAAAAAAAONJQEAAAAA1wHsP7ozvwm0FPeVGgzqODg0Dhs%3DppJgXkaWKv3w2knqe7FSF2GquoVHzW4mTtPYYZotzeibD5OdSk'

        headers = {'Authorization': 'Bearer '+bt}
        response = requests.get("https://api.twitter.com/2/tweets/search/recent?query="+term+"&tweet.fields=author_id",headers=headers)

        #Converting response to dictionary
        jsonResp = response.json()

        #Extracting data from dictionary (data would be a list of dictionaries)
        data = jsonResp["data"]


        #Looping through data dictionaries to get author_id and id
        #Using author_id and id to get embeded links for tweets
        i=1
        embDict = []
        for x in data:
            urlReq = "https://publish.twitter.com/oembed?url=https://twitter.com/" + x["author_id"] + "/status/" + x["id"]
            embUrlReq = requests.get(urlReq,verify=False)
            embUrl = embUrlReq.json()

            #Storing embedded links in a list
            embDict.append(embUrl["html"].replace("\n",""))
            i += 1
        
        print(embDict)
        
        return render_template('results.html', rDict = embDict)

    
    
    return render_template('index.html')
        
