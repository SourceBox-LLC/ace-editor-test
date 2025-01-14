import streamlit as st

col1, col2 = st.columns(2)

with col1:
    st.header("Quickstart")
    st.write("Get started on a new project fast")
    if st.button("Get Started"):
        st.write("directing to quickstart page!")
    

with col2:
    st.header("Edit Project")
    st.write("Get to work on an existing project")
    st.button("Edit Project")
