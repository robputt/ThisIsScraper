# ThisIsScraper
My local new website (www.thisisplymouth.co.uk) offers a terrible viewing experience and lots of ads and a nasty adblocker detector which masks any content if you have such a plugin enabled... This is my attempt to extract the articles into plain text for easier reading... 

This script only works for the website above at the moment but it could probably be adapted fairly easily for any newspaper using Trinity Mirror's content management system.

## What does this thing do? 

The software provides 2 components written in Python, the scraper which runs on cron periodically to pull any new articles, and the viewer which hosts a small Flask app to display the pulled content.

The original site:
![original site](https://github.com/robputt796/ThisIsScraper/blob/master/docs/thisisads.jpg?raw=true)

As you can see the original site has alot of advertisements as highlighted in the green bounding boxes and dedicated very little screen space to the actual content... Here is the same article viewed in the ThisIsScraper viewer, no ads and no clutter, just the content.

ThisIsScraper site:
![ThisIsScraper site](https://github.com/robputt796/ThisIsScraper/blob/master/docs/thisisscraper.jpg?raw=true)

## Demo

You can view a demo of ThisIsScraper running here - http://95.138.162.109/

## Limitations

* This thing looks really ugly, but functional.
* Only tested against ThisIsPlymouth.co.uk but probably works for other newspapers with ThisIs websites. 
* Currently doesn't pull any images or video content related to the article.

Feel free to raise a PR to fix any of the limitations above :-).

## Requirements

* Host capable of running Python 3 (probably works with Python 2.7 as well but I haven't tested this)
* Internet connection to pull articles

## Installation

Here is how I got ThisIsScraper running on Debian 8 on the demo box, if you are using a different operating system adjust as required.

Clone the git repo...

```
git clone https://github.com/robputt796/ThisIsScraper.git
```

Install the Python pre-requisites and create a virtualenv.

```
apt-get install mysql-server apache2 libapache2-mod-proxy-html libxml2-dev python3 python3-dev python3-setuptools
easy_install3 pip
pip3 install virtualenv
virtualenv /opt/thisisscraper
source /opt/thisisscraper/bin/activate
cd ThisIsScraper
pip install -r requirements.txt
```

Create a new empty schema in your MySQL DB, don't worry the tables will be populated the first time the scraper cron runs.

```
mysql
CREATE DATABASE thisisscraper;
```

Create the config.py file and update as required.

```
cp this_is_scraper/config.py.sample this_is_scraper/config.py
vi this_is_scraper/config.py
```

Install ThisIsScraper to your virtualenv (each time you update the config you'll need todo this, sorry I should have used some configfile parsing thing really!).

```
python setup.py install
```

Add the scraper script to cron...

```
mkdir /var/log/thisisscraper
crontab -e
```

Something like this should do the trick...

```
*/5 * * * * /opt/thisisscraper/bin/python /home/user/ThisIsScraper/this_is_scraper/scraper.py > /var/log/thisisscraper/`date +\%Y\%m\%d\%H\%M\%S`-cron.log 2>&1
```

Carry on with the installation, but at the end check back in on the log directory to make sure that the scraper has pulled the articles as required...

Create a systemd file to run the Flask app...

```
vi /lib/systemd/system/thisisviewer.service
```

Here is what mine looks like, adjust as needed...

```
[Unit]
Description=ThisIsScraperViewer
After=network.target

[Service]
User=user
ExecStart=/opt/thisisscraper/bin/python /home/user/ThisIsScraper/this_is_scraper/viewer.py
WorkingDirectory=/home/user/ThisIsScraper/
Restart=on-failure
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Now do a reload and try and start the service, if all is succesful a curl to localhost on port 5000 should send back some HTML...

```
systemctl daemon-reload
systemctl start thisisviewer.service
curl http://localhost:5000
```

If you get HTML back set the service to start at boot...

```
systemctl enable thisisviewer.service
```

Now we can configure Apache to reverse proxy the Flask app so we can access the articles on port 80 and from another host. The Flask app should only listen on 127.0.0.1.

```
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_ajp
a2enmod rewrite
a2enmod deflate
a2enmod headers
a2enmod proxy_balancer
a2enmod proxy_connect
a2enmod proxy_html
vi /etc/apache2/sites-enabled/000-default.conf
```

Update the default virtualhost to reverse proxy to the Flask app, of course if you have more than 1 virtual host on the box your configs will look different.

```
<VirtualHost *>
    ProxyPreserveHost On

    # Servers to proxy the connection, or;
    # List of application servers:
    # Usage:
    # ProxyPass / http://[IP Addr.]:[port]/
    # ProxyPassReverse / http://[IP Addr.]:[port]/
    # Example: 
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    ServerName thisisscraper.robertputt.co.uk 
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

Restart Apache...

```
service apache2 restart
```

Try visiting your webserver in your browser from another host. If all has gone well and the scraper cron has run for the first time you should see a nice plain text article listing.
