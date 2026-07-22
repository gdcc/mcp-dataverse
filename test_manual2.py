import urllib.request
import threading
import time
import json

session_id = None

def read_sse():
    global session_id
    req = urllib.request.Request("http://localhost:8100/sse")
    with urllib.request.urlopen(req) as resp:
        print("Connected to SSE")
        while True:
            line = resp.readline().decode('utf-8')
            if not line:
                break
            print("SSE:", line.strip())
            if line.startswith("data: /messages/?session_id="):
                session_id = line.strip().split("=")[1]

t = threading.Thread(target=read_sse)
t.daemon = True
t.start()

time.sleep(1) # wait for SSE connection
if session_id:
    print("Found session ID:", session_id)
    post_url = f"http://localhost:8100/messages/?session_id={session_id}"
    init_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    req = urllib.request.Request(post_url, data=json.dumps(init_msg).encode('utf-8'), method='POST')
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            print("POST Status:", resp.status)
            print("POST Response:", resp.read().decode('utf-8'))
    except Exception as e:
        print("POST Error:", e)

time.sleep(2) # wait for SSE response
