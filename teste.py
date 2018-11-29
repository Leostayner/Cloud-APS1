import threading
import random

list_ids = [0]


def check(list_ids):
    list_name = ["a","b","c"]
    while True:
        print(list_ids)
        list_ids.append(random.choice(list_name))

        if len(list_ids) > 5 :
            list_ids.remove(list_ids[0])

threading.Thread(target =  check, args = [list_ids] ).start()
