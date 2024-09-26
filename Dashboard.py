import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="GI Dashboard"
)

st.write("# Ghost Inspector: Dashboard")

st.sidebar.info("Navigate to the required service above.")

st.markdown(
    """
    Welcome to the Ghost Inspector Dashboard, a utility to enable bulk actions
    and speed up user workflow on the [Ghost Inspector](https://app.ghostinspector.com)
    automated testing platform.
    """
)

st.info(
    "If you are familiar with this dashboard and Ghost Inspector, \
    proceed to the required service from the sidebar."
)

st.write("Have a look through the _Why_, _What_, and _How_ tabs below to understand the dashboard.")

why_tab, what_tab, how_tab = st.tabs(["Why", "What", "How"])

why_tab.markdown(
    """
    ##### Check Results
    - View suite-level test execution results with all test details.
    - Skip opening individual tests to check parameters like screenshot difference.
    - Quick access to URLs for tests, screenshot comparisons, recorded videos.
    - Easy interface to cycle between multiple suites in multiple folders.
    - Sort results based on metric of choice, such as highest screenshot difference.
    - Reduces time taken to zero-in on anomalous results by **75%**.
    - Requires tests to have been created and run on your Ghost Inspector account.

    ##### Create Suite
    - Bulk create a suite and all required tests in it.
    - Single interface to provide all necessary creation parameters.
    - Convenient CSV functionality to configure tests to be added to the new suite.
    - One click execution handles suite creation, updation, and test creation, updation.
    - Reduces time required to create a suite and its tests by atleast **300%**.
    - At least one template/sample/precedent for each test type is a pre-requisite.
    - Use this feature after the templates have been created on Ghost Inspector.
    """
)

what_tab.markdown(
    """
    ##### CSV Format
    - A CSV file is required to build tests and attach them to the new suite.
    - This CSV requires a specific format to enable the dashboard to read it correctly.
    - Column names: `clone-test-id`, `test-name`, `starting-url`.
    - The order of columns does not matter so long as the name is accurate.
    - While `test-name` can take any string value as the test name, others have specific reqrements.
    - The `clone-test-id` has to be an existing test's ID as can be extracted from the test url.
      - Example: `https://app.ghostinspector.com/tests/66abf82c73297bf4d46dbc64` would have the \
        test ID as `66abf82c73297bf4d46dbc64` to be used under the `clone-test-id` column.
    - The `starting-url` can be a standard complete URL but it can also use the variable `$baseUrl`.
      - Standard URL: `https://docs.streamlit.io/develop/api-reference/write-magic/st.write`
      - Short URL: `$baseUrl/write-magic/st.write` 
      - Here, the common part `https://docs.streamlit.io/develop/api-reference` is replaced by `$baseUrl`, \
        which can be repeated in other URLs such as `$baseUrl/text/st.code` or `$aseUrl/media/st.logo`.
    ---
    """
)

what_tab.write("Sample CSV which uses the above data:")
csv_df = pd.DataFrame(
    {
        'clone-test-id': ['66abf82c73297bf4d46dbc64', '66abf82c73297bf4d46dbc65', '66abf82c73297bf4d46dbc66'],
        'test-name': ['Write Page', 'Code Page', 'Logo Page'],
        'starting-url': ['$baseUrl/write-magic/st.write', '$baseUrl/text/st.code', '$aseUrl/media/st.logo']
    }
)
what_tab.dataframe(csv_df, hide_index=True)

how_tab.markdown(
    """
    ##### Design
    - The dashboard has handy information boxes with links for fields which may require 
      a few steps for the user to source.
    - Linear design principles are used, with a top to bottom flow of use.
    - Where prudent, interface elements like buttons and dropdowns only appear if 
      preceding conditions are met, minimising the scope for confusion.
    
    ##### Sources
    - The official [Ghost Inspector API](https://docs.ghostinspector.com/api) \
      is used to interface with the platform. _Users will need an account and potentially \
      a subscription of the service to generate an API key to be used here_.
    - This dashboard has been built using the [Streamlit](https://docs.streamlit.io) framework.
    - Hosting has been provided by Streamlit's [Commmunity Cloud](https://share.streamlit.io) as open access.
    """
)
