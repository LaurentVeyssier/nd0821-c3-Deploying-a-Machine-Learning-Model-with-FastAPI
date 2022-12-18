"""
Unit test of main.py API module with pytest
author: Laurent veyssier
Date: Dec. 16th 2022
"""

from fastapi.testclient import TestClient
from fastapi import HTTPException
import json
import logging

from starter.main import app

# Initialize logging
logging.basicConfig(filename='test.log',
                    level=logging.INFO,
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

client = TestClient(app)


def test_root():
    """
    Test welcome message for get at root
    """
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == "Welcome to our model API"


def test_inference_query():
    """
    Test model inference output
    """
    sample =  {  'age':50,
                'workclass':"Private", 
                'fnlgt':234721,
                'education':"Doctorate",
                'education_num':16,
                'marital_status':"Separated",
                'occupation':"Exec-managerial",
                'relationship':"Not-in-family",
                'race':"Black",
                'sex':"Female",
                'capital_gain':0,
                'capital_loss':0,
                'hours_per_week':50,
                'native_country':"United-States"
            }

    data = json.dumps(sample)

    r = client.post("/inference", data=data )

    # test response and output
    assert r.status_code == 200
    assert r.json()["age"] == 50
    assert r.json()["fnlgt"] == 234721

    # test prediction vs expected label
    logging.info(f'********* prediction = {r.json()["prediction"]} ********')
    assert r.json()["prediction"] == '>50K'


def test_incomplete_inference_query():
    """
    Test incomplete sample does not generate prediction
    """
    sample =  {  'age':50,
                'workclass':"Private", 
                'fnlgt':234721,
            }

    data = json.dumps(sample)
    r = client.post("/inference", data=data )

    assert 'prediction' not in r.json().keys()
    logging.warning(f"The sample has {len(sample)} features. Must be 14 features")
        
    