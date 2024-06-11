from flask import Flask, jsonify, request
import threading
import os


try:
    from pymongo.mongo_client import MongoClient
except:
    os.system('python -m pip install "pymongo[srv]"')

try:
    import pyrogram
except:
    os.system("pip install tgcrypto")
    os.system("pip install git+https://github.com/KurimuzonAkuma/pyrogram.git")
    

app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the App!"



def run_bot():
    while True:
        os.system("python3 bot.py")
        print("[WARNING] The bot.py shut down. This should not be printed")
        import time
        time.sleep(1)


if __name__ == '__main__':
    app.run(debug=False)
