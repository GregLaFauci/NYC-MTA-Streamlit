import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import matplotlib.pyplot as plt

def main():

    st.title('MTA Stations in NYC')

    DATA_URL = ('Stations3.csv')

    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows, index_col=0)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data['date_opened'] = pd.to_datetime(data['date_opened'])
        print(data)
        return data

    # data_load_state = st.text('Loading data...')
    data = load_data(500)
    # data_load_state.text('Loading data... done!')

    yearDF = pd.DataFrame(data['date_opened'].dt.year.value_counts())

    years = data['date_opened'].dt.year.value_counts().index.tolist()

    counts = data['date_opened'].dt.year.value_counts().values.tolist()

    year_counts_zip = zip(years, counts)
    year_counts = list(year_counts_zip)
    year_counts.sort(key=lambda x: x[0], reverse=False)




    # Some number in the range 1885-2020
    year_to_filter = st.slider('Select a year to filter open subway stations at that time:', 1885, 2020, 1980)
    filtered_data = data[data['date_opened'].dt.year <= year_to_filter]    

    st.subheader('Map of all stations in %s' % year_to_filter)



    viewport = pdk.data_utils.compute_view(points=data[['longitude', 'latitude']], view_proportion=0.6)

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=viewport,
        layers=[
            pdk.Layer(
                'ScatterplotLayer', 
                data=filtered_data, 
                auto_highlight=True,
                get_radius=80, 
                get_fill_color='[red, green, blue ]', 
                get_position='[longitude, latitude]',
                pickable=True)
            ]
        ))


    st.subheader('Number of stations by year')
    st.bar_chart(yearDF, use_container_width=True)


    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    if st.checkbox('Show filtered data'):
        st.subheader('Filtered data')
        st.write(filtered_data)

if __name__ == '__main__':
    main()