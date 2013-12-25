#!/bin/python
###################################################################################
# Profile utilities for all other scripts or python projects
#
# Uses 
# 
# Created by smtechnocrat$gmail.com
#
###################################################################################
import os, time, logging, logging.config
import cProfile

#Logging
logging.basicConfig(filename='profiler.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logger = logging.getLogger('Profiler')

# a decorator for timing other functions
def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        logger.info(f.__name__ + ' took : ' + str(end - start) + ' ms time')
        return result

    return f_timer
      
def profilefunc(f):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = f(*args,**kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func

def get_number():
  for x in xrange(500000):
      yield x

@profilefunc
def test_func():
    for x in get_number():
        res = x ^ x
    return 'some result'

# A cutom profiler using basic time functions 
class myprofiler():

    def __init__(self,name='myprofiler'):
        self.name = name
        self.start = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start    

    def checkpoint(self,name='myprofiler'):
        logger.info('{timer} {checkpoint} took {elapsed} seconds.'.format(
                      timer = self.name,
                      checkpoint = name,
                      elapsed = self.elapsed).strip())
        
    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        self.checkpoint('finished.')
        pass



if __name__ == '__main__':
    res = test_func()
