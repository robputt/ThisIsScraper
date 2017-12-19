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

* Host capable of running Python 3
* Internet connection to pull articles

Tested with the following:

* Debian 8
* Python 3.4 (from OS packages)

## Installation


