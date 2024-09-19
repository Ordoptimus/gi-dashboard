import streamlit as st

st.set_page_config(
    page_title="GI Dashboard"
)

st.write("# Ghost Inspector: Dashboard")

st.sidebar.info("Navigate to the required service above.")

st.markdown(
    """
    Welcome to the Ghost Inspector Dashboard, a utility to enable bulk actions
    and speed up the users' workflow in the [Ghost Inspector](https:app.ghostinspector.com)
    automated testing platform.
    """
)

st.info("If you are familiar with Ghost Inspector and this dashboard, \
    proceed to the required service from the sidebar.")

st.markdown(
    """
    ### Features
    #### Check Results
    - View suite-level test execution results with all test details.
    - Skip opening individual tests to check parameters like screenshot difference.
    - Quick access to URLs for tests, screenshot comparisons, recorded videos.
    - Easy interface to cycle between multiple suites in multiple folders.
    - Sort results based on metric of choice, such as highest screenshot difference.
    - Reduces time taken to zero-in on anomalous results by **75%**.

    #### Create Suite
    - Bulk create a suite and all required tests in it.
    - Single interface to provide all necessary creation parameters.
    - Convenient CSV functionality to configure tests to be added to the new suite.
    - One click execution handles suite creation, updation, and test creation, updation.
    - Reduces time required to create a suite and its tests by atleast **300%**,
      if at least one template/sample/precedent for each test exists.


    ### Reference
    - The dashboard has handy information boxes with links for fields which may require 
      a few steps for the user to source.
    - Linear design principles are used, with the user expected to proceed from top to bottom.
    - Where prudent, interface elements like buttons and dropdowns only appear if 
      preceding conditions are met, minimising scope for confusion.
    - CSV format will have a guide here in the next update.


    """
)
