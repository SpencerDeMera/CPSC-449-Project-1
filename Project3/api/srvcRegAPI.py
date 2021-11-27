import hug
import threading
import requests
import os
import time
import json
import datetime

registry = {}

def healthCheck():
    for srvc in registry:
        for items in registry[srvc]:
            r = requests.get("http://" + items + "/health")
            if r.status_code == 200:
                print("Success")
            else:
                registry[srvc].remove(items)

def daemon_function(name):
    print("Daemon thread " + str(name) + ": starting")
    time.sleep(30)

    # health checks
    while True:
        healthCheck()
        time.sleep(300) # Sleep for 300 seconds OR 5 minutes

@hug.startup()
def main(self):
    # Create Daemon thread
    print("Main    : Creating daemon thread...")
    daemon = threading.Thread(target=daemon_function, args=(1,), daemon=True)
    print("Main    : Running daemon thread...")
    daemon.start()
    print("Main    : Daemon thread is running...")

# Register new services
@hug.post('/register')
def register(
    name: hug.types.text, 
    domainName: hug.types.text, 
    port: hug.types.text,
    response,
):
    newService = {
        'Name': name,
        'DomainName': domainName,
        'Port': port,
    }
    mutex = threading.Lock()

    mutex.acquire()
    if newService["Name"] not in registry:
        registry[newService["Name"]] = [newService["DomainName"] + ':' + newService["Port"]]
    else:
        registry[newService["Name"]].append(newService["DomainName"] + ':' + newService["Port"])
    mutex.release()

    print(name + " service is registered")