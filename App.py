import os
from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, abort
import pyrebase

app = Flask(__name__)
api = Api(app)

config = {
        
    "apiKey": "AIzaSyDXqCgLK3aI--94TpUkbV9Cg0N0hO0-5qw",
    'authDomain': "cloud-leo-83ccf.firebaseapp.com",
    'databaseURL': "https://cloud-leo-83ccf.firebaseio.com",
    'projectId': "cloud-leo-83ccf",
    'storageBucket': "cloud-leo-83ccf.appspot.com",
    'messagingSenderId': "774405168607"
  }

firebase = pyrebase.initialize_app(config)
db = firebase.database()


class Tarefas(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required = True,  help= 'No task title provided',  location='json')
        self.reqparse.add_argument('description', type=str, default = "", location='json')
        super(Tarefas, self).__init__()
        
    def get(self):
        print(db.get())
        return db.child("Tarefas").get().val()
                                   
    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'title': args['title'],
            'description': args['description']
        }
        db.child("Tarefas").set(task)
        return db.child("Tarefas").get().val()


@app.route('/healthcheck/', methods = ["GET"])
def healthcheck():
    return "", 200


api.add_resource(Tarefas, '/Tarefas/', endpoint='tasks')

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5000)


