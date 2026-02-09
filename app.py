import pandas as pd
import streamlit as st
from visitor import visitor_reg, visitor_list

def main():
    st.set_page_config(
        page_title="Hotel Visitor Management System",
        page_icon="🏨",
        layout="wide",
        initial_sidebar_state="auto"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding-top: 0rem;
        }
        .stButton > button {
            background-color: #1f77b4;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            padding: 10px 30px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #0f4a7f;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for page tracking
    if "page" not in st.session_state:
        st.session_state.page = "Visitor Registration"
        visitor_reg()  # Show visitor registration by default

    # side bar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Use the options below to navigate through the application.")
    
    if st.sidebar.button("Visitor Registration", use_container_width=True):
        st.session_state.page = "Visitor Registration"
    if st.sidebar.button("Visitor List", use_container_width=True):
        st.session_state.page = "Visitor List"
    
    # Display content based on selected page
    if st.session_state.page == "Visitor Registration":
        visitor_reg()
    elif st.session_state.page == "Visitor List":
        visitor_list()

if __name__ == "__main__":
    main()