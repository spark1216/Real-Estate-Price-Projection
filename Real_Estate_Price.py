import streamlit as st
import pandas as pd
import numpy as np
st.title('US Real Estate Price Prediction')
import util
util.load_saved_artifacts()

housesize= st.number_input('House Area (Square Feet)', 800)
zipcode = st.number_input('Zipcode(5-Digit)',10021)
acre_lot = st.number_input('Acre Lot (Square Feet)',0)
bed = st.selectbox(
    'Bed',
    (0,1,2,3,4,5))
bath = st.selectbox(
    'Bath',
    (0,1,2,3,4,5))
estimatepricebutton=st.button("Estimate Price!")
if estimatepricebutton:
    price=util.get_estimated_price(bed, bath, acre_lot, housesize, zipcode)
    st.write(f"Estimated Price: ${price}")
