import streamlit  as st
import pandas as pd

import api.suites as gi
import api.results as re

st.set_page_config(
    page_title="Suite Creator"
)

# Streamlit page title
st.title("Ghost Inspector: Suite Creator")

with st.sidebar:
    # Input field for API key
    api_key = st.text_input("Enter your API key:")

    if not api_key:
        st.info('The API key can be found at https://app.ghostinspector.com/account \
                        under the Details section.')

    # fetching list of organisations
    organisations = gi.Organisations(api_key)
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

# Get user inputs
suite_name = st.text_input("Suite Name")
base_url = st.text_input("Base URL")
suite_description = st.text_area("Suite Description")

# folder_id = st.text_input("Folder ID")
st.session_state.all_folders = re.fetch_folders(api_key)
if isinstance(st.session_state.all_folders, dict) is False:
    st.session_state.all_folders = None
    st.info("Please add your API key in the sidebar to pick folders.")

if 'all_folders' in st.session_state and st.session_state.all_folders is not None:
    # Folders dropdown
    folder_options = sorted([folder for folder in st.session_state.all_folders.keys()])
    st.session_state.selected_folder = st.selectbox('Pick a folder to house the new suite:', 
                                                   folder_options, 
                                                   index=None, 
                                                   placeholder="Expand dropdown ...",)
    if st.session_state.selected_folder:
        folder_id = st.session_state.all_folders[st.session_state.selected_folder]

# Add a line of text after the button
st.write("You can add multiple variables by using the below fields repeatedly.")

# Initialize an empty dictionary to store variables
if 'var_dict' not in st.session_state:
    st.session_state.var_dict = {}
# Input for variable name and value
variable_name = st.text_input("Variable Name")
variable_value = st.text_input("Variable Value")

# Button to add variable to the dictionary
if st.button("Add Variable"):
    if variable_name and variable_value:
        st.session_state.var_dict[variable_name] = variable_value
        # st.success(f"Added variable: {variable_name} = {variable_value}")
        st.session_state.var_list = [{"name": k, "value": v} 
                                     for k, v in st.session_state.var_dict.items()]
    else:
        st.error("Please enter both variable name and value.")

    # Display the current variables dictionary
    # st.write("Current Variables:", st.session_state.variables_dict)
    st.write("Current Variables:")
    st.dataframe(pd.DataFrame(list(st.session_state.var_dict.items()),
                        columns=["Name", "Value"]), hide_index=True)

csv_payload = st.file_uploader("Upload CSV")

if csv_payload is not None:
    df = pd.read_csv(csv_payload)

    # Button to create and update suite
    if st.button("Create Suite"):
        master_params = {
            'organization': org_id,
            'name': suite_name,
            'details': suite_description,
            'base_url': base_url,
            'folder': folder_id,
            'variables': st.session_state.var_list
            }
        try:
            suites = gi.Suites(master_params, api_key)
            new_suite_id = suites.suite_id
        except Exception as e:
            print(f"Error creating suite: {e}")
    
        # creating and updating tests for each row
        with st.spinner('Creating and updating tests as per uploaded CSV ...'):
            for index, row in df.iterrows():
                test_params = {}
                test_params['test_id'] = row['clone-test-id']
                test_params['test_name'] = row['test-name']
                test_params['start_url'] = row['starting-url'].replace("$baseUrl", base_url)
                test_params['suite_id'] = new_suite_id
                
                tests = gi.Tests(test_params, api_key)
        st.success(f"Suite created and populated with tests successfully! \
                   \n\nAccess it at: https://app.ghostinspector.com/suites/{new_suite_id}")
