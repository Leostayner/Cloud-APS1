import os
from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, abort
import pyrebase

app = Flask(__name__)
api = Api(app)

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


class Tarefas(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required = True,  help= 'No task title provided',  location='json')
        self.reqparse.add_argument('description', type=str, default = "", location='json')
        super(Tarefas, self).__init__()
        
    def get(self):
        return db.get()
                                   
    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': 1,
            'title': args['title'],
            'description': args['description']
        }
        return db.push(task)


# class TarefasID(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, required = True, location='json')
#         self.reqparse.add_argument('description', type=str, default = "", location='json')
        
#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task' : marshal(task[0], task_fields)}

#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for key, value in args.items():
#             if value is not None:
#                 task[key] = value
# waiter = client.get_waiter('instance_terminated')
#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#             tasks.remove(task[0])
#             return{'result' : True}

@app.route('/healthcheck/', methods = ["GET"])
def healthcheck():
    return "", 200


api.add_resource(Tarefas, '/Tarefas/', endpoint='tasks')
# api.add_resource(TarefasID, '/Tarefas/<int:id>', endpoint='task')

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5000)


