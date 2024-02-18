import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd

# Define a function to extract addresses from an HTML file
def extract_addresses(html):
    soup = BeautifulSoup(html, 'html.parser')
    address_spans = soup.find_all('span', id=lambda x: x and x.startswith('PageContent_dgvDetails_lblAddress'))
    addresses = [span.text.strip() for span in address_spans]
    return addresses

# Create a file uploader widget
uploaded_files = st.file_uploader("Upload your HTML files", accept_multiple_files=True)

# Display the number of files uploaded
if uploaded_files:
    st.write(f"Number of files uploaded: {len(uploaded_files)}")

# Dropdown box for selecting the ward
ward_options = [f'Ward {i}' for i in range(1, 101)]
selected_ward = st.selectbox("Select Ward:", ward_options)

# Button to extract addresses and save to CSV
if st.button("Extract"):
    if uploaded_files:
        all_addresses = []

        # Iterate over each uploaded file
        for uploaded_file in uploaded_files:
            html = uploaded_file.getvalue().decode("utf-8")
            addresses = extract_addresses(html)
            all_addresses.extend(addresses)

        # Convert the addresses to a DataFrame
        df = pd.DataFrame({"Address": all_addresses})

        # Save to CSV with the selected ward name
        csv_file_name = f'{selected_ward.lower()}_addresses_combined.csv'
        df.to_csv(csv_file_name, index=False)

        st.success(f'Addresses extracted and saved to {csv_file_name}')

# Display the addresses in a table
if "df" in locals():
    st.write(df)

# Provide a direct link to download the combined CSV file
if "csv_file_name" in locals():
    st.markdown(f"Download your combined CSV file [here](/{csv_file_name})")

# Button to download the combined CSV file directly
if "csv_file_name" in locals():
    download_button = st.download_button(
        label="Download Combined File",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=csv_file_name,
        key="download_csv_file",
        help="Click to download the combined CSV file"
    )
