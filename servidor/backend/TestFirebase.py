import pyrebase

class testFirebase():
    def __init__(self):
        self.config = {
            "apiKey": "AIzaSyBfFWZ1rknUXM-s6A5puyuXHXtHGrv5B7s",
            "authDomain": "simova-pji3.firebaseapp.com",
            "databaseURL": "https://simova-pji3.firebaseio.com",
            "projectId": "simova-pji3",
            "storageBucket": "simova-pji3.appspot.com",
            "messagingSenderId": "891988837307",
            "appId": "1:891988837307:web:3197a9ca70be4e46933a9e",
            "measurementId": "G-N7K82GVHQ5"
        }
        self.firebase = pyrebase.initialize_app(self.config)

    def enviar(self, info):
        dados = self.firebase.database()
        dados.child().update(info)
