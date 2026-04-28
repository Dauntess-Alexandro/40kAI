import time
import os
from project_paths import RESPONSE_PATH, ensure_runtime_dirs

def sendToGUI(message):
    ensure_runtime_dirs()
    with open(str(RESPONSE_PATH), "w", encoding="utf-8") as f:
        f.write(message)

def recieveGUI():
    time.sleep(1)
    file_path = str(RESPONSE_PATH)
    if os.path.exists(file_path):
        os.remove(file_path)

    while True: 
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                response = f.read()
            os.remove(file_path)
            return response
