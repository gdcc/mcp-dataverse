import urllib.request
import threading
import time
import json
import ssl

def read_sse():
    req = urllib.request.Request("http://localhost:8100/sse")
    with urllib.request.urlopen(req) as resp:
        print("Connected to SSE")
        while True:
            line = resp.readline()
            if not line:
                break
            print("SSE:", line.decode('utf-8').strip())

t = threading.Thread(target=read_sse)
t.daemon = True
t.start()

time.sleep(1) # wait for SSE connection
