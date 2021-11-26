import hug
import threading
import requests
import os
import time
import json
import datetime

def thread_function(name):
    print("Daemon thread " + str(name) + ": starting")
    # time.sleep(2)
    # print("Daemon thread " + str(name) + ": finishing")

@hug.startup()
def daemon_thread(self):
    print("Main    : Creating daemon thread...")
    daemon = threading.Thread(target=thread_function, args=(1,), daemon=True)
    print("Main    : Running daemon thread...")
    daemon.start()
    print("Main    : Daemon thread is running...")

    # HealthChecks
    
