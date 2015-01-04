RiotCodingChallenge
===================
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install virtualenv

sudo apt-get install gunicorn

sudo apt-get install nginx
sudo nano /etc/nginx/sites-enabled/default

sudo service nginx restart

gunicorn -c gunicorn.conf.py RiotCodingChallenge.wsgi:application

python manage.py collectstatic

Improvements:
	- break up data for getting summoner data into separate api calls for better user experience
	- cache layer to speed up calls and reduce Riot API calls