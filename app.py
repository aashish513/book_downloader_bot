from flask import Flask
import threading
import os




def run_bot():
    while True:
        os.system("python3 bot.py")
        print("[WARNING] The bot.py shut down. This should not be printed")
        import time
        time.sleep(1)

# threading.Thread(run_bot()).start()
thread = threading.Thread(target=run_bot)
thread.start()



app = Flask(__name__)


# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the App!"


# if __name__ == '__main__':
#     threading.Thread(run_bot()).start()
#     app.run(debug=False)
