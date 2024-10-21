import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# Set up the Streamlit app layout
st.set_page_config(layout="wide")
st.title("Web Page Analyzer")

# Input URL field
url = st.text_input("Enter URL:", "https://www.plap.mil.cn/")

# Analyze button
if st.button("Analyze"):
    try:
        # Fetch the webpage using requests with appropriate headers
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # Parse the webpage content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create two columns layout in Streamlit
        col1, col2 = st.columns(2)

        # Display the webpage content in column 1
        with col1:
            st.subheader("Webpage Content")
            st.components.v1.html(response.text, height=600, scrolling=True)

        # Column 2 for links, text content, and network info
        with col2:
            # Links tab
            with st.expander("Links Found"):
                links = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        full_url = urljoin(url, href)
                        links.append({'Text': link.text.strip(), 'URL': full_url})
                st.dataframe(pd.DataFrame(links))  # Display the links in a table

            # Text tab
            with st.expander("Text Content"):
                text = soup.get_text()
                st.text_area("Extracted Text Content", text, height=200)

            # Network info tab
            with st.expander("Network Info"):
                st.json({
                    'Status Code': response.status_code,
                    'Headers': dict(response.headers),
                    'Content Type': response.headers.get('content-type'),
                    'Encoding': response.encoding,
                    'Response Time': response.elapsed.total_seconds()
                })

    # Error handling to display any exceptions
    except Exception as e:
        st.error(f"Error: {str(e)}")
