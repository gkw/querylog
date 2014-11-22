
#!/usr/bin/env python
import sys, random
from pprint import pprint
from datetime import datetime 

from random import randrange
from datetime import timedelta
import pymongo

#python2.7 is used to run this script

def query(params):

  pprint (params)

  conn = pymongo.MongoClient()
  db = conn.endgame.conding_GenkiKuroda
  
  results = db.find({'visited_at':{'$gt':params['from']},
                     'visited_at':{'$lt':params['to']}},
                    {'_id':0,'ipv4':1,'visited_at':1,'url':1}).sort('visited_at', 1)

  #make sure index is being used...
  #pprint(db.find({'visited_at':{'$gt':params['from']},
  #                'visited_at':{'$lt':params['to']}}}.explain()

  for x in results:
    visited_at = x['visited_at']
    print ("%s %s %s") % (visited_at, d2ip(x['ipv4']), x['url'])
  print ("%d hits" % results.count())

def random_date(start, end):
    """
    Source: http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)

    return start + timedelta(seconds=random_second)

def hexpad(num):
  h = str(hex(num))[2:6]
  if len(h) == 1:
    return "0" + h
  else:
    return h

def num2hex(d):
  return [hexpad(d[0]),hexpad(d[1]),hexpad(d[2]),hexpad(d[3])]

def d2ip(d):
  return str(int(d[0],16)) + "." + \
         str(int(d[1],16)) + "." + \
         str(int(d[2],16)) + "." + \
         str(int(d[3],16))

def init(count):

  conn = pymongo.MongoClient()
  db = conn.endgame.conding_GenkiKuroda.drop()
  db = conn.endgame.conding_GenkiKuroda

  ipaddr = [0,0,0,0]
  for x in xrange(count):
    for i in range(4):
      ipaddr[i] = random.randint(0, 255)

    d1 = datetime.strptime('1/1/2014  1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('11/1/2014 3:50 PM', '%m/%d/%Y %I:%M %p')

    log = {'ipv4':num2hex(ipaddr),
           'visited_at': random_date(d1, d2),
           'url': 'http://example.org/products/' + str(randrange(count)) + '.html'}
    db.insert(log)

  #create indexes
  db.ensure_index('visited_at', 1)
  db.ensure_index('visited_at', -1)
  db.ensure_index('ipv4', 1)
  db.ensure_index('ipv4', -1)

if __name__ == "__main__":
  try:
    init(1000)
  except:
    print "cannot be initialized..."
    quit()

  try:
    fromDate = datetime(2014, 1, 1, 0, 0, 0, 0)
    toDate   = datetime(2014, 4, 1, 0, 0, 0, 0)
    query({'from':fromDate,'to':toDate})
  except:
    print "something wrong happened..."
    quit()
