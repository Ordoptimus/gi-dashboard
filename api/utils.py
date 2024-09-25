import pandas as pd


def format_df(df):
    '''
    Formats the result_df to remove extraneous columns and rearrange important ones
    '''
    df = df.drop(columns=['Test Result ID', 
                          'Browser', 
                          'Screen Size', 
                          'Geolocation', 
                          'Start URL', 
                          'End URL', 
                          'Status', 
                          'Date Triggered'])
    priority_cols = ['Name',
                    'Passed', 
                    'Screenshot Passed',
                    'Screenshot Difference',
                    'Test Result URL',
                    'Screenshot Comparison URL',
                    'Date Completed',
                    'Video URL'
                    ]
    remaining_cols = [col for col in df.columns.to_list() if col not in priority_cols]
    priority_cols.extend(remaining_cols)
    df = df.reindex(columns=priority_cols)
    df['Screenshot Difference'] *= 100  # converting back to percentage form
    return df


# #deprecated
# def parse_tests(all_tests):
#     '''
#     Arranging the all-test JSON output by suite
#     '''
#     suite_dict = {}
#     for test_id, suite in all_tests.items():
#         if suite not in suite_dict:
#             suite_dict[suite] = [test_id]
#         else:
#             suite_dict[suite].append(test_id)
#     return suite_dict


# # deprecated
# def test_iterate(suite_dict, api_key):
#     '''
#     Collect Dataframe test results per suite for entire organisation
#     '''
#     result_df, suite_results = pd.DataFrame(), {}

#     for suite, test_list in suite_dict.items():
#         for test in test_list:
#             df = csv_tests(test, api_key)
#             result_df = pd.concat([result_df, df])
#         suite_results[suite] = result_df

#         print(f"Results per suite: {suite_results}")

#     return suite_results


# # deprecated
# def fetch_suite_tests(api_key):
#     '''
#     Fetches a comprehensive list of all tests in JSON, abridged to test_id and suite
#     '''
#     api_endpoint = f"https://api.ghostinspector.com/v1/tests/?apiKey={api_key}"

#     try:
#         response = requests.get(api_endpoint.format(api_key))
#         response_json = response.json()

#         all_tests = {}
#         for test in response_json["data"]:
#             test_id = test.get("_id")
#             suite = test.get("suite")
#             if test_id and suite:
#                 all_tests[test_id] = suite["name"]

#         return all_tests
#     except Exception as e:
#         print(f"Error fetching test IDs and suites: {e}")
#         return {}
