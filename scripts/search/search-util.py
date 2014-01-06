#!/bin/python

###################################################################################
# A Python script to look for patterns in a file or text.
#
# use docopt for arguments parsing
# Currently uses a logging. 
#
# TODO pass logging enabled and filename as a switch

# Created by smtechnocrat$gmail.com
#
###################################################################################
"""Usage: search-util.py [-vifd] [INPUT_TXT] [INPUT_FILE] [OUTPUT_DIR] ...
    
   An utility script to look for common patterns in a file or text. Supports the following
   lookups
     1) Date format lookups
     2) Links - href
     3) emails
   
   Arguments:
       INPUT_TXT     optional
       INPUT_FILE    optional fully qualified path of the input file to search 
       OUTPUT_DIR    optional directory path, default is HOME dir for search results to be written.

   Options:
      -h     --help
      -v     verbose mode
      -i     input text
      -f     fully qualified name of the input file to search
      -d     fully qualified path of the directory where the output will be dumped.

"""

import os
import time
import logging, logging.config

from docopt import docopt

#Logging
logging.basicConfig(filename='search-utils.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logger = logging.getLogger('searchutilslog')


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
      

def parseArguments(args=None):
   input_file = None

   if len(args['INPUT_TXT']) == 0:
      if len(args['INPUT_FILE']) == 0:
         logger.info("No input provided. Please provide text string or file name to search for.");
      else:
         input_file = args['INPUT_FILE']
   else:
     input_txt = args['INPUT_TXT']
   return input_txt, input_file

#Utility class using regular expressions to search for a pattern
import re

class RegUtil:
   def __init__(self, txt=None):
	self.inputtxt = txt
  
   def get_dates(input_txt):
	searchtxt = input_txt or self.inputtxt
        month_regex = ur'(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.  \
                           ?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)'

        day_regex = ur'(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?'
        date_regex = month_regex + day_regex
        print date_regex
        return re.findall(month_regex + day_regex, 'hello fred jan frfrfrf January, feb, 12-01-2011, monday',re.IGNORECASE)






   
#-------------End of class Regutil --------------------------------
if __name__ == '__main__':
    logger.debug('Starting search-utils script.')
    arguments = docopt(__doc__)

    inputtxt, inputfile = parseArguments(arguments)
    print inputtxt
    print inputfile
    #check to see if out directory path was provided 
    #if not, use HOME directory
    if len(arguments['OUTPUT_DIR']) == 0:
        outputdir = DEFAULT_FILE_DIR
    else:
        outputdir = arguments['OUTPUT_DIR'][0]

    logger.info("Writing to the following directory: {0}".format(outputdir))
    
    regutil = RegUtil("Hello today is the first day of Jan.")
    print regutil.get_dates()
   

    
#import json
#print json.dumps(stories, indent=1)
