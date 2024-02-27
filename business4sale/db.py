import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Initialize the Firebase app
#cred = credentials.Certificate('path/to/service-account.json')
#firebase_admin.initialize_app(cred)

BUSINESS_COLLECTION = 'business4sale'

# Save an object to Firestore
def save_object_to_firestore(id, obj):

    # Get the Firestore client
    db = firestore.client()
    
    # Save the JSON object to a document in the "users" collection
    res = db.collection(BUSINESS_COLLECTION).document(id).set(obj)
    print(res)


def test_save_object_to_firestore():
    id = "abc123"
    obj = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }
    save_object_to_firestore(id, obj)
