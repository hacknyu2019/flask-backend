import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_word():
    return "Hello World!"


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run()
    app.run(host='0.0.0.0', port=int(port))