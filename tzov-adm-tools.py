from flask import Flask, jsonify, request, make_response

import json
import re
app = Flask(__name__)
import warnings
warnings.filterwarnings('ignore')
import os
import time

import requests
import xmltodict

global port
port= os.environ["PORT"]






def has_non_digit(inputString):
    return bool(re.search(r'\D', inputString))

 
    



@app.route('/scrape', methods=['GET'])
def scrape_data():
    id = str(request.args.get('id'))
    if len(id)!=8 or has_non_digit(id):
        return jsonify({'Error': 'Invalid length or symbol'}), 400
    
    try:
        time.sleep(1)
        r = requests.get(url="https://adm.tools/action/gov/api/", params={"egrpou": id})
        if r.status_code == 429:
            return jsonify({'Error': 'Too many requests'}), 429
        


        
        data_1 = xmltodict.parse(r.content)
        data_1=data_1['export']['company']
       
       

        data={'id':id, 
            'name':data_1["@name"].replace('"',"'"),
            'name_short':data_1["@name_short"].replace('"',"'"),
            'address':data_1["@address"].replace('"',"'"),
            'director':data_1["@director"].replace('"',"'"),
            'director_gen':data_1["@director_gen"].replace('"',"'")
            }
        
            

        

    

        # Use json.dumps to convert the dictionary to a JSON string with indentation
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        # Use jsonify to create a response object from the JSON string
        response = make_response(json_str)
        # Set the content-type to 'application/json'
        response.mimetype = 'application/json'
        return response



    except:
        return jsonify({'Error': 'Try again, error on API side'}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,use_reloader=False,debug=False)