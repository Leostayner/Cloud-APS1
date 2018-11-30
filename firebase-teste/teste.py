import pyrebase

config = {
    'apiKey': "AIzaSyDXqCgLK3aI--94TpUkbV9Cg0N0hO0-5qw",
    'authDomain': "cloud-leo-83ccf.firebaseapp.com",
    'databaseURL': "https://cloud-leo-83ccf.firebaseio.com",
    'projectId': "cloud-leo-83ccf",
    'storageBucket': "cloud-leo-83ccf.appspot.com",
    'messagingSenderId': "774405168607"
  }

firebase = pyrebase.initialize_app(config)
db = firebase.database()


db.push({"id": 1, "nome": "unificar", "description": "teste-inicial"})
a = db.get()
#db.child("tarefas").remove
l = a.val()
print(l)