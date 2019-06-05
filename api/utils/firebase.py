import pyrebase


class Firebase():
    def __init__(self):
        config = {
            "apiKey": "AIzaSyD_iJiVuDbFRQi0z65Q8X803MhknKxnx7s",
            "authDomain": "sober-driver-1547168650254.firebaseapp.com",
            "databaseURL": "https://sober-driver-1547168650254.firebaseio.com",
            "storageBucket": "sober-driver-1547168650254.appspot.com"
        }
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def create(self, collection, data):
        self.db.child(collection).set(data)

    def delete(self, collection, room_id):
        self.db.child(collection).child(room_id).remove()
