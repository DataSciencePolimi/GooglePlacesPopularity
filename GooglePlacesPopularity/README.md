# google-maps
Python codes and Mongo DB integration to make Google Maps API calls, popular times enrichment and store in a NoSQL DB.
Flow
1. Run retrieve_pois_and_store.py to call Google APIs and store into MongoDB
2. Run enrich_popular_times.py to scrap popular times bar plots by using the attached Python library populartimes-master.
