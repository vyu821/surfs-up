from flask import Flask

#create new Flask app instance
app = Flask(__name__)

# flask routes
# root, starting point
@app.route('/')
def hello_world():
    return 'Hello World'
