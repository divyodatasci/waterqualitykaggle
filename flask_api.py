# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 19:46:56 2021

@author: Admin
"""

from flask import Flask,request
import numpy as np
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger


app = Flask(__name__)
Swagger(app)

pickle_in = open("water_classifier.pkl","rb")

water_classifier = pickle.load(pickle_in)

@app.route('/')
def welcome():
    return "Welcome All"

@app.route('/predict', methods=["Get"])
def predict_water_potability():
    
    """Let's check the quality of water using the following parameters.
    ---
    parameters:
        - name: ph
          in: query
          type: number
          required: true
        - name: Hardness
          in: query
          type: number
          required: true
        - name: Solids
          in: query
          type: number
          required: true
        - name: Chloramines
          in: query
          type: number
          required: true
        - name: Sulfate
          in: query
          type: number
          required: true
        - name: Conductivity
          in: query
          type: number
          required: true
        - name: Organic_carbon
          in: query
          type: number
          required: true
        - name: Trihalomethanes
          in: query
          type: number
          required: true
        - name: Turbidity
          in: query
          type: number
          required: true
    responses:
        200:
            description: The output values
            
    """
    ph= request.args.get("ph") 
    Hardness= request.args.get("Hardness")
    Solids= request.args.get("Solids")
    Chloramines= request.args.get("Chloramines") 
    Sulfate= request.args.get("Sulfate")
    Conductivity= request.args.get("Conductivity") 
    Organic_carbon= request.args.get("Organic_carbon") 
    Trihalomethanes= request.args.get("Trihalomethanes")
    Turbidity= request.args.get("Turbidity")
    
    prediction=water_classifier.predict([[ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]])
    print(prediction)
    return "Hello The answer is"+str(prediction)


@app.route('/predict_file',methods=["POST"])
def predict_waterquality_file():
    
    """Let's check quality of water
    This is using docstrings for specifications.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
        
    """
    df_test=pd.read_csv(request.files.get("file"))
    print(df_test.head())
    prediction=water_classifier.predict(df_test)
    
    return str(list(prediction))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080) 
         