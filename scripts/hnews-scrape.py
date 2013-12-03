#!/bin/python

###################################################################################
# A Python script to extract Hacker News headlines and links and save the extract
# in a file.
#
# Uses BeautifulSoup to scrape the web page.
# use docopt for arguments parsing
# Created by smtechnocrat$gmail.com
#
###################################################################################
"""Usage: hnews-scrape.py [-vd] [OUTPUT_DIR] ...
    
   Scrape hacker news front page and dump all headlines and its corresponding links 
   to the output file.
   
   Arguments:
       OUTPUT_DIR    optional directory path, default is HOME dir

   Options:
      -h --help
      -v     verbose mode
      -d     fully qualified path of the directory where the output will be dumped.

"""

import os, time, logging, logging.config
import requests
import time

from BeautifulSoup import BeautifulSoup
from docopt import docopt

#Logging
logging.basicConfig(filename='testscript.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logger = logging.getLogger('hackerNewsscraper')


#default directory for saving downloaded files 
DEFAULT_FILE_DIR= os.environ['HOME']

# a decorator for timing other functions
def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        logger.info(f.__name__ + ' took : ' + str(end - start) + ' ms time')
        return result

    return f_timer
      
@timefunc
def createSoup(url):
    logger = logging.getLogger(__name__)
    #url for Hacker news
    #hackerurl = "https://news.ycombinator.com"
    #download zipped contents
    headers={ "User-Agent": "HN scraper / Contact me:", "Accept-Encoding": "gzip"}
    #make a single request for the webpage
    r = requests.get(url, headers=headers)
    #convert the plaintext html into beautifulsoup DOM
    soup = BeautifulSoup(''.join(r.text))
    return soup

@timefunc
def parsesoup(soup):
    #parse through the outer and inner tables and then find the rows
    outer_table = soup.find("table")
    inner_table = outer_table.findAll("table")[1]
    rows = inner_table.findAll('tr')

    #create a list of dictionary with the following keys: 
    #title, link and current position of each story
    stories=[]
    rows_per_story=3
    for row_num in range(0, len(rows)-rows_per_story, rows_per_story):
        #grab the first and second rows and create an array of their cells 
        story_pieces = rows[row_num].findAll('td')
        meta_pieces  = rows[row_num + 1].findAll('td')
        #create our own story dictionary
        story = { 
              "current_position": story_pieces[0].string, 
              "link": story_pieces[2].find('a')['href'], 
              "title": story_pieces[2].find('a').string 
            }
        stories.append(story)
        try:
            story["posted_by"] = meta_pieces[1].findAll("a")[0].string
        except IndexError:
            continue #this is a job posting, not a story 

    return stories


def writecontents(contents, filename):
    linenum=1
    with open(filename, 'w') as f:
        for item in contents:
            f.write('{0} {1}\n'.format(linenum, item['title'].encode('utf-8'))) #use new print format instead of %
            f.write('{0}\n\n'.format(item['link'].encode('utf-8')))
            linenum += 1

if __name__ == '__main__':
    logger.debug('Starting hacker scraper script.')
    arguments = docopt(__doc__)
    #check to see if out directory path was provided 
    #if not, use HOME directory
    if len(arguments['OUTPUT_DIR']) == 0:
        outputdir = DEFAULT_FILE_DIR
    else:
        outputdir = arguments['OUTPUT_DIR'][0]

    logger.info("Writing to the following directory: {0}".format(outputdir))

    filename = outputdir+ os.sep + 'hnews-' + time.strftime("%d-%m-%Y:%H-%M") + '.txt'
    hackerurl = "https://news.ycombinator.com"
    hnewssoup = createSoup(hackerurl)
    contents = parsesoup(hnewssoup)
    writecontents(contents,filename)
    


 
#import json
#print json.dumps(stories, indent=1)
