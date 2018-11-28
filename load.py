import os
from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, abort
import random
import boto3

app = Flask(__name__)
api = Api(app)

dic_id   = {}
list_ids = []

def list_id(ec2, dic_id, list_ids):
    list_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

    for instance in list_instances:
        list_tags = (instance.tags)

        for tag in list_tags:
            if (tag["Key"] == "Owner") and (tag["Value"] == "Leonardo Medeiros") and len(list_tags) == 1:
                list_ids.append(str(instance.id))
                dic_id[instance.id] = instance.public_ip_address
                
    return dic_id, list_id
    
ec2 = boto3.resource('ec2')
#ec2 = boto3.resource('ec2', region_name = "us-east-1" , aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY)
dic_id, list_id = list_id(ec2, dic_id, list_ids)


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