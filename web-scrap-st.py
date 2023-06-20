import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_url(p, q, custom_url):
    urll = []
    if custom_url:
        urll.append(custom_url)
    else:
        base_url = 'https://www.makaan.com/mumbai/mumbai-south-property-10046?page='
        for i in range(p, q + 1):
            url = base_url + str(i)
            result = requests.get(url).text
            soup = BeautifulSoup(result, 'html.parser')
            pro_url = soup.find_all('div', class_='title-line')
            for p in pro_url:
                for a in p.find_all('a', class_='typelink', href=True):
                    urll.append(a['href'])
    return urll


# Streamlit UI
st.title("Scrape URLs from Makaan.com")
st.write("Enter the starting and ending page numbers or a custom URL to scrape URLs:")

p = st.number_input("Enter the starting page number:", value=1, step=1)
q = st.number_input("Enter the ending page number:", value=1, step=1)
custom_url = st.text_input("Enter a custom URL (optional):")

if st.button("Scrape URLs"):
    # Scrape the URLs
    scraped_urls = scrape_url(int(p), int(q), custom_url)

    # Ask user for Excel file name
    excel_file_name = st.text_input("Enter the Excel file name (without extension):", value="scraped_urls")

    if scraped_urls:
        # Create a DataFrame from the scraped URLs
        df = pd.DataFrame({"URLs": scraped_urls})

        # Save DataFrame to Excel
        excel_file_path = f"{excel_file_name}.xlsx"
        df.to_excel(excel_file_path, index=False)

        st.success(f"Scraped URLs saved to {excel_file_path}!")
    else:
        st.warning("No URLs were scraped.")
