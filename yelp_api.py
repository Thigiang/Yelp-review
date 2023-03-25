import requests
import json
import csv
import time
"""
Get business's info. to obtain business id
"""
def business(offset, location):
    url="https://api.yelp.com/v3/businesses/search"
    api_key="Aefw4e0ZaUbkZruvRo7XWccAcnDK6rV4xQoZZdVHkGVoKrBGSz2p4wsZb2yZJQU2O7UoowxU1BT-wP3t2QXd48v6VSbc6xp30E5lTwsOVWKq1buQCCK9_hQBUYcaZHYx"
    headers={"accept":"application/json","Authorization": "Bearer "+api_key}
    params={"term":"restaurant","location":location, "limit":"25","offset": offset}
    businesses=requests.get(url, headers=headers, params=params)
    if not businesses.ok:
        print("error")
        print(businesses.text)
    return businesses.json()

def review(id):
    url = "https://api.yelp.com/v3/businesses/"
    end_point="/reviews"
    api_key="Aefw4e0ZaUbkZruvRo7XWccAcnDK6rV4xQoZZdVHkGVoKrBGSz2p4wsZb2yZJQU2O7UoowxU1BT-wP3t2QXd48v6VSbc6xp30E5lTwsOVWKq1buQCCK9_hQBUYcaZHYx"
    id=id
    headers={
        "accept": "application/json",
        "Authorization": "Bearer "+api_key
    }
    params={"limit": "10"}
    reviews=requests.get(url+id+end_point, headers=headers, params=params)
    if not reviews.ok:
        # print("Error")
        return reviews.json()
        pass
    return reviews.json()
# location=[
#     "San Jose City", "San Francisco City","Mountain View City",
#     "Fremont City", "Palo Alto City","Oakland City", "Berkeley City",
#     "San Mateo City", "Redwood City","Sunnyvale City",
#     "Pleasanton City","Hayward City","Dublin City"
# ]
location=["Hayward City"]
print(location)
# stt=0
stt=7456
for city in location:
    offset_range=[0,100,400,700,1000]
    All_bus_id=[]
    for i in range(len(offset_range)-1):
        offset=offset_range[i]
        business_id=[]
        while offset < offset_range[i+1]:
            busi_subset=business(offset, city)
            for res in busi_subset['businesses']:
                business_id.append(res['id'])
            offset += 25
        All_bus_id.append(business_id)
    for j in range(len(All_bus_id)):
        content=[]
        business_id=All_bus_id[j]
        for idx in range(len(business_id)):
            subre=review(business_id[idx])
            if list(subre.keys())[0]!="reviews":
                pass
            else:
                for rev in subre["reviews"]:
                    stt+=1
                    content.append([stt,rev["text"],rev["rating"]])
        # if j == 0 and city == location[0]:
        #     with open("big_data.csv",'w') as file:
        #         writer=csv.writer(file)
        #         writer.writerows(content)
        # else:
        #     with open("big_data.csv",'a') as file:
        #         writer=csv.writer(file)
        #         writer.writerows(content)
        with open("big_data.csv",'a') as file:
            writer=csv.writer(file)
            writer.writerows(content)
        time.sleep(30)
    time.sleep(45)


# print(len(All_bus_id[0]),len(All_bus_id[1]),len(All_bus_id[2]),len(All_bus_id[3]))
# offset=400
# business_id=[]
# while offset < 700:
#     busi_subset=business(offset)
#     for res in busi_subset['businesses']:
#         business_id.append(res['id'])
#     offset += 25
# print(len(business_id))




# test=review(business_id[0])
# content=[]
# for rev in test["reviews"]:
#     content.append([rev["text"],rev["rating"]])
# print(content)


# stt=2072
# All_content=[]
# for i in range(1):
#     content=[]
#     business_id=All_bus_id[3]
#     for idx in range(len(business_id)):
#         subre=review(business_id[idx])
#         if list(subre.keys())[0]!="reviews":
#             pass
#         else:
#             for rev in subre["reviews"]:
#                 stt+=1
#                 content.append([stt,rev["text"],rev["rating"]])
                # All_content.append(content)

# print(len(content))
# with open("data_Fremont.csv",'w') as file:
#     writer=csv.writer(file)
#     writer.writerows(content)
# with open("data_Fremont.csv",'a') as file:
#     writer=csv.writer(file)
#     writer.writerows(content)





