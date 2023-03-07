import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber Pickups in NYC')

date_column = 'date/time'
data_url = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(data_url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[date_column] = pd.to_datetime(data[date_column])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Done! (using st.cache_data)')

#st.subheader('Raw Data')
#st.write(data)
if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(data)

st.subheader('Number of Pickups by Hour')

hist_values = np.histogram(
    data[date_column].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

#st.subheader('Map of All Pickups')
#st.map(data)
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[date_column].dt.hour == hour_to_filter]
st.subheader(f'Map of All Pickups at {hour_to_filter}:00')
st.map(filtered_data)