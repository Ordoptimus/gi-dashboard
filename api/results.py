import requests
import io
import pandas as pd

import api.utils as utils


class Folders:
    def __init__(self, api_key, org_id) -> None:
        self.api_key = api_key
        self.org_id = org_id

        self.all_folders = self.fetch_folders()
        
    def fetch_folders(self) -> dict:
        '''
        Fetches a comprehensive list of all folders in JSON, abridged to folder_id, folder_name
        '''
        api_endpoint = f"https://api.ghostinspector.com/v1/folders/?apiKey={self.api_key}"

        try:
            response = requests.get(api_endpoint.format(self.api_key))
            response_json = response.json()

            all_folders = {}
            if response_json["code"] == "SUCCESS":
                for folder in response_json["data"]:
                    folder_id = folder.get("_id")
                    folder_name = folder.get("name")
                    folder_org = folder.get("organization")
                    if folder_org == self.org_id:
                        if folder_id and folder_name:
                            all_folders[folder_name] = folder_id

            return all_folders
        except Exception as e:
            print(f"Error fetching folder IDs and names: {e}")
            return e

    def folder_suites(self, folder_id) -> dict:
        '''
        Fetches a list of all suites for a folder, in JSON, abridged to suite_id, suite_name
        '''
        api_endpoint = f"https://api.ghostinspector.com/v1/folders/{folder_id}/suites/?apiKey={self.api_key}"

        try:
            response = requests.get(api_endpoint.format(folder_id, self.api_key))
            response_json = response.json()

            suite_dict = {}
            for suite in response_json["data"]:
                suite_id = suite.get("_id")
                suite_name = suite.get("name")
                if suite_id and suite_name:
                    suite_dict[suite_name] = suite_id

            return suite_dict
        except Exception as e:
            print(f"Error fetching suite IDs and names: {e}")
            return {}


def csv_tests(test_id, api_key):
    '''
    Fetching individual test results as CSV
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/tests/{test_id}/results/csv/?apiKey={api_key}"
    params = {"apiKey": api_key, "count": 1}

    try:
        response = requests.get(api_endpoint, params=params)
        # if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        return df
    except Exception as e:
        print(f"Error listing result for test ID {test_id}: {e}")


def suite_results(suite_id, api_key):
    '''
    Collect Dataframe test results for the given suite
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/suites/{suite_id}/tests/?apiKey={api_key}"
    test_list = []

    try:
        response = requests.get(api_endpoint.format(suite_id, api_key))
        response_json = response.json()

        for test in response_json["data"]:
            test_id = test.get("_id")
            if test_id:
                test_list.append(test_id)
    except Exception as e:
        print(f"Error fetching test IDs and suites: {e}")

    result_df = pd.DataFrame()
    for id in test_list:
        df = csv_tests(id, api_key)
        result_df = pd.concat([result_df, df])

    return utils.format_df(result_df)
