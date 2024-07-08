# largely a testing module and safe to ignore

import gi as gi

api_key = ''

all_tests = gi.fetch_all(api_key)
suite_dict = gi.parse_tests(all_tests)
suite_results = gi.test_iterate(suite_dict, api_key)
print(suite_results)