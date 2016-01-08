# Tweetification


from django.shortcuts import render

# Create your views here.

import tweepy
import time
import smtplib
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt



auth = tweepy.OAuthHandler('YOUR_KEY', 'YOUR_KEY_2')


auth.set_access_token('YOUR_TOKEN', 'YOUR_TOKEN_2')

api = tweepy.API(auth)

sender = "YOUR_EMAIL"
password = "YOUR_Password"


SUBJECT = "Tweet with keyword posted."

def send_email(message, receiver):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    new_msg = 'Subject: %s\n\n%s' % (SUBJECT, message)
    server.sendmail(sender, receiver, new_msg)
    server.quit()

    
def tweet_checker(keyword, receiver_address, posted_by):
	# we use a file that will store list of IDs of tweets it has already checked
	if not os.path.isfile("tweets_checked.txt"):  
	        tweets_checked = []
	        print "File not found"
                #we create a list of ids of tweets
	    

	## if the program has run before, it loads the list of ids of comments that have been encrypted 
	##    so as to not encrypt the same comment twice.
	        
	else:
	    with open("tweets_checked.txt", "r") as f:
	    	print "File found"
	        tweets_checked = f.read()   
	        tweets_checked = tweets_checked.split("\n")
	        tweets_checked = filter(None, tweets_checked)




	while True:
	    search_results = api.user_timeline(screen_name = posted_by, count = 5)
	    for tweet in search_results:
	    	print tweet.text
	        if keyword in tweet.text and tweet.id_str not in tweets_checked:
	         	send_email("Text: " + tweet.text + "\n" + "ID: " + tweet.id_str, receiver_address)				
	         	tweets_checked.append(tweet.id_str)
	         	with open ("tweets_checked.txt", "a") as f:
	         		f.write(tweet.id_str + "\n")
	        else:
	        	print "No tweet found w/ keyword"
	    time.sleep(5)
        
  #every controller, by default, has to take in at least one parameter.          
def home_controller(request):
	return render_to_response("home_page.html")
@csrf_exempt
def form_controller(request):
	keyword= request.POST["keyword"]
	posted_by= request.POST["posted_by"]
	receiver = request.POST["receiver"]
	tweet_checker(keyword, receiver, posted_by)
	return HttpResponse("Done!")


