import sys
import requests
import json

ip = input("Public IP: ")
edp = "http://" + ip + ":5000/Tarefas/"

if (sys.argv[1]) == "tarefa adicionar":
    data = {"title": sys.argv[2], "description": sys.argv[3]}
   
    r = requests.post(edp, json = data)
    print(r.text)

elif (sys.argv[1]) == "tarefa listar":
    r = requests.get(edp)
    print(r.text)
    