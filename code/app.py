import streamlit as st
import numpy as np
import pandas as pd
import functions as fn
import plotly.express as px
import plotly.figure_factory as ff


st.title('Explore Storm Events in US States')
st.write('''

Climate change has had highly variable effects in different places.
This dashboard lets you see the climate impacts so far. For each state, you can see the impact of extreme weather events on: 
         
- Number of Deaths
- Damage to property
- Damage to crops''')

@st.cache
def load_data():
    data = pd.read_pickle("storm_data_final.pkl")
    return data

# Create a text element and let the reader know the data is loading.
#data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
#data_load_state.text("Loading data... Done!")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data[:100])

######################### PIE CHART ##########################

state = st.selectbox('Select a state',sorted(data.state.unique().tolist()))
measure = st.radio("Select measure of climate impact",('deaths', 'damage_property', 'damage_crops'))

def generate_pie(data, measure, state = 'the United States'):
    
    if state != 'the United States':
        data = data[data['state'] == state]
    data_by_event = data[['year', 'event_type', 'injuries', 'deaths', 'damage_property', 'damage_crops']].groupby(['event_type'])[['injuries', 'deaths', 'damage_property', 'damage_crops']].sum().reset_index()
    pie_fig = px.pie(data_by_event, values=data_by_event[measure], names=data_by_event.event_type, color=data_by_event.event_type)
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    pie_fig.update_layout(title=f"<b>{measure.title()} caused by extreme weather in {state}</b>", title_x=0.5)
    st.plotly_chart(pie_fig)
    
generate_pie(data, measure, state)



######################### CHOROPLETH MAPS ##########################

def map_events(data, year, measure, state= 'usa'):
    
    state_grouped = data.groupby(['state', 'fips', 'year'])[measure].sum().reset_index()
    if state != 'usa':
        state_df = state_grouped[(state_grouped['state'] == state) & (state_grouped['year'] == year)]
    else: 
        state_df = state_grouped[(state_grouped['year'] == year)]
    values = state_df[measure].tolist()
    fips = state_df['fips'].tolist()

    colorscale = [
        'rgb(193, 193, 193)',
        'rgb(239,239,239)',
        'rgb(195, 196, 222)',
        'rgb(144,148,194)',
        'rgb(101,104,168)',
        'rgb(65, 53, 132)']

    fig = ff.create_choropleth(
        fips=fips, values=values, scope=[state],
        binning_endpoints=[1000, 10000, 100000, 1000000], colorscale=colorscale,
        county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
        legend_title=f'{measure.title()} by County', title=f'{state.upper()}, {year}'
    )
    st.plotly_chart(fig)

year = st.slider('Year', 1997, 2019, 2019)  # min: 0h, max: 23h, default: 17h

map_events(data, year, 'damage_property', state)


###################### IMAGES ########################

st.subheader('''

Compare with the nation overall.''')

st.image('/Users/NeilenBenvegnu/Downloads/newplot (1).png', caption=None, width=None, use_column_width='auto', clamp=False, channels='RGB', output_format='auto')

st.write('''Results are derived from the National Oceanic and Atmospheric Administration's [Storm Events Database](https://www.ncdc.noaa.gov/stormevents/ftp.jsp).''')