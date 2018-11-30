import os
from flask import Flask, render_template,redirect,  jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal, abort
import random
import boto3
import requests
from threading import Timer
import threading
import time

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


def import_key(client):
	k = open("./teste/Lp.pub", "r")
	response = client.import_key_pair(
	KeyName = 'L2',
	PublicKeyMaterial = k.read()
)

def create_instance(ec2):
	instances = ec2.create_instances(
		ImageId='ami-0ac019f4fcb7cb7e6',
		MinCount= 1,
		MaxCount= 1,
		InstanceType = 't2.micro',
		SecurityGroups = ["APS_L"],
		KeyName= "L2",
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
	print("\nCreate Instance")
	return instances

def fila(_id, ip):
	print("Timer iniciado para:", ip)
	global list_queue
	global list_ids
	
	edp = "http://" + ip + ":5000/" + "healthcheck/"
				try:
					rq = requests.get(edp)
					if(rq.status_code != 200):
						raise ValueError("teste")
					
					list_ids.append(_id)
					list_queue.remove(_id)
	
				except:	
					client.terminate_instances(
						InstanceIds = [_id]
					)				


def check(client, ec2, list_ids, n_intances = 3):
	list_queue = []
	
	while True:
		if len(list_ids) > 0:
		
			for _id in list_ids:         
				edp = "http://" + dic_id[_id] + ":5000/" + "healthcheck/"
				
				try:
					rq = requests.get(edp)
					if(rq.status_code != 200):
						raise ValueError("teste")

				except:	
					print("Error: ",edp)
					list_ids.remove(_id)
					
					client.terminate_instances(
						InstanceIds = [_id]
					)	

					new_instance = create_instance(ec2)
					new_id  = new_instance[0].id
					new_instance = ec2.Instance(new_id)
					
					list_queue.append(new_id)
					dic_id[new_id] = new_instance.public_ip_address
					
					t = Timer(300.0, fila, args = [new_id, new_instance.public_ip_address])
					t.start()
					
					print("Instancia IP: {0}".format(dic_id[new_id]))
					

		if (len(list_ids) + len(list_queue) < n_intances):
			new_instance = create_instance(ec2)
			new_id  = new_instance[0].id
			
			new_instance = ec2.Instance(new_id)
			
			list_queue.append(new_id)
			dic_id[new_id] = new_instance.public_ip_address
			
			t = threading.Timer(300.0, fila, args = [new_id, new_instance.public_ip_address])
			t.start()

			print("Instancia IP: {0}".format(dic_id[new_id]))
								

threading.Thread(target =  check, args = [client, ec2, list_ids] ).start()

if __name__ == "__main__":
	app.run(debug = False, host = "0.0.0.0", port = 5000)
