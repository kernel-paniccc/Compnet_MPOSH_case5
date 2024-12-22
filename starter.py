from threading import Thread
from src import app
import os

with open("src/logs/app.log", 'w') as f:
    f.write("")

def run_tunnel():
    result = os.system('tuna http 8080')

if __name__ == "__main__":
    start = Thread(target=run_tunnel)
    #start.start()
    app.run(use_reloader=True, port=8080)
