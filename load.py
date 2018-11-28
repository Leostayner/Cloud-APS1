import os
from flask import Flask, render_template,redirect,  jsonify
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
dic_id, list_id = list_id(ec2, dic_id, list_ids)


@app.route('/', defaults={'path': ''}, methods = ["GET", "POST"])
@app.route('/<path:path>', methods = ["GET", "POST"])
def catch_all(path):
    ip = dic_id[random.choice(list_ids)]
    edp = "http://" + ip + ":5000/" + path
    return redirect(edp, code = 307)

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5000)