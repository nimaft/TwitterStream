import requests


#Holds query string
query="vote"

#Requesting tweets from Streaming API, returns 10 tweets
bt = 'AAAAAAAAAAAAAAAAAAAAAAONJQEAAAAA1wHsP7ozvwm0FPeVGgzqODg0Dhs%3DppJgXkaWKv3w2knqe7FSF2GquoVHzW4mTtPYYZotzeibD5OdSk'

headers = {'Authorization': 'Bearer '+bt}
response = requests.get("https://api.twitter.com/2/tweets/search/recent?query=nyc&tweet.fields=author_id",headers=headers)

#Converting response to dictionary
jsonResp = response.json()

#Extracting data from dictionary (data would be a list of dictionaries)
data = jsonResp["data"]


#Looping through data dictionaries to get author_id and id
#Using author_id and id to get embeded links for tweets
i=1
embDict = {}
for x in data:
    urlReq = "https://publish.twitter.com/oembed?url=https://twitter.com/" + x["author_id"] + "/status/" + x["id"]
    embUrlReq = requests.get(urlReq,verify=False)
    embUrl = embUrlReq.json()

    #Storing embedded links in a dictionary
    embDict["tweet"+str(i)] = embUrl["html"].replace("\n","")
    i += 1




