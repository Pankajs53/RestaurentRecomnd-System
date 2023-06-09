import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from wordcloud import WordCloud
from io import BytesIO

class ZRecomand:
    def __init__(self, df, similarity):
        self.df = df
        self.similarity = similarity
        self.choosencusine = None
        self.restn = None
        self.map_fig = None

    def TotalRestaAvailableInEachCity(self):
        try:
            # reading the geo file
            fp = "C:\\Users\\312tx asus\\Desktop\\Faltu Projects\\NLP BASED\\newR\\Maps_with_python-master\\india-polygon.shp"
            map_df = gpd.read_file(fp)
            map_df_copy = gpd.read_file(fp)

            # creating a df with state count
            m = []
            for i, j in self.df['state'].value_counts().items():
                m.append({'State': i, 'Count': j})

            statedf = pd.DataFrame(m)

            # Merging the data
            merged = map_df.set_index('st_nm').join(statedf.set_index('State'))
            merged['Count'] = merged['Count'].replace(np.nan, 0)

            # Create figure and axes for Matplotlib and set the title
            fig, ax = plt.subplots(1, figsize=(10, 10))
            ax.axis('off')
            ax.set_title('Number of Restaurants Available Per State',
                         fontdict={'fontsize': '20', 'fontweight': '10'})

            # Plot the figure
            merged.plot(column='Count', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0', legend=True)

            # Save the figure to a buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close(fig)

            # Assign the figure to the map_fig attribute
            self.map_fig = fig

        except FileNotFoundError:
            st.error("File Not Found. Please provide the correct path for the Geo Location File.")
        except KeyError:
            st.error("The 'State/st_nm' column is missing in the dataframe.")
        except Exception as e:
            st.error("An error occurred: " + str(e))


    def choose_state(self):
        # Print the unique list of cities/states
        states = self.df['state'].unique().tolist()

        # Flag to track the validity of the selected state/city
        valid_state = False

        # Loop until a valid state/city is selected
        while not valid_state:
            try:
                # Prompt the user to choose a state/city
                self.rest = st.selectbox('Choose a state', states)

                # Check if the selected state/city is in the list of unique cities/states
                if self.rest not in self.df['state'].unique().tolist():
                    # Raise a ValueError if the input is not in the list
                    raise ValueError("INVALID STATE/CITY SELECTED")

                # Set the flag to True if a valid city/state is selected
                valid_state = True

            except ValueError as ve:
                # Print the custom error message for an invalid state/city selection
                st.error(str(ve))

            except Exception as e:
                st.error("Please choose a correct state/city from the above list")

    def choose_city(self):
        cities = self.df[self.df['state'] == self.rest]['City'].unique().tolist()
        valid_city = False
        while not valid_city:
            try:
                self.choosencity = st.selectbox('Choose a city', cities)
                if self.choosencity not in self.df[self.df['state'] == self.rest]['City'].unique().tolist():
                    raise ValueError("INVALID CITY")

                valid_city = True

            except ValueError as ve:
                st.error(str(ve))

            except Exception as e:
                st.error("Please choose a correct city from the above list")

    def total_rest_incity(self):
        st.write("The number of Restaurants Available in the city: ", self.df[self.df['City'] == self.choosencity].shape[0])
        st.write("Most Famous Cuisines as per the selected City")
        self.cusines_asper_city()

    def cusines_asper_city(self):
        values = self.df[self.df['City'] == self.choosencity]['Cuisines'].dropna().tolist()
        # Concatenate the values into a single string
        text = ' '.join(values)
        # Create the WordCloud object
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        # Create the figure and plot the word cloud
        fig = plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        # Pass the figure to Streamlit
        st.pyplot(fig)
    
    def selectCusine(self):
        newdata = self.df[self.df['City'] == self.choosencity]
        cu = []
    
        for i in newdata['Cuisines']:
            cuisine = i.split(", ")
            for j in cuisine:
                if j not in cu:
                    cu.append(j)
    
        st.write("List of all Cuisines Available", cu)
    
        valid_cuisine = False
    
        while not valid_cuisine:
            try:
                self.choosencusine = st.selectbox("Please select a cuisine from the above cuisine list", cu)
                valid_cuisine = True
            except Exception as e:
                st.write(e)
    
        return self.choosencusine


    def restnamepercity(self, choosencity, choosencuisine):
        restpercity = self.df[
            (self.df['City'] == choosencity) & (self.df['Cuisines'].str.contains(choosencuisine, case=False))]
        restnames = restpercity['Restaurant Name'].unique().tolist()
    
        st.write(restnames)
    
        if len(restnames) == 0:
            st.warning("No matching restaurants found")
            return
    
        selected_rest = st.selectbox("Select a restaurant:", restnames)
    
        if selected_rest:
            self.restn = selected_rest
            index = restpercity[restpercity['Restaurant Name'] == selected_rest].index[0]
            self.top5similarResAcroosTheCity(index)

    def top5similarResAcroosTheCity(self, index):
        n = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda x: x[1])
        l_index = []
        count = 0
        
        for i in n:
            if count < 6:
                l_index.append(i[0])
                count += 1
        
        l_index = l_index[1:]
        
        rest = []
        for i in l_index:
            rest.append(self.df.loc[i]['Restaurant Name'])
        
        st.write("Top 5 Similar Restaurants across the city:")
        for r in rest:
            st.write(r)
