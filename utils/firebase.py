import firebase_admin
from firebase_admin import credentials, firestore_async, storage

cred = credentials.Certificate("config/firebase.json")
app = firebase_admin.initialize_app(cred, {
  "storageBucket": "..."
})

db = firestore_async.client()
bucket = storage.bucket()