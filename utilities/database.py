from pymongo import MongoClient


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


def remove(collection, document):
    col = db[collection]
    col.delete_one({"name": document["name"]})


def edit(collection, document):
    col = db[collection]
    col.update_one({"_id": document["_id"]}, {"$set": document})


# Create a new client and connect to the server
client = MongoClient(uri)
db = client['BurningRegister']