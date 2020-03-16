import googlemaps
import requests
import json
import requests
import json
import time
from time import gmtime, strftime


import populartimes

########################################################
# Scraping Google Maps Popular Times Bar Plot for a given Place ID
########################################################

APIKEY = 'your api key'

from pymongo import MongoClient


if __name__ == "__main__" :

   client = MongoClient('localhost:27017')
   db = client.GoogleMaps

   pagetoken = None

   cnt = 0
   MAX_LIMIT = 100

   for res in db.pois.find({"density_crawl_time": {"$exists": False}}):
      if res is None:
         print("end of pois cursor")
         break

      place_id = res["place_id"]

      print("before sending, mongo record:")
      print(res)

      new_res = populartimes.get_id(APIKEY, place_id)

      current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

      if "international_phone_number" in new_res:
         international_phone_number = new_res["international_phone_number"]
         db.pois.update({"place_id": place_id}, {"$set": {"int_phone": international_phone_number}})

      if "populartimes" in new_res:
         density_week = new_res["populartimes"]
         db.pois.update({"place_id": place_id}, {"$set": {"density": density_week, "density_crawl_time": current_time}})

      db.pois.update({"place_id": place_id}, {"$set": {"density_crawl_time": current_time}})

      print("after sending, obtained res:")
      print(new_res)

      cnt += 1

   print("completed after " + str(cnt) + " api calls")

