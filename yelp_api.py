import requests
import json
import csv
import time

class Yelp:
    def __init__(self, location, api_key):
        self.__location=location
        self.__api_key=api_key
        self.__url="https://api.yelp.com/v3/"
    
    def get_business_per_loc(self, location):
        url=self.__url + "businesses/search"
        headers={"accept":"application/json","Authorization": "Bearer "+self.__api_key}
        offset_range=[i for i in range(0,1000, 50)]
        businesses=[]
        for offset in offset_range:
            params={"term":"restaurant","location":location, "limit":"50","offset": offset}
            business=requests.get(url, headers=headers, params=params)
            if not business.ok:
                print("error")
                print(business.text)
            res = business.json()["businesses"]
            businesses.extend(res)
        return businesses


    def get_buss_all_loc(self):
        all_buss=[]
        for city in self.__location:
            all_buss.extend(self.get_business_per_loc(city))
            time.sleep(1)
        return all_buss

    def get_all_buss_ids(self):
        all_bus_id=[]
        all_buss=self.get_buss_all_loc()
        for buss in all_buss:
            all_bus_id.append(buss["id"])
        return all_bus_id


    def get_review_for_buss(self,buss_id):
        url=self.__url +"businesses/"+buss_id+"/reviews"
        headers={"accept": "application/json",
            "Authorization": "Bearer "+self.__api_key}
        params={"limit": "3"}
        reviews=requests.get(url, headers=headers, params=params)
        if not reviews.ok:
            print("error",reviews.text)
            return []
        else:    
            content=[]
            result=reviews.json()
            if "reviews" in result:
                for res in result["reviews"]:
                    content.append((res["text"],res["rating"]))
            return content

    def get_all_reviews(self):
        all_bus_ids=self.get_all_buss_ids()
        all_reviews=[]
        for bus_id in all_bus_ids:
            all_reviews.extend(self.get_review_for_buss(bus_id))
        return all_reviews


"""
location contains most of the cities in Bay Area
"""
api_key="Aefw4e0ZaUbkZruvRo7XWccAcnDK6rV4xQoZZdVHkGVoKrBGSz2p4wsZb2yZJQU2O7UoowxU1BT-wP3t2QXd48v6VSbc6xp30E5lTwsOVWKq1buQCCK9_hQBUYcaZHYx"
# location=[
#     "San Jose City", "San Francisco City","Mountain View City",
#     "Fremont City", "Palo Alto City","Oakland City", "Berkeley City",
#     "San Mateo City", "Redwood City","Sunnyvale City",
#     "Pleasanton City","Hayward City","Dublin City"
# ]
class Save:
    def __init__(self,content,name):
        self.__content=content
        self.__name=name
    def save_as_csv_w(self):
        with open(self.__name,'w') as file:
            writer=csv.writer(file)
            writer.writerows(self.__content)
    def save_as_csv_a(self):
        with open(self.__name,'a') as file:
            writer=csv.writer(file)
            writer.writerows(self.__content)
location=["Sunnyvale City"]
yelp=Yelp(location, api_key)
reviews = yelp.get_all_reviews()
save_review=Save(reviews, name="Yelp_data.csv")
# save_review.save_as_csv_w()
save_review.save_as_csv_a()
