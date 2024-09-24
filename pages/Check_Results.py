# exe command: pyinstaller --onefile ghost_inspector_app.py


import streamlit as st
import api.results as gi

st.set_page_config(
    page_title="GI Dashboard"
)

# Streamlit page title
st.title("Ghost Inspector: Test Results")

# info box to get user to input API key
st.info('Enter your API key in the sidebar.', icon="ℹ️")

# Input field for API key
api_key = st.sidebar.text_input("Enter your API key:")
st.sidebar.info('The API key can be found at https://app.ghostinspector.com/account \
        under the Details section.')

# API calls
if st.button("Connect to Ghost Inspector"):
    with st.spinner('Fetching list of test folders ...'):
        # fetching folder name-id dictionary
        st.session_state.all_folders = gi.fetch_folders(api_key)
        if isinstance(st.session_state.all_folders, dict) is False:
            st.session_state.all_folders = None
            st.error("Error connecting. Please check your API key.")


if 'all_folders' in st.session_state and st.session_state.all_folders is not None:
    # Folders dropdown
    folder_options = sorted([folder for folder in st.session_state.all_folders.keys()])
    st.session_state.selected_folder = st.selectbox('Pick a folder to view its test suites:', 
                                                   folder_options, 
                                                   index=None, 
                                                   placeholder="Expand dropdown ...",)

    if st.session_state.selected_folder is not None:
        # Fetch suites button
        if st.button("Fetch Suites"):
            with st.spinner('Fetching suite data ...'):
                # fetching suite name-id dictionary
                folder_id = st.session_state.all_folders[st.session_state.selected_folder]
                st.session_state.suite_dict = gi.folder_suites(folder_id, api_key)
                
        if "suite_dict" in st.session_state:
            # Suites dropdown
            suite_options = sorted([suite for suite in st.session_state.suite_dict.keys()])
            st.session_state.selected_suite = st.selectbox('Pick a suite to view its tests with results:', 
                                                suite_options, 
                                                index=None, 
                                                placeholder="Expand dropdown ...",)
            
            if st.session_state.selected_suite is not None:
                with st.spinner('Fetching test data ...'):
                    suite_id = st.session_state.suite_dict[st.session_state.selected_suite]
                    st.session_state.suite_result_df = gi.suite_results(suite_id, api_key)

                if 'suite_result_df' in st.session_state:
                    st.header(st.session_state.selected_suite)
                    st.dataframe(st.session_state.suite_result_df, hide_index=True)
                else:
                    st.error("Error fetching results. Please check your test ID and API key.")
