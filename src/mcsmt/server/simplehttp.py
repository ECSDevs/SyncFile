from flask import Flask

# init app
app = Flask(__name__)

# web server
@app.route("/<path:path>")
def server(path):
    with open(path,'rb')as f:
        return f.read()

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=7809)
