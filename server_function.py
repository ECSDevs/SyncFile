from flask import Flask
import os

# init app
app = Flask(__name__)

# web server
@app.route("/<path:path>")
def server(path):
    if path=='client.json':
        with open('client.json')as f:
            return f.read()
    with open(path,'rb')as f:
        return f.read()

if __name__ == '__main__':
    app.debug = True
    app.run(host="127.0.0.1",port=7809)