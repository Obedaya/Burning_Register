from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
import numpy as np
from datetime import datetime

load_dotenv()

mongourl = os.getenv("MONGO_URL")

def insert(collection, document):
    try:
        col = db[collection]
        col.insert_one(document)
        print("Product inserted successfully.")
    except Exception as e:
        print(f"Error inserting product: {str(e)}")


def get(collection, document):
    col = db[collection]
    return col.find_one(document)


def delete(collection, id):
    col = db[collection]
    col.delete_one({"_id": ObjectId(id)})

def collection_exists(collection):
    return collection in db.list_collection_names()

def create_collection(collection):
    db.create_collection(collection)


import numpy as np

def edit_by_id(collection, id, update):
    # Convert numpy.int64 to int
    for key, value in update.items():
        if isinstance(value, np.int64):
            update[key] = int(value)
    col = db[collection]
    result = col.update_one({"_id": ObjectId(id)}, {"$set": update})
    print(f'Updated {result.modified_count} documents.')

def edit_by_name(collection, name, update):
    # Convert numpy.int64 to int
    for key, value in update.items():
        if isinstance(value, np.int64):
            update[key] = int(value)
    col = db[collection]
    result = col.update_one({"name": name}, {"$set": update})
    print(f'Updated {result.modified_count} documents.')

def edit_by_query(collection, query, update):
    # Convert numpy.int64 to int
    for key, value in update.items():
        if isinstance(value, np.int64):
            update[key] = int(value)
    col = db[collection]
    result = col.update_many(query, {"$set": update})
    print(f'Updated {result.modified_count} documents.')


def find_all(collection, query={}):
    col = db[collection]
    return col.find(query)

def find_by_name(collection, name):
    col = db[collection]
    return col.find_one({"name": name})

def group_by(collection, group_by):
    col = db[collection]
    result = col.aggregate([
        {
            "$group": {
                "_id": f"${group_by}",
                "items": {
                    "$push": "$$ROOT"
                }
            }
        }
    ])
    return list(result)

def replace(collection, id, document):
    col = db[collection]
    col.replace_one({"_id": ObjectId(id)}, document)

def checkout(productlist, isteam, total, movie):
    for product in productlist:
        previous = find_by_name("inventory", product["name"])
        if previous is None:
            raise Exception(f'Product {product["name"]} not found in database.')
        previous_amount = int(previous["amount"])
        edit_by_name("inventory", product["name"], {"amount": previous_amount - product["amount"] })
    checkout_history = {
        "timestamp": datetime.now(),
        "total": total,
        "isteam": isteam,
        "movie": movie,
        "cancellation": False,
        "products": productlist,
    }
    print(str(checkout_history))
    insert("history", checkout_history)




# Create a new client and connect to the server
client = MongoClient(mongourl)
db = client['BurningRegister']