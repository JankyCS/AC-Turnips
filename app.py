from AC_turnip_prices import pogG
import flask
from flask import request, jsonify
import time
global save

global lastTime
#lastTime=time.time()
#save=pogG()
#print(save)
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])

def home():
    return jsonify(pogG())  

if __name__ == '__main__':
    app.run()
