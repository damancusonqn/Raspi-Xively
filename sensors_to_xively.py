#!/home/pi/xively_tutorial/.envs/venv/bin/python
##!/usr/bin/env python
 
import os
import xively
import subprocess
import time
import datetime
import requests
import sys
import logging
import onewire_readtemp
import dhtreader
# extract feed_id and api_key from environment variables
FEED_ID = os.environ["FEED_ID"]
API_KEY = os.environ["API_KEY"]
DEBUG = os.environ["DEBUG"] or false

logging.basicConfig(level=logging.DEBUG, filename='/home/pi/xively_tutorial/debug2.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# initialize api client
api = xively.XivelyAPIClient(API_KEY)

#initialize OneWire driver
onewire_readtemp.one_wire_init()

# initialize DHT driver
DHT11 = 11
DHT22 = 22
AM2302 = 22
dhtreader.init()

def read_DHT():
  dev_type = DHT11
  dhtpin = 24 
  logging.debug('calling dhtreader...')
  try:
    t,h = dhtreader.read(dev_type, dhtpin)
    #logging.debug('dhtreader: t: %s, h: %s',t,h)
  except Exception, e:
    logging.debug('Error in DHT driver: %s' % e)  
  if t and h:
     return (t,h)

 
# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed, channel):
  try:
    datastream = feed.datastreams.get(channel)
    #datastream = feed.datastreams.get("load_avg")
    if DEBUG:
      print "Found existing datastream (%s)" % channel
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream (%s)" % channel
    datastream = feed.datastreams.create(channel, tags=channel)
    return datastream
 
# main program entry point - runs continuously updating our datastream with the
# current 1 minute load average
def run():
  print "--Starting Reading Sensors and sending the datastreams to Xively..."
  logging.debug("Starting Sensor Reading & Xively Updating")
 
  feed = api.feeds.get(FEED_ID)
 
  datastream1 = get_datastream(feed, "DS1820_Temp")
  datastream1.max_value = 100
  datastream1.min_value = -15
  datastream2 = get_datastream(feed, "DHT11_Temp")
  datastream2.max_value = 100
  datastream2.min_value = -15
  datastream3 = get_datastream(feed, "DHT11_Hum")
  datastream3.max_value = 95
  datastream3.min_value = 5
 
  while True:

    temp1=temp2=hum = 0

    try:
      temp1 = onewire_readtemp.read_temp()
    except Exception as e:
      logging.debug('Error in 1-Wire: (check sensor connection)%s',e)
      print("Error in onewire: (check sensor connection) %s" % e)

    try:
        temp2, hum = read_DHT() #se puede hacer esto??
    except Exception as e:
        logging.debug('Error in DHT:(check sensor connection) %s' % e)
        print("Error in DHT:(check sensor connection) %s" % e)
 
    if DEBUG:
      if temp1!=0 or temp2!=0 or hum!=0:
        print "Updating Xively feed with readed values:"
        logging.debug("Updating Xively feed with readed values:")
      if temp1!=0:
        print "----- DS1820_Temp: %s" % temp1
        logging.debug("----- DS1820_Temp: %s" % temp1)
      if temp2!=0 or hum!=0:
        print "----- DHT11:_Temp: %s, Hum: %s" % (temp2, hum)
        logging.debug("----- DHT11:_Temp: %s, Hum: %s" % (temp2, hum)) 

    if temp1!=0:  
      datastream1.current_value = temp1
      datastream1.at = datetime.datetime.utcnow()
    if temp2!=0:
      datastream2.current_value = temp2
      datastream2.at = datetime.datetime.utcnow()
    if hum!=0:  
      datastream3.current_value = hum
      datastream3.at = datetime.datetime.utcnow()

    try:
      datastream1.update()
      datastream2.update()
      datastream3.update()
    except requests.HTTPError as e:
      print "HTTPError({0}): {1}".format(e.errno, e.strerror)
 
    logging.debug("Going to sleep for 10m")
    time.sleep(60) #Every 10 minutes !!!!ojo corregir a 600s!!!
 
run()
