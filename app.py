from flask import Flask, request, jsonify
import requests
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained machine learning model
with open('crop_water_usage_model.pkl', 'rb') as f:
    model = pickle.load(f)
