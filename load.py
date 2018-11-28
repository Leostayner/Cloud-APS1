import os
from flask import Flask, render_template,redirect,  jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, abort
import random
import boto3
import requests
from threading import Timer

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
            if (tag["Key"] == "Owner") and (tag["Value"] == "Leonardo Medeiros"):
                list_ids.append(str(instance.id))
                dic_id[instance.id] = instance.public_ip_address
                
    return dic_id, list_id

    
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


dic_id, list_id = list_id(ec2, dic_id, list_ids)


@app.route('/', defaults={'path': ''}, methods = ["GET", "POST"])
@app.route('/<path:path>', methods = ["GET", "POST"])
def catch_all(path):
    ip = dic_id[random.choice(list_ids)]
    edp = "http://" + ip + ":5000/" + path
    return redirect(edp, code = 307)


def create_instance(ec2):
    instances = ec2.create_instances(
        ImageId='ami-0ac019f4fcb7cb7e6',
        MinCount= 1,
        MaxCount= 1,
        InstanceType = 't2.micro',
        SecurityGroups = ["APS_L"],
        KeyName= "L",
        TagSpecifications=[
            {
                'ResourceType': 'instance',

                'Tags': [
                    {
                        'Key': 'Owner',
                        'Value': "Leonardo Medeiros",
                    },
                ]
            },
        ],
        UserData = """#!/bin/bash
        git clone https://github.com/Leostayner/Cloud-APS1
        cd /Cloud-APS1  
        . install.sh
        """
    )
    print("Create Instance")
    return instances



def terminate_instances(client, _id):
    waiter = client.get_waiter('instance_terminated')
    client.terminate_instances(
        InstanceIds = [_id]
    )

def check(client, ec2, n_intances = 3):
    for _id in list_ids:
        edp = "http://" + dic_id[_id] + ":5000/" + "healthcheck/"

        flag = False     
        for time in range(1000):
            try:
                rq = requests.get(edp)
                if(rq.text == 200):
                    flag = True
                    break      

            except:
                pass
        
        if (not flag):
            terminate_instances(client, _id)
            list_ids.remove(_id)

        if (len(list_ids) < n_intances):
            instance = create_instance(ec2)
            #waiter = client.get_waiter('instance_terminated')
            #waiter.wait(InstanceIds = instance[0].id)
            list_ids.append(instance[0].id)

t = Timer(30.0, check, args = (client, ec2))
t.start()

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5000)
