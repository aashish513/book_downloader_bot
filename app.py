from flask import Flask
import threading
import os
import requests
import time
url="https://book-downloader-bot-b051.onrender.com"



def run_bot():
    print("starting bot.py")
    # os.system("python3 bot.py")
    print("[WARNING] The bot.py shut down. This should not be printed")


# threading.Thread(run_bot()).start()
thread = threading.Thread(target=run_bot)
thread.start()


def keep_alive():
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # print(f"Successfully pinged {url}")
                pass
            else:
                print(f"Failed to ping {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while pinging {url}: {e}")
        time.sleep(60)  # Sleep for 1 minute

thread2 = threading.Thread(target=keep_alive)
thread2.start()


app = Flask(__name__)


# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the App!"


# if __name__ == '__main__':
#     threading.Thread(run_bot()).start()
#     app.run(debug=False)
