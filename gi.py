'''
Sample O/P for fetch_all:

response = {
  "code": "SUCCESS",
  "data": [
    {
      "_id": "5db700c6881b5f7978697da9",
      "suite": {
        "_id": "5a1e1b90154014760af39ef5",
        "name": "Smoke Tests"
      },
    },
    {
      "_id": "5e2a0b342d0f5947444c31fc",
      "suite": {
        "_id": "5a1e1b90154014760af39ef5",
        "name": "Smoke Tests"
      },
    },
    {
      "_id": "5db700c6881b5f7978697da9",
      "suite": {
        "_id": "5a1e1b90154014760af39ef5",
        "name": "Sanity Tests"
      },
    },
    {
      "_id": "5e2a0b342d0f5947444c31fc",
      "suite": {
        "_id": "5a1e1b90154014760af39ef5",
        "name": "Sanity Tests"
      },
    }
  ]
}
'''


import requests
import io
import pandas as pd


def fetch_folders(api_key):
    '''
    Fetches a comprehensive list of all folders in JSON, abridged to folder_id, folder_name
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/folders/?apiKey={api_key}"

    try:
        response = requests.get(api_endpoint.format(api_key))
        response_json = response.json()

        all_folders = {}
        for folder in response_json["data"]:
            folder_id = folder.get("_id")
            folder_name = folder.get("name")
            if folder_id and folder_name:
                all_folders[folder_name] = folder_id

        return all_folders
    except Exception as e:
        print(f"Error fetching folder IDs and names: {e}")
        return {}


def folder_suites(folder_id, api_key):
    '''
    Fetches a list of all suites for a folder, in JSON, abridged to suite_id, suite_name
    WIP
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/folders/{folder_id}/suites/?apiKey={api_key}"

    try:
        response = requests.get(api_endpoint.format(folder_id, api_key))
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


def fetch_suite_tests(api_key):
    '''
    Fetches a comprehensive list of all tests in JSON, abridged to test_id and suite
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/tests/?apiKey={api_key}"

    try:
        response = requests.get(api_endpoint.format(api_key))
        response_json = response.json()

        all_tests = {}
        for test in response_json["data"]:
            test_id = test.get("_id")
            suite = test.get("suite")
            if test_id and suite:
                all_tests[test_id] = suite["name"]

        return all_tests
    except Exception as e:
        print(f"Error fetching test IDs and suites: {e}")
        return {}


def csv_tests(test_id, api_key):
    '''
    Fetching individual test results as CSV
    '''
    api_endpoint = f"https://api.ghostinspector.com/v1/tests/{test_id}/results/csv/?apiKey={api_key}"

    try:
        response = requests.get(api_endpoint.format(test_id, api_key))
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
    return result_df


#deprecated
def parse_tests(all_tests):
    '''
    Arranging the all-test JSON output by suite
    '''
    suite_dict = {}
    for test_id, suite in all_tests.items():
        if suite not in suite_dict:
            suite_dict[suite] = [test_id]
        else:
            suite_dict[suite].append(test_id)
    return suite_dict


# deprecated
def test_iterate(suite_dict, api_key):
    '''
    Collect Dataframe test results per suite for entire organisation
    '''
    result_df, suite_results = pd.DataFrame(), {}

    for suite, test_list in suite_dict.items():
        for test in test_list:
            df = csv_tests(test, api_key)
            result_df = pd.concat([result_df, df])
        suite_results[suite] = result_df

        print(f"Results per suite: {suite_results}")

    return suite_results
