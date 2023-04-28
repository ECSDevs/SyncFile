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
    os.system("start python server_autogen.py")
    app.run(host="0.0.0.0",port=7809)
