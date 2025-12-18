import contextlib
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = MongoClient(os.getenv("uri"))
db = client["courses"]

@app.get('/courses')
def get_courses(sort_by: str = 'date', domain: str = None):
    # Iterate over all courses to aggregate chapter ratings into the course rating
    # Note: This is inefficient for large datasets but kept to preserve logic
    for course in db.courses.find():
        total = 0
        count = 0
        if "chapters" in course:
            for chapter in course["chapters"]:
                with contextlib.suppress(KeyError):
                    total += chapter["rating"]["total"]
                    count += chapter["rating"]["count"]
                    
        
        db.courses.update_one(
            {"_id": course["_id"]},
            {"$set": {"rating": {"total": total, "count": count}}}
        )
    
    # Determine sort field and order
    if sort_by == 'date':
        sort_field = 'date'
        sort_order = -1

    elif sort_by == 'rating':
        sort_field = 'rating.total'
        sort_order = -1
    
    else:
        sort_field = 'name'
        sort_order = 1

    # Build query
    query = {}
    if domain:
        query["domain"] = domain

    # Fetch and return sorted/filtered courses

    courses = db.courses.find(query, {'name': 1, "date": 1, "description": 1, "domain": 1, "chapters": 1, "rating": 1}).sort(sort_field, sort_order)
    
    results = []
    for course in courses:
        course["_id"] = str(course["_id"])
        results.append(course)

    return results