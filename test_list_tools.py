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

initialized_msg = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}

list_tools_msg = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
}

time.sleep(3) # Wait for proxy to establish
print("Sending initialize")
proc.stdin.write(json.dumps(init_msg) + "\n")
proc.stdin.flush()

line = proc.stdout.readline()
print("INIT STDOUT:", line.strip())

print("Sending initialized notification and tools/list")
proc.stdin.write(json.dumps(initialized_msg) + "\n")
proc.stdin.write(json.dumps(list_tools_msg) + "\n")
proc.stdin.flush()

line = proc.stdout.readline()
print("TOOLS STDOUT:", line.strip())

proc.terminate()
