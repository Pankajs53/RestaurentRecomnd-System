import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from wordcloud import WordCloud
from io import BytesIO
from oops2 import ZRecomand

try:
    df = pickle.load(open('newdata.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("File not found. Please provide the correct file paths.")
except Exception as e:
    st.error("An error occurred while loading the files: " + str(e))



def main():
    st.title("ZRecomand App")
   
    # Create an instance of the ZRecomand class
    zr = ZRecomand(df, similarity)

    # Brief Introduction
    st.write("🍽️ Welcome to the ZRecomand App! 🌟")
    st.write("Discover amazing restaurants and get personalized recommendations based on cuisine similarity.")
    st.write("🔍 To get started, follow the instructions below:")
    st.write("1. 🌍 Select a state from the drop-down list.")
    st.write("2. 🏙️ Once you select a state, a list of cities in that state will be displayed.")
    st.write("3. 📍 Choose a city from the list.")
    st.write("4. 🍔 The app will show you the total number of restaurants available in the selected city.")
    st.write("5. 🌮 You can also explore the most famous cuisines in that city using a word cloud visualization.")
    st.write("6. 🍽️ Select a cuisine from the cuisine list to get recommendations.")
    st.write("7. 🗺️ The app will provide you with the top 5 similar restaurants across the city based on your selection.")
    st.write("8. 🔁 You can explore different cities and cuisines by repeating the steps above.")

    # Generate the map plot
    zr.TotalRestaAvailableInEachCity()

    # Display the map plot
    st.pyplot(zr.map_fig)


    zr.choose_state()

    if zr.rest:
        zr.choose_city()
        zr.total_rest_incity()
        zr.selectCusine()

        if zr.choosencusine:
            zr.restnamepercity(zr.choosencity, zr.choosencusine)  # Pass the arguments here


if __name__ == '__main__':
    main()
