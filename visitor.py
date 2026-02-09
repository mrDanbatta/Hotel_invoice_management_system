import pandas as pd
import streamlit as st
import datetime

def visitor_reg():
    # st.write("Welcome to the Hotel Visitor Management System. Please use the form below to register a visit.")
    # st.subheader("Visitor Registration Form")

    name, surname, rep, check_in, check_out, status = None, None, None, None, None, None
     # Header with styling
    st.markdown("# 🏨 Visitor Management System")
    st.markdown("Welcome to the Hotel Visitor Management System. Please use the form below to register a visit.")
    st.markdown("---")

    with st.container():
        st.markdown("## Visitor Registration Form")

    # Create a form for visitor registration
    name = st.text_input("First Name")
    surname = st.text_input("Last Name")
    rep = st.text_input("Company/Organization")
    check_in = st.date_input("Check-in Date")
    check_out = st.date_input("Check-out Date")
    hotel = st.selectbox("Hotel", ["Hilton London Paddington", "London Hilton On Park Lane",
                                   "Royal Lancaster London", "The Landmark London"])
    
    if st.button("Submit"):
        # Create a DataFrame to store the visitor information
        if not all([name, surname, rep, check_in, check_out, hotel]):
            st.error("Please fill out all fields before submitting.")
            return
        visitor_data = {
            "First Name": name,
            "Last Name": surname,
            "Company/Organization": rep,
            "Check-in Date": check_in,
            "Check-out Date": check_out,
            "Hotel": hotel,
            "Status": status,
            "Payment Status": "Pending"
        }
        df = pd.DataFrame([visitor_data])
        # df['Check-in Date'] = df['Check-in Date']
        # df['Check-out Date'] = df['Check-out Date']
        df['Status'] = df.apply(lambda row: "Checked-in" if row['Check-in Date'] <= datetime.date.today() <= row['Check-out Date'] else ("Checked-out" if row['Check-out Date'] < datetime.date.today() else "Upcoming"), axis=1)
        
        # Display the visitor information
        st.subheader("Visitor Information:")
        st.write(df)
        
        pd.DataFrame(visitor_data, index=[0]).to_csv("visitor_data.csv", mode='a', header=not pd.io.common.file_exists("visitor_data.csv"), index=False)
        st.success("Visitor information submitted successfully!")

