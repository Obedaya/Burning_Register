from utilities import database as db

#history = list(db.find_all("history", {"movie": "Ratatouille"}))
#for hist in history:
#    if len(hist["products"]) ==0:
#        db.delete("history", hist["_id"])

history = list(db.find_all("history"))
for hist in history:
    db.delete("history", hist["_id"])