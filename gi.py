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


def fetch_all(api_key):
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


def test_results(test_id, api_key):
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


def suite_results(suite_dict, suite, api_key):
    '''
    Collect Dataframe test results for the given suite
    '''
    test_list = suite_dict[suite]
    result_df = pd.DataFrame()

    for test in test_list:
        df = test_results(test, api_key)
        result_df = pd.concat([result_df, df])
    return result_df


# deprecated
def test_iterate(suite_dict, api_key):
    '''
    Collect Dataframe test results per suite for entire organisation
    '''
    result_df, suite_results = pd.DataFrame(), {}

    for suite, test_list in suite_dict.items():
        for test in test_list:
            df = test_results(test, api_key)
            result_df = pd.concat([result_df, df])
        suite_results[suite] = result_df

        print(f"Results per suite: {suite_results}")

    return suite_results
