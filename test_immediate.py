import subprocess
import time
import json

proc = subprocess.Popen(
    ["npx", "-y", "mcp-remote", "http://localhost:8100/sse"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

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

print("Sending initialize IMMEDIATELY")
proc.stdin.write(json.dumps(init_msg) + "\n")
proc.stdin.flush()

for _ in range(5):
    line = proc.stdout.readline()
    if line:
        print("STDOUT:", line.strip())

proc.terminate()
