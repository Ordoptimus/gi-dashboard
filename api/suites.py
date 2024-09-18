import requests
import io
import pandas as pd


def create_suite(name, org, api_key):
    '''
    Creates a new suite for the provided org ID
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/suites/?apiKey={api_key}"
    payload = {
        "name": name,
        "organization": org
    }

    try:
        response = requests.post(api_endpoint.format(api_key), json=payload)
        response_json = response.json()
        suite_id = response_json['data']['_id']
        return suite_id
    
    except Exception as e:
        print(f"Error creating suite: {e}")
        return e


def update_suite(suite_id, updates, api_key):
    '''
    Updates given suite with the provided configuration
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/suites/{suite_id}/?apiKey={api_key}"
    payload = {
        "folder": updates.get("folder_id"),
        "details": updates.get("description"),
        "variables": updates.get("variables")
    }

    try:
        response = requests.post(api_endpoint.format(suite_id, api_key), json=payload)
        response_json = response.json()
        return response_json
    
    except Exception as e:
        print(f"Error creating suite: {e}")
        return e
    
    
def suite_handler():
    None
    

def duplicate_test(test_id, api_key):
    '''
    Dupicates existing test as template to be passed for updation
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/tests/{test_id}/duplicate/?apiKey={api_key}"

    try:
        response = requests.post(api_endpoint.format(test_id, api_key))
        response_json = response.json()
        test_id = response_json['data']['_id']
        return test_id
    
    except Exception as e:
        print(f"Error duplicating suite: {e}")
        return e