def visitor_list():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 🏨 Visitor List")
        st.markdown("Below is the list of registered visitors.")
    with col2:
        # Limit rows
        row_limit = st.number_input("Rows to Display", min_value=1, value=10, step=1)
    try:
        df = pd.read_csv("visitor_data.csv")
        df['Check-in Date'] = pd.to_datetime(df['Check-in Date']).dt.date
        df['Check-out Date'] = pd.to_datetime(df['Check-out Date']).dt.date
        df['Status'] = df.apply(lambda row: "Checked-in" if row['Check-in Date'] <= datetime.date.today() <= row['Check-out Date'] else ("Checked-out" if row['Check-out Date'] < datetime.date.today() else "Upcoming"), axis=1)
        
        # Filter section
        st.markdown("### Filters")
        search_term = ""
        status_filter = ["Checked-in", "Checked-out", "Upcoming"]
        payment_filter = ["Pending", "Paid"]
        hotel_filter = df["Hotel"].unique().tolist()

        with st.expander("🔍 Filters", expanded=False):
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 1.5])

            with filter_col1:
                status_filter = st.multiselect("Filter by Status", ["Checked-in", "Checked-out", "Upcoming"], default=["Checked-in", "Checked-out", "Upcoming"])

            with filter_col2:
                payment_filter = st.multiselect("Filter by Payment Status", ["Pending", "Paid"], default=["Pending", "Paid"])

            with filter_col3:
                hotel_filter = st.multiselect("Filter by Hotel", df["Hotel"].unique().tolist(), default=df["Hotel"].unique().tolist())

            with filter_col4:
                search_term = st.text_input("Search by Name", placeholder="First or Last Name")

        # Apply filters
        filtered_df = df[(df['Status'].isin(status_filter)) & 
                 (df['Payment Status'].isin(payment_filter)) & 
                 (df['Hotel'].isin(hotel_filter))]

        # Apply search filter
        if search_term:
            filtered_df = filtered_df[
                (filtered_df['First Name'].str.contains(search_term, case=False, na=False)) |
                (filtered_df['Last Name'].str.contains(search_term, case=False, na=False))
            ]

        # Limit the number of rows displayed
        filtered_df = filtered_df.tail(row_limit)

        st.markdown("---")
        
        # Header row
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1, 1, 2, 0.8, 0.8, 1.5, 1, 0.8, 0.8, 0.8])
        with col1:
            st.markdown("**First Name**")
        with col2:
            st.markdown("**Last Name**")
        with col3:
            st.markdown("**Company/Organization**")
        with col4:
            st.markdown("**Check-in**")
        with col5:
            st.markdown("**Check-out**")
        with col6:
            st.markdown("**Hotel**")
        with col7:
            st.markdown("**Status**")
        with col8:
            st.markdown("**Payment**")
        with col9:
            st.markdown("**Action**")
        with col10:
            st.markdown("**Edit**")
        st.markdown("---")
        
        # Data rows with highlighting and edit functionality
        for idx, (index, row) in enumerate(filtered_df.iterrows()):
            if idx >= row_limit:
                break
            # Determine background color based on status
            if row['Status'] == 'Checked-in':
                bg_color = '#90EE90'  # Light green
            elif row['Status'] == 'Checked-out':
                bg_color = '#FFB6C6'  # Light red
            else:  # Upcoming
                bg_color = '#87CEEB'  # Light blue
            
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1, 1, 2, 0.8, 0.8, 1.5, 0.8, 0.8, 1, 0.8])
            
            with col1:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["First Name"]}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["Last Name"]}</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["Company/Organization"]}</div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["Check-in Date"]}</div>', unsafe_allow_html=True)
            with col5:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["Check-out Date"]}</div>', unsafe_allow_html=True)
            with col6:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["Hotel"]}</div>', unsafe_allow_html=True)
            with col7:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["Status"]}</div>', unsafe_allow_html=True)
            with col8:
                st.markdown(f'<div style="background-color: {bg_color}; padding: 5px; border-radius: 5px;">{row["Payment Status"]}</div>', unsafe_allow_html=True)
            with col9:
                if st.button("Toggle", key=f"payment_{index}"):
                    updated_df = pd.read_csv("visitor_data.csv")
                    current_status = updated_df.loc[index, 'Payment Status']
                    new_status = "Paid" if current_status == "Pending" else "Pending"
                    updated_df.loc[index, 'Payment Status'] = new_status
                    updated_df.to_csv("visitor_data.csv", index=False)
                    st.rerun()
            with col10:
                if st.button("Edit", key=f"edit_{index}"):
                    st.session_state[f"editing_{index}"] = True
            
            # Edit form
            if st.session_state.get(f"editing_{index}", False):
                st.markdown("---")
                st.markdown(f"### Edit Visitor {index + 1}")
                
                edit_col1, edit_col2 = st.columns(2)
                with edit_col1:
                    new_first_name = st.text_input("First Name", value=row["First Name"], key=f"fn_{index}")
                    new_last_name = st.text_input("Last Name", value=row["Last Name"], key=f"ln_{index}")
                    new_rep = st.text_input("Company/Organization", value=row["Company/Organization"], key=f"rep_{index}")
                with edit_col2:
                    new_check_in = st.date_input("Check-in Date", value=row["Check-in Date"], key=f"ci_{index}")
                    new_check_out = st.date_input("Check-out Date", value=row["Check-out Date"], key=f"co_{index}")
                    new_hotel = st.selectbox("Hotel", ["Hilton London Paddington", "London Hilton On Park Lane",
                                                       "Royal Lancaster London", "The Landmark London"],
                                           index=["Hilton London Paddington", "London Hilton On Park Lane",
                                                  "Royal Lancaster London", "The Landmark London"].index(row["Hotel"]),
                                           key=f"hotel_{index}")
                
                edit_btn_col1, edit_btn_col2 = st.columns(2)
                with edit_btn_col1:
                    if st.button("Save", key=f"save_{index}"):
                        updated_df = pd.read_csv("visitor_data.csv")
                        updated_df.loc[index, "First Name"] = new_first_name
                        updated_df.loc[index, "Last Name"] = new_last_name
                        updated_df.loc[index, "Company/Organization"] = new_rep
                        updated_df.loc[index, "Check-in Date"] = new_check_in
                        updated_df.loc[index, "Check-out Date"] = new_check_out
                        updated_df.loc[index, "Hotel"] = new_hotel
                        updated_df.to_csv("visitor_data.csv", index=False)
                        st.session_state[f"editing_{index}"] = False
                        st.rerun()
                with edit_btn_col2:
                    if st.button("Cancel", key=f"cancel_{index}"):
                        st.session_state[f"editing_{index}"] = False
                        st.rerun()
        
        # Key/Legend
        st.markdown("---")
        st.markdown("### Legend")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div style="background-color: #90EE90; padding: 10px; border-radius: 5px;"><b>Checked-in</b> - Guest is currently at the hotel</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="background-color: #FFB6C6; padding: 10px; border-radius: 5px;"><b>Checked-out</b> - Guest has left the hotel</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="background-color: #87CEEB; padding: 10px; border-radius: 5px;"><b>Upcoming</b> - Guest arrival pending</div>', unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("No visitor data found. Please register a visitor first.")

