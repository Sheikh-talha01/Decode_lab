import os
import sys

# Ensure project1/src is importable
ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from project1.app import create_app
import uvicorn

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
