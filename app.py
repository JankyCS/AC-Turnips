from AC_turnip_prices import getListings
import flask
from flask import request, jsonify
import time
global save
global lastTime
lastTime=time.time()
save=getListings()
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])

def home():
    global save
    global lastTime
    if time.time()-lastTime>600:
        save=getListings(save)
        lastTime=time.time()
    return jsonify(save)  

if __name__ == '__main__':
    app.run()
