from AC_turnip_prices import pogG
import flask
from flask import request, jsonify
import time
global save

global lastTime
lastTime=time.time()
save=pogG()
#print(save)
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])

def home():
    global save
    global lastTime
    if time.time()-lastTime>600:
        save=pogG(save)
        lastTime=time.time()
    else:
        print("time since last refresh:"+str(time.time()-lastTime))
    return jsonify(save)  

if __name__ == '__main__':
    app.run()
