from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
import datetime
import bcrypt
import traceback
import math
import json
from tools.eeg import get_head_band_sensor_object


from db_con import get_db_instance, get_db

from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"


#Create our app
app = Flask(__name__)
#add in flask json
FlaskJSON(app)

#g is flask for a global var storage 
def init_new_env():
    #To connect to DB
    if 'db' not in g:
        g.db = get_db()

    if 'hb' not in g:
        g.hb = get_head_band_sensor_object()

    #g.secrets = get_secrets()
    #g.sms_client = get_sms_client()

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/') #endpoint
def index():
    return redirect('/static/index.html')


@app.route("/secure_api/<proc_name>",methods=['GET', 'POST'])
@token_required
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp



@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp

def compute_average_euclidean_distance():
    db, cursor = get_db_instance()
    cursor.execute("SELECT data FROM brain")
    rows = cursor.fetchall()

    max_index = len(rows) - (len(rows) % 2) #if odd ignores last data set in table
    total_distance = 0

    for i in range(max_index // 2):
        data1 = json.loads(rows[i][0])
        data2 = json.loads(rows[max_index // 2 + i][0])

        distance = math.sqrt(
            (data1['O1'] - data2['O1']) ** 2 +
            (data1['O2'] - data2['O2']) ** 2 +
            (data1['T3'] - data2['T3']) ** 2 +
            (data1['T4'] - data2['T4']) ** 2
        )
        total_distance += distance

    average_distance = total_distance / (max_index // 2)
    return average_distance

@app.route("/average_euclidean_distance")
def average_euclidean_distance():
    try:
        average_distance = compute_average_euclidean_distance()
        return json_response(data={"Average_Euclidean_Distance": average_distance})
    except Exception as e:
        logger.error(f"Error computing average Euclidean distance: {e}")
        return json_response(status_=500, data={"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

