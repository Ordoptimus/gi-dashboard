import requests
import io
import pandas as pd


def create_suite(name, org, api_key):
    '''
    Creates a new suite for the provided org ID
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/suites/?apiKey={api_key}"

    try:
        response = requests.post(api_endpoint.format(api_key))
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

    # replace payload with API specifications
    payload = {
        "folder": updates.get("folder_id"),
        "description": updates.get("description"),
        "variables": updates.get("variables")
    }

    try:
        response = requests.post(api_endpoint.format(api_key), json=payload)
        response_json = response.json()
        return suite_id
    
    except Exception as e:
        print(f"Error creating suite: {e}")
        return e
