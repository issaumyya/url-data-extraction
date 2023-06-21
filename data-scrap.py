import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

def scrape_url(custom_url):
    urll = []
    result = requests.get(custom_url).text
    soup = BeautifulSoup(result, 'html.parser')
    pro_url = soup.find_all('div', class_='title-line')
    for p in pro_url:
        for a in p.find_all('a', class_='typelink', href=True):
            urll.append(a['href'])
    return urll

# Streamlit UI
st.set_page_config(
    page_title="Hello!",
    page_icon="👋",
)
st.title("Property Values from Custom URL")
st.write("Enter a custom URL from makaan.com to scrape property values:")

def search_on_makaan(query):
    # Create the search URL based on the query
    search_url = f"https://www.makaan.com/pune-residential-property/buy-property-in-{query}-city"
    return search_url

# Create a search bar in the Streamlit app
search_query = st.text_input("Enter your search query for Makaan.com")

# Create a button to trigger the search action
search_button = st.button("Search")

# Check if the search button is clicked and perform the search action
if search_button:
    scraped_urls = scrape_url(search_on_makaan(search_query))
    if scraped_urls:
        st.subheader("Property Values:")
        
        bedroom = []
        sq_ft = []
        new = []
        negotiable = []
        sec_deposit = []
        facing = []
        status = []
        price = []
        carpet_sq_ft = []
        bathroom = []
        booking_amt = []
        floor_no = []
        construction_status = []
        sub_loc = []
        age_of_property = []

        for u in scraped_urls:
            result = requests.get(u).text
            soup = BeautifulSoup(result, 'html.parser')

            bhk1 = soup.find('span', class_='type')
            bedroom.append(bhk1.text if bhk1 else np.nan)

            sq_ft1 = soup.find('span', class_='size')
            sq_ft.append(sq_ft1.text if sq_ft1 else np.nan)

            new1 = soup.find('td', id='New/Resale')
            new.append(new1.text if new1 else np.nan)

            neg1 = soup.find('td', id='Price Negotiable')
            negotiable.append(neg1.text if neg1 else np.nan)

            sec1 = soup.find('td', id='Security Deposit')
            sec_deposit.append(sec1.text if sec1 else np.nan)

            fac1 = soup.find('td', id='Facing')
            facing.append(fac1.text if fac1 else np.nan)

            fur = soup.find('div', class_='kd-wrap js-list-wrap')
            if fur:
                fur1 = fur.find('td', id='Status')
                status.append(fur1.text if fur1 else np.nan)
            else:
                status.append(np.nan)

            price1 = soup.find('span', class_='price')
            price.append(price1.text if price1 else np.nan)

            car1 = soup.find('td', id='Carpet area')
            carpet_sq_ft.append(car1.text if car1 else np.nan)

            bath1 = soup.find('td', id='Bathrooms')
            bathroom.append(bath1.text if bath1 else np.nan)

            booking1 = soup.find('td', id='Booking Amount')
            booking_amt.append(booking1.text if booking1 else np.nan)

            floor1 = soup.find('td', id='Floor')
            floor_no.append(floor1.text.split(' ')[0] if floor1 else np.nan)

            constr1 = soup.find('td', id='Status')
            construction_status.append(constr1.text if constr1 else np.nan)

            subloc = soup.find('span', class_='ib loc-name')
            sub_loc.append(subloc.text if subloc else np.nan)

            age = soup.find('td', id='Age of Property')
            age_of_property.append(age.text if age else np.nan)

        property_data = pd.DataFrame({
            "Bedroom": bedroom,
            "Sq Ft": sq_ft,
            "New/Resale": new,
            "Negotiable": negotiable,
            "Security Deposit": sec_deposit,
            "Facing": facing,
            "Status": status,
            "Price": price,
            "Carpet Sq Ft": carpet_sq_ft,
            "Bathroom": bathroom,
            "Booking Amount": booking_amt,
            "Floor No": floor_no,
            "Construction Status": construction_status,
            "Sub Loc": sub_loc,
            "Age of Property": age_of_property
        })

        # Display property values
        st.dataframe(property_data)

        # Ask user for Excel file name
        excel_file_name = st.text_input("Enter the Excel file name (without extension):", value="property_values")

        # Save DataFrame to Excel if Excel button is clicked
        if st.button("Save as Excel"):
            excel_file_path = f"{excel_file_name}.xlsx"
            property_data.to_excel(excel_file_path, index=False)
            st.success(f"Property values saved to {excel_file_path}!")
    else:
        st.warning("No URLs were scraped.")
 else:
    st.warning("Coudnt find any urls")
