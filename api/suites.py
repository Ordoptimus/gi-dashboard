import requests
import io
import pandas as pd


class Suites:

    def __init__(self, master_params, api_key) -> None:
        self.master_params = master_params
        self.api_key = api_key
        self.suite_id = None

        self.create_suite(self.master_params['name'],
                          self.master_params['organization'])
        self.update_suite(self.suite_id,
                          self.master_params)

    def create_suite(self, name, org) -> None:
        '''
        Creates a new suite for the provided org ID
        '''
        api_endpoint = f"https://api.ghostinspector.com/v1/suites/?apiKey={self.api_key}"
        payload = {
            "name": name,
            "organization": org
        }
        try:
            response = requests.post(api_endpoint.format(self.api_key), json=payload)
            response_json = response.json()
            self.suite_id = response_json['data']['_id']
        
        except Exception as e:
            print(f"Error creating suite: {e}")

    def update_suite(self, suite_id, master_params):
        '''
        Updates given suite with the provided configuration
        '''
        api_endpoint = f"https://api.ghostinspector.com/v1/suites/{suite_id}/?apiKey={self.api_key}"
        payload = {
            "folder": master_params.get("folder"),
            "details": master_params.get("details"),
            "variables": master_params.get("variables")
        }
        try:
            response = requests.post(api_endpoint.format(suite_id, self.api_key), json=payload)
            response.raise_for_status()
        
        except Exception as e:
            print(f"Error creating suite: {e}")
            return e
    

def duplicate_test(test_id, api_key) -> str:
    '''
    Dupicates existing test as template to be passed for updation
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/tests/{test_id}/duplicate/?apiKey={api_key}"
    try:
        response = requests.post(api_endpoint.format(test_id, api_key))
        response_json = response.json()
        new_test_id = response_json['data']['_id']
        return new_test_id
    
    except Exception as e:
        print(f"Error duplicating suite: {e}")
        return e


def update_test(test_id, test_params, api_key):
    '''
    Updates given test with the provided configuration
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/tests/{test_id}/?apiKey={api_key}"
    payload = {
            'name': test_params.get('test_name'),
            'startUrl': test_params.get('start_url'),
            'suite': test_params.get('suite_id')
        }
    try:
        response = requests.post(api_endpoint.format(test_id, api_key), json=payload)
        response.raise_for_status()
    
    except Exception as e:
        print(f"Error duplicating suite: {e}")
        return e
    