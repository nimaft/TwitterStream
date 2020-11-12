# TwitterStream :bird:
A simple web server powered by [Flask](https://flask.palletsprojects.com/), created to process and display 10 latest tweets based on user query.
Check out the app @ http://twitter.nimadoes.xyz/

## Overview
* User enters a search term.
* Flask processes the request and extracts the query term.
* It uses Twitter API v2 [Filtered Stream](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/introduction) endpoint to filter the complete stream of real-time public Tweets and stores the response.
* Twitter's response is parsed and *author_id* and *id* are extracted from it.
* Using the extracted values, webserver submits requests to Twitter [oEmbed API](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-oembed) to receive the URL of the Tweet to be embedded.
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
  * index page receives accepts both GET and POST methods:
    * GET: renders the template for index.html
    * POST: user has searched for a term > redirects to /results/<term> page
  * results page (when receiving a search query)
    * GET
      * confirms the search term is not empty
      * converts search term to URL friendly term (e.g. converts #NYC to %23NYC)
      * sends the request to Twitter and stores the response
      * converts the response from JSON to Python dictionary and stores data in a list
      * loops through list values, extracts author_id and id, creates a string and submit it to oEmbed API to get embed URL
      * stores the embed URLs in a list, passes search term, results list and renders results.html
    * POST: should not accept receive requests, in case it does, renders index.html
 
 
 * Templates: used by Flask to render dynamic webpages. Base template holds links to stylesheets and scripts.
 
 
 #### At this point you might ask: what is the point? I created this little web app to use with a CI/CD pipeline on Amazon AWS. Let's review how everything comes together with AWS.


## CI/CD Pipeline with AWS :cloud:
![design](/TwiApp/static/TwiApp.png)
Following services were used in creating the pipeline on AWS:
* **AWS Identity and Access Management (IAM):** defining permissions for ECS and containers.
* **Amazon Virtual Private Cloud (VPC):** where to run containers and load balancer.
* **CodeBuild:** 
  * Pulls the source code for Flask app from this repo.
  * Reads buildspec.yaml and builds an image.
  * Uploads the image to Docker Hub :whale:.
  * Creates imagedefinitions.json [used by CodePipeline]
* **CodePipeline:**
  * Source stage: monitors main branch of this repository, upon detecting an update, triggers build stage.
  * Build stage: triggers the build project defined in CodeBuild. Upon successful build, deploy stage is triggered.
  * Deploy stage: uses imagedefinition.json, passes it on to ECS and runs a Fargate task.
* **AWS Secrets Manager:** provides Docker hub credentials to CodeBuild and Elastic Container Service.
* **AWS Systems Manager > Parameter Store:** provides Twitter bearer key to ECS task definition to be used as an environmental variable for the container.
* **Elastic Container Service (ECS):**
  * Contains a task definition directing AWS how to deploy Docker images.
    * Container port mapping and environmental variables are set withing task definition.
  * An ECS service Contains the deployment settings (which Task Definition to use), auto scaling policy, and load balancer settings. (Similar to Kubernetes Deployment)
  * I used **Fargate** as the compute engine for the containers.
* **Application Load Balancer:**
  * Helps having consistent IP for your application.
  * When running multiple containers (tasks) within an ECS service, it helps distributing the traffic.
  * ECS automatically registers and deregister tasks with ALB's target group when tasks are created or deleted.
* **Route 53:** I used route 53 to set a custom domain for ALB.
 
#### What’s next?
:mage_man: Creating a CloudFormation template to easily provision services for this project.
