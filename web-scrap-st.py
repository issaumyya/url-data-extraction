import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

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

        # Print property values for the first 100 entries
        st.write("Property Values:")
        
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

        for u in df['URLs'][:100]:
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

        st.dataframe(property_data)
    else:
        st.warning("No URLs were scraped.")
