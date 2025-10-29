# entrypoint.py
import os
import sys
import uvicorn

port = int(os.getenv("PORT", "8000"))
print(f"[boot] PID={os.getpid()} PORT={port} PYTHONPATH={os.getenv('PYTHONPATH','')}")
sys.stdout.flush()

# Run app explicitly; no shell expansion needed
uvicorn.run("src.app:app", host="0.0.0.0", port=port, log_level="info")
