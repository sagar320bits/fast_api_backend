import pymongo
import json
from dotenv import load_dotenv
import os
load_dotenv()

client=pymongo.MongoClient(os.getenv("uri"))
db=client["courses"]
collection=db["courses"]

with open("courses.json","r") as f:
    courses=json.load(f)
collection.create_index("name")
print(collection.create_index("name"))

for course in courses:
    course["rating"]={'total':0,'count':0}
    print(course["rating"])

for course in courses:
    for chapter in course["chapters"]:
        chapter["rating"]={'total':0,'count':0}
for course in courses:
    collection.insert_one(course)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
client.close()

