import os
from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, abort

app = Flask(__name__)
api = Api(app)

tasks = [
    {"id": 1,
    "title": "Alo",
    "description": "alo 1 vez"},
    
    {"id": 2,
    "title": "Alo Alo",
    "description": "alo 2 vez"},

    {"id": 3,
    "title": "Alo Alo Alo",
    "description": "alo 3 vez"}
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
}

class Tarefas(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required = True,  help= 'No task title provided',  location='json')
        self.reqparse.add_argument('description', type=str, default = "", location='json')
        super(Tarefas, self).__init__()
        
    def get(self):
        return {'tasks': [marshal(task, task_fields) for task in tasks]}
                                   
    def post(self):
        args = self.reqparse.parse_args()
        print(args, len(args))
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description']
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}, 201


class TarefasID(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required = True, location='json')
        self.reqparse.add_argument('description', type=str, default = "", location='json')
        
    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task' : marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for key, value in args.items():
            if value is not None:
                task[key] = value

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
            tasks.remove(task[0])
            return{'result' : True}



api.add_resource(Tarefas, '/Tarefas/', endpoint='tasks')
api.add_resource(TarefasID, '/Tarefas/<int:id>', endpoint='task')

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5000)


