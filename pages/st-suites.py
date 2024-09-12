import streamlit  as st
import pandas as pd

st.set_page_config(
    page_title="Suite Creator"
)

# Streamlit page title
st.title("Ghost Inspector: Suite Creator")

# Input field for API key
api_key = st.sidebar.text_input("Enter your API key:")

# Input field for Organisation ID
org_id = st.sidebar.text_input("Enter your Organisation ID:")
st.sidebar.info('The API key can be found at https://app.ghostinspector.com/account \
                under the Details section. \
                \n\nThe Organisation ID can be found at https://app.ghostinspector.com/account/organizations \
                by clicking on one of the available organisations there.')

# Get user inputs
suite_name = st.text_input("Suite Name")
base_url = st.text_input("Base URL")
suite_description = st.text_area("Suite Description")
folder_id = st.text_input("Folder ID")

# Add a line of text after the button
st.write("You can add multiple variables by using the below fields repeatedly.")

# Initialize an empty dictionary to store variables
if 'variables_dict' not in st.session_state:
    st.session_state.variables_dict = {}
# Input for variable name and value
variable_name = st.text_input("Variable Name")
variable_value = st.text_input("Variable Value")

# Button to add variable to the dictionary
if st.button("Add Variable"):
    if variable_name and variable_value:
        st.session_state.variables_dict[variable_name] = variable_value
        # st.success(f"Added variable: {variable_name} = {variable_value}")
    else:
        st.error("Please enter both variable name and value.")

    # Display the current variables dictionary
    # st.write("Current Variables:", st.session_state.variables_dict)
    st.write("Current Variables:")
    st.dataframe(pd.DataFrame(list(st.session_state.variables_dict.items()),
                        columns=["Name", "Value"]), hide_index=True)

csv_payload = st.file_uploader("Upload CSV")

if csv_payload is not None:
    df = pd.read_csv(csv_payload)

    for index, row in df.iterrows():
        clone_test_id = row['clone-test-id']
        test_name = row['test-name']
        starting_url = row['starting-url']
        starting_url = starting_url.replace("$baseUrl", base_url)

    # Button to add variable to the dictionary
    if st.button("Create Suite"):
        # Invoke suite creation function
        None