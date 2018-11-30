import threading
import random

list_ids = [0,1,2,3,4,5,6,7,8]


def check():
    list_name = ["a","b","c"]
    while True:
        for i in list_ids:
            list_ids.remove(i)
            print(list_ids)

threading.Thread(target = check,  ).start()
