# exe command: pyinstaller --onefile ghost_inspector_app.py


import streamlit as st
import api.results as gi
import api.suites as su

st.set_page_config(
    page_title="GI Dashboard"
)

# Streamlit page title
st.title("Ghost Inspector: Test Results")

# info box to get user to input API key
st.info('Enter your API key in the sidebar.', icon="ℹ️")

# Input field for API key
# api_key = st.sidebar.text_input("Enter your API key:")
# st.sidebar.info('The API key can be found at https://app.ghostinspector.com/account \
#         under the Details section.')

with st.sidebar:
    # Input field for API key
    api_key = st.text_input("Enter your API key:")
    org_id = None

    if not api_key:
        st.info('The API key can be found at https://app.ghostinspector.com/account \
                        under the Details section.')

    # fetching list of organisations
    organisations = su.Organisations(api_key)
    st.session_state.all_orgs = organisations.all_orgs

    # alert box to prompt for API key beofre showing org dropdown
    if isinstance(st.session_state.all_orgs, dict) is False:
        st.session_state.all_orgs = None
        st.info("Please add your API key above to select organisation.")

    if 'all_orgs' in st.session_state and st.session_state.all_orgs is not None:
        # Organisations dropdown
        org_options = sorted([org for org in st.session_state.all_orgs.keys()])
        st.session_state.selected_org = st.selectbox('Select organisation to house the new suite:', 
                                                    org_options, 
                                                    index=None, 
                                                    placeholder="Expand dropdown ...",)
        if st.session_state.selected_org:
            org_id = st.session_state.all_orgs[st.session_state.selected_org]

# API calls
if st.button("Connect to Ghost Inspector"):
    with st.spinner('Fetching list of test folders ...'):
        # fetching folder name-id dictionary
        folders = gi.Folders(api_key, org_id)
        st.session_state.all_folders = folders.all_folders
        if isinstance(st.session_state.all_folders, dict) is False or org_id is None:
            st.session_state.all_folders = None
            st.error("Error connecting. Please check your API key and organisation.")


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
                folders = gi.Folders(api_key, org_id)
                folder_id = st.session_state.all_folders[st.session_state.selected_folder]
                st.session_state.suite_dict = folders.folder_suites(folder_id)
                
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
