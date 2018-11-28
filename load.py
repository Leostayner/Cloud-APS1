import os
from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, abort
import random

app = Flask(__name__)
api = Api(app)

dic_id   = []
list_ids = []

def list_id(ec2):
    list_instances = ec2.instances.all()
    
    for instance in list_instances:
        list_tags = (instance.tags)

        try:
            for tag in list_tags:
                if (tag["Key"] == "Owner") and (tag["Value"] == "Leonardo Medeiros") and len(list_tags) == 1:
                    list_id.append[instance.id]
                    dic[instance.id] = instance.public_ip_address)
        except:
            pass

ec2 = boto3.resource('ec2')
list_id(ec2)

class GetAll(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required = True, location='json')
        self.reqparse.add_argument('description', type=str, default = "", location='json')
    
    def get(self):
        ip = dic_id[random.choice(list_ids)]
        edp = "http://" + ip + ":5000"
        request.get(edp)

    def post(self):
        ip = dic_id[random.choice(list_ids)]
        edp = "http://" + ip + ":5000"
        request.post(edp, json = request.json)

            
api.add_resource(GetAll, '/GetAll/', endpoint= 'getall')

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5000)