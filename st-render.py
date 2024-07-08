# exe command: pyinstaller --onefile ghost_inspector_app.py


import streamlit as st
import gi


# Streamlit app title
st.title("Ghost Inspector Test Results")

# info box to get user to input API key
st.info('Enter your API key in the sidebar. \
        You can get your key from https://app.ghostinspector.com/account \
        under the Details section.', icon="ℹ️")

# Input field for API key
api_key = st.sidebar.text_input("Enter your API key:")

# API calls
if st.button("Connect to Ghost Inspector"):
    with st.spinner('Fetching list of test suites ...'):
        all_tests = gi.fetch_all(api_key)
        st.session_state.suites = gi.parse_tests(all_tests)

if 'suites' in st.session_state:
    # Create a dropdown select box
    suite_options = sorted([suite for suite in st.session_state.suites.keys()])
    st.session_state.selected_suite = st.selectbox('Pick a suite to view its test results:', 
                                                   suite_options, 
                                                   index=None, 
                                                   placeholder="Expand dropdown ...",)

    if st.session_state.selected_suite is not None:
        with st.spinner('Fetching test data ...'):
            st.session_state.suite_result_df = gi.suite_results(st.session_state.suites, 
                                            st.session_state.selected_suite, 
                                            api_key)

            if 'suite_result_df' in st.session_state:
                # Fetch results button
                if st.button("Fetch Results"):
                    st.header(st.session_state.selected_suite)
                    st.write(st.session_state.suite_result_df)
                else:
                    st.error("Error fetching results. Please check your test ID and API key.")
