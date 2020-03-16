import requests
import json


########################################################
# START MONGO instance on your machine
# call Google APIs and store into MongoDB
########################################################


APIKEY = 'your_api_key'

from pymongo import MongoClient


def retrievePoiAndInsertToMongo(url, token=None):
   try:
      print(url)
      if not token is None:
         token = "&pagetoken="+token
         url += token

      response = requests.get(url)
      res = json.loads(response.text)

      #print("here results ---->>> ", len(res["results"]))

      if ("results" in res):
         results_paginated = res["results"]
         for result in results_paginated:
            #print(result)

            if not ("place_id" in result):
               print("place_id should exist in returning results, skipping this POI record")
               continue;

            place_id = str(result["place_id"])
            if (db.pois.find({"place_id": place_id}).count() == 0):
               db.pois.insert(result)
               print("insertion to mongo is success! id:" + str(place_id))
            else:
               print("already existing place id:" + str(place_id))


      pagetoken = res.get("next_page_token",None)

      print("here -->> ", pagetoken)
   except Exception as ex:
      print(ex)
   return pagetoken


if __name__ == "__main__" :

   client = MongoClient('localhost:27017')
   db = client.GoogleMaps

   pagetoken = None

   print("started")
   cnt = 0
   MAX_LIMIT = 1000

   isEnded = False

   list_of_pois = ["amusement park","atm","bakery","bank","bar","beauty salon","book store","bus station","cafe","car dealer","car rental","car repair","car wash","casino","cemetery","church","city hall","clothing store","convenience store","courthouse","department store","electronics store","embassy","furniture store","gas station","gym","hair care","hardware store","home goods store","insurance_agency", "jewelry_store", "laundry", "lawyer", "library", "liquor_store", "local_government_office", "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office", "real_estate_agency", "restaurant", "roofing_contractor", "rv_park", "school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "supermarket", "synagogue", "taxi_stand", "train_station", "transit_station", "travel_agency", "veterinary_care", "zoo"]

   next_page_token = None
   for poi in list_of_pois:
      poi_cnt = 0
      url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + poi + "+in+Istanbul&key=" + APIKEY
      next_page_token = retrievePoiAndInsertToMongo(url, next_page_token)
      poi_cnt +=1
      cnt += 1
      while (next_page_token is not None):
         next_page_token = retrievePoiAndInsertToMongo(url, next_page_token)
         poi_cnt +=1
         cnt += 1
      if next_page_token is None:
         print("page token is empty, breaking the operation")
         print(" done: " + poi + " with " + str(poi_cnt))


   print("completed after " + str(cnt) + " api calls")

