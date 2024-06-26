import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from django.conf import settings
import os

class FirebaseClient:

    def __init__(self):
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(os.path.expanduser('~/serviceAccountKey.json'))
            firebase_admin.initialize_app(cred)
        self._db = firestore.client()

        self._db = firestore.client()
        self._collection = self._db.collection(u'users')

    def get_by_id(self, id):
        """Get users on firestore database using document id"""
        print('debug did i get to this function?')
        doc_ref = self._collection.document(id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict().get("name")
        else:
            print("No such document!")
        return 'no_match'
        
    def all(self):
        """Get all users from firestore database"""
        docs = self._collection.stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]

    def filter(self, field, condition, value):
        """Filter users using conditions on firestore database"""
        docs = self._collection.where(field, condition, value).stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]
    
    def get_event_members(self, event_id):
        doc_ref = self._db.collection(u'party-groups').document(event_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()['members']
        else:
            print("No such document!")
        return []
    
    def get_fcm_tokens(self, id):
        doc_ref = self._collection.document(id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()['fcmTokens'][-1]
        else:
            print("No such document!")
        return ''
    