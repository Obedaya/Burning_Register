import utilities.database as db
from dotenv import load_dotenv
import os
import secrets

load_dotenv()

preauthmails = list(os.getenv("PREAUTHMAIL").split(","))

def init_auth():
    if not db.collection_exists("auth"):
        db.create_collection("auth")
    
    if len(list(db.find_all("auth"))) == 0:
        db.insert("auth", {
            "credentials": {"usernames": {}},
            "cookie": {"expiry_days": 30, "key": str(secrets.token_urlsafe), "name": "burning_cinema_auth"},
            "preauthorized": {"emails": preauthmails}
        })
                                    
