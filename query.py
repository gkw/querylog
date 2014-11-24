
#!/usr/bin/env python
import sys, random
from pprint import pprint
from datetime import datetime 

from random import randrange
from datetime import timedelta
import pymongo


class IPv4:
  def __init__(self):
    self.digits = [0,0,0,0]

  def set(self, d):
    self.digits = d

  def hexpad(self, num):
    h = str(hex(num))[2:6]
    if len(h) == 1:
      return "0" + h
    else:
      return h

  def num2hex(self):
    d = self.digits
    return [self.hexpad(d[0]),self.hexpad(d[1]),self.hexpad(d[2]),self.hexpad(d[3])]

  @staticmethod
  def char2ip(d):
    return str(int(d[0],16)) + "." + \
           str(int(d[1],16)) + "." + \
           str(int(d[2],16)) + "." + \
           str(int(d[3],16))
  
#python2.7 is used to run this script

def query(params):

  pprint (params)

  conn = pymongo.MongoClient()
  db = conn.endgame.conding_GenkiKuroda
  
  results = db.find({'visited_at':{'$gt':params['from']},
                     'visited_at':{'$lt':params['to']}},
                    {'_id':0,'ipv4':1,'visited_at':1}).sort('visited_at', 1)

  #make sure index is being used...
  #pprint(db.find({'visited_at':{'$gt':params['from']},
  #                'visited_at':{'$lt':params['to']}}}.explain()

  try:
    last_date = None
    ipv4s = set([])
    ip_count = 0

    for x in results:
      visited_at = x['visited_at']
      
      #reset ipv4s for new day
      if last_date != None:
        if last_date.year  != visited_at.year or   \
           last_date.month != visited_at.month or \
           last_date.day   != visited_at.day:
          #print ipv4s
          ip_count = ip_count + len(ipv4s)
          ipv4s = set([])
      last_date = visited_at
      ipv4s.add("".join(x['ipv4']))

      print ("%s %s") % (visited_at, IPv4.char2ip(x['ipv4']))
    print ("%d hits (%d unique hits)" % (results.count(),  ip_count+len(ipv4s)))
  except Exception as ex01:
    print ex01

def random_date(start, end):
    """
    Source: http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)

    return start + timedelta(seconds=random_second)

def init(count):

  conn = pymongo.MongoClient()
  db = conn.endgame.conding_GenkiKuroda.drop()
  db = conn.endgame.conding_GenkiKuroda

  ipaddr = IPv4()
  for x in xrange(count):
    for i in range(4):
      try:
        ipaddr.digits[i] = random.randint(0, 255)
      except Exception as ex01:
        print ex01

    d1 = datetime.strptime('1/1/2014  1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('11/1/2014 3:50 PM', '%m/%d/%Y %I:%M %p')

    log = {'ipv4':ipaddr.num2hex(),
           'visited_at': random_date(d1, d2),
          #'url': 'http://example.org/products/' + str(randrange(count)) + '.html'
          }
    db.insert(log)
    
    #intentinally making some duplicate IP addresses.
    log = {'ipv4':ipaddr.num2hex(),
           'visited_at': random_date(d1, d2),
          #'url': 'http://example.org/products/' + str(randrange(count)) + '.html'
          }
    db.insert(log)

  #create indexes
  db.ensure_index('visited_at', 1)
  db.ensure_index('visited_at', -1)
  db.ensure_index('ipv4', 1)
  db.ensure_index('ipv4', -1)

if __name__ == "__main__":
  try:
    init(5000)
  except Exception as ex01:
    print ex01, "cannot be initialized..."
    quit()

  try:
    fromDate = datetime(2014, 1, 1, 0, 0, 0, 0)
    toDate   = datetime(2014, 4, 1, 0, 0, 0, 0)
    query({'from':fromDate,'to':toDate})
  except:
    print "something wrong happened..."
    quit()
