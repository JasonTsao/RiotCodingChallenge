RIOTCODINGCHALLENGE (MOBILE MATCH VIEWER)
=========================================

The idea of this app is to be a mobile website that makes it easy to see some 
information regarding the most recent match that you have been in. Unfortunately 
this only regards to ranked players since of the Riot philosophy I actually just read about here

https://developer.riotgames.com/discussion/riot-games-api/show/XvQsMryF

Only found this out after I finished writing this thing but oh well. 


CODE BASE
=========
https://github.com/JasonTsao/RiotCodingChallenge

USAGE
=====
Go to http://54.186.40.204 on your mobile phone

Type in a ranked summoner name in the input box and press enter or click login

Wait for a little and the page should load with player data from your most recent match
Swipe left and right on the image to see stats of differnt players on each team. Click on 
the buttons on the top to swap between team one and team two.

That's it!

Some of the win and ranked data might not load on the first call because of the limit on
api calls to Riot but I'll get to that.


INSTALLATION INSTRUCTIONS (Ubuntu)
==================================
Make sure python version is 2.7.6

Prequisite applications
------------------------
sudo apt-get install git
sudo apt-get install redis-server
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install virtualenv

Setup Virtual Environment
---------------------------
virtualenv venv
source venv/bin/activate


Applications needed for running on a live server(AWS)
----------------------------------------------------
sudo apt-get install nginx
sudo apt-get install gunicorn

sudo nano /etc/nginx/sites-enabled/default
sudo service nginx restart
gunicorn -c gunicorn.conf.py RiotCodingChallenge.wsgi:application
python manage.py collectstatic


Pull the repository from git
-----------------------------
git clone https://github.com/JasonTsao/RiotCodingChallenge.git
cd RiotCodingChallenge

Installing necessary python libraries
-------------------------------------
sudo pip install -r requirements.txt


Setting up database
-------------------
python manage.py syncdb  (follow the instructions that come up and say yes to everything)
python manage.py migrate

if python manage.py syncdb didn't work try 
python2.7-dbg manage.py syncdb
python2.7-dbg manage.py migrate


Start Server
------------
python manage.py runserver

Start Redis
------------
redis-server


Fill in runes and masteries by calling RiotAPI
-----------------------------------------------
Go to browser and open a tab.

get runes
http://localhost:8000/riot/api/runes/get/all?region=na

get masteries
http://localhost:8000/riot/api/masteries/get/all?region=na

These are necessary to have beforehand for masteries since information about mastery type (Offense, Defense, Utility)is provided by 
	/api/lol/static-data/{region}/v1.2/mastery api endpoint
that isn't provided by calling 
	/api/lol/static-data/{region}/v1.2/mastery/{id} 



Your ready to go! Go to http://localhost:8000 and check it out!

http://localhost:8000/admin

Go to that link to see the admin page and sign in with the credentials you used when you ran
python manage.py syncdb

There you'll see a nice GUI for the database tables/models used and can watch it get filled up as you use the app! 


Technology Stack
================
Frontend
--------
	Javascript, jQuery
	HTML
	CSS
	idangerous swiper library
	meanmenu library


Backend
-------
	python (base language)
	Django (web framework)
	south (for database use in Django)
	redis (nosql cache layer for quicker response times later on)
	sqllite (relational database for more permanent data storage)

Server
------
	gunicorn (web server gateway interface)
	nginx (static file serving)


Server Host
-----------
	Amazon Web Service EC2



Improvements if I have more time
================================
Cache
-----
	write and improved cache layer (redis or even memcached) to speed up calls and reduce Riot API calls
	write a scheduler to update data that can go stale if constantly being pulled from cache


Reduce API Calls
----------------
	batching calls to reduce riot API calls as much as possible (get stats for comma separated list of summoner Ids)


User Experience
---------------
	have empty slide divs there and ready when page loads so page isn't empty on load
	have different system api calls for each summoner and different pieces of info( Masteries, Runes, basic data, ranked data, summoner images...etc)
		this is for speed improvements to user doesn't feel like they're waiting a long time for something to happen
	having a standard image does not exist image if  image doesn't exist on ddragon


Add More Relevant Data
----------------------
	create new pages for more detailed views of info
		detailed masteries
		detailed runes
		champions this summoner does well against
		champions this summoner doesn't do well against


Fix Team Two page glitch 
------------------------
	the first time logging in as a summoner the team two swiper sometimes doesn't work because I want 
	to hide it so only one team is shown at once but the thing can't be hidden before images are loaded
	otherwise the swiper library won't be able to get the sizing stuff correct
	

Make this work for non NA region
--------------------------------
	I only really made this work for NA. I'm sure if I tried other regions there'd be language problems and displaying
	things since I'm assuming everything can work as a string or unicode but not utf-8 and what not


Security
--------
	There's currently nothing stopping a random user from calling the apis and making things happen but for the purpose of a weekend 
	project I thought I'd let it slide

	turn DEBUG mode to False on the server cause that's no good if people can see the stack trace